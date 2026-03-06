#!/usr/bin/env python3
"""
台灣總體統計資料庫通用查詢腳本
支援 20 個統計領域、254 個資料表

用法:
  python query_nstat.py --code A046201010 --start 2024-M1 --end 2024-M12
  python query_nstat.py --search "薪資"
  python query_nstat.py --domain "勞工統計"
  python query_nstat.py --list-domains
  python query_nstat.py --code A046201010 --describe
"""

import json
import sys
import os
import argparse
import time

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

BASE_URL = "https://nstatdb.dgbas.gov.tw/dgbasAll/webMain.aspx?sdmx/"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CODES_FILE = os.path.join(SCRIPT_DIR, "..", "references", "function_codes.json")


def load_function_codes():
    """載入功能代碼對照表"""
    try:
        with open(CODES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(json.dumps({"error": f"找不到功能代碼對照表: {CODES_FILE}"}, ensure_ascii=False, indent=2))
        sys.exit(1)


def fetch_dataset(func_code, retries=1):
    """下載完整資料集，含重試機制"""
    if not HAS_REQUESTS:
        print(json.dumps({
            "error": "缺少 requests 套件，請執行: pip install requests",
            "url": BASE_URL + func_code
        }, ensure_ascii=False, indent=2))
        sys.exit(1)

    url = BASE_URL + func_code
    for attempt in range(retries + 1):
        try:
            resp = requests.get(url, timeout=60)
            resp.raise_for_status()
            ct = resp.headers.get("Content-Type", "")
            if "json" not in ct.lower():
                if attempt < retries:
                    time.sleep(2)
                    continue
                return {"error": f"API 回傳非 JSON 格式 (Content-Type: {ct})，請確認功能代碼 {func_code} 是否正確"}
            return resp.json()
        except requests.exceptions.Timeout:
            if attempt < retries:
                time.sleep(2)
                continue
            return {"error": "API 請求逾時（60秒），請稍後再試"}
        except requests.exceptions.RequestException as e:
            if attempt < retries:
                time.sleep(2)
                continue
            return {"error": f"API 請求失敗: {str(e)}"}
        except json.JSONDecodeError:
            return {"error": "API 回應無法解析為 JSON"}
    return {"error": "重試後仍失敗"}


def parse_structure(data):
    """解析 API-JSON 結構"""
    # structure 可能在 data.structure 或 data.data.structure
    structure = data.get("structure", {})
    if not structure or (isinstance(structure, str) and not structure.strip()):
        structure = data.get("data", {}).get("structure", {})

    dimensions = structure.get("dimensions", {})
    series_dims = dimensions.get("series", [])
    obs_dims = dimensions.get("observation", [])

    dim_maps = []
    for dim in series_dims:
        dmap = {
            "name": dim.get("name", ""),
            "keyPosition": dim.get("keyPosition", 0),
            "values": {}
        }
        for v in dim.get("values", []):
            dmap["values"][v["id"]] = v["name"]
        dim_maps.append(dmap)

    time_map = {}
    for o in obs_dims:
        for idx, v in enumerate(o.get("values", [])):
            time_map[str(idx)] = {"id": v["id"], "name": v["name"]}

    return dim_maps, time_map


def describe_table(data, func_code, code_info):
    """描述資料表的維度結構"""
    dim_maps, time_map = parse_structure(data)
    
    lines = []
    lines.append(f"## {code_info.get('name', func_code)}")
    lines.append(f"- **功能代碼**: {func_code}")
    lines.append(f"- **統計領域**: {code_info.get('domain', '未知')}")
    lines.append(f"- **資料來源**: 行政院主計總處")
    lines.append("")

    for i, dm in enumerate(dim_maps):
        lines.append(f"### 維度 {i+1}：{dm['name']} (keyPosition={dm['keyPosition']})")
        lines.append(f"共 {len(dm['values'])} 項：")
        lines.append("")
        lines.append("| id | 名稱 |")
        lines.append("|----|------|")
        for vid in sorted(dm["values"].keys(), key=lambda x: int(x) if x.isdigit() else x):
            lines.append(f"| {vid} | {dm['values'][vid]} |")
        lines.append("")

    if time_map:
        sorted_times = sorted(time_map.values(), key=lambda x: x["id"])
        lines.append(f"### 統計期間")
        lines.append(f"- **範圍**: {sorted_times[0]['name']} ~ {sorted_times[-1]['name']}")
        lines.append(f"- **筆數**: {len(sorted_times)}")
        lines.append("")

    return "\n".join(lines)


def filter_data(data, func_code, code_info, dim_filters, start_time, end_time):
    """篩選指定維度與時間範圍的數據"""
    dim_maps, time_map = parse_structure(data)

    if not dim_maps:
        return {"error": "無法解析資料表維度結構"}

    datasets = data.get("data", {}).get("dataSets", [])
    if not datasets:
        return {"error": "API 回應無資料集"}

    all_series = datasets[0].get("series", {})

    # 決定要查詢的 series keys
    target_keys = []
    if dim_filters:
        # 有指定維度篩選
        dim_indices = {}
        for dim_idx, filter_ids in dim_filters.items():
            dim = dim_maps[dim_idx]
            id_list = sorted(dim["values"].keys(), key=lambda x: int(x) if x.isdigit() else x)
            indices = []
            for fid in filter_ids:
                if str(fid) in dim["values"]:
                    try:
                        idx = id_list.index(str(fid))
                        indices.append(idx)
                    except ValueError:
                        pass
            dim_indices[dim_idx] = indices if indices else list(range(len(id_list)))

        # 對未指定的維度，使用全部
        for i in range(len(dim_maps)):
            if i not in dim_indices:
                dim_indices[i] = list(range(len(dim_maps[i]["values"])))

        # 生成所有組合
        from itertools import product
        dim_count = len(dim_maps)
        ranges = [dim_indices.get(i, [0]) for i in range(dim_count)]
        for combo in product(*ranges):
            key = ":".join(str(c) for c in combo)
            if key in all_series:
                target_keys.append(key)
    else:
        target_keys = list(all_series.keys())

    # 收集結果
    results = []
    for series_key in target_keys:
        if series_key not in all_series:
            continue
        
        observations = all_series[series_key].get("observations", {})
        
        # 解析 series key 為維度標籤
        indices = series_key.split(":")
        dim_labels = []
        for i, idx_str in enumerate(indices):
            if i < len(dim_maps):
                idx = int(idx_str)
                id_list = sorted(dim_maps[i]["values"].keys(), key=lambda x: int(x) if x.isdigit() else x)
                if idx < len(id_list):
                    vid = id_list[idx]
                    dim_labels.append({
                        "dim_name": dim_maps[i]["name"],
                        "value_id": vid,
                        "value_name": dim_maps[i]["values"][vid]
                    })

        for obs_idx, values in observations.items():
            time_info = time_map.get(obs_idx, {})
            time_id = time_info.get("id", "")
            time_name = time_info.get("name", "")

            if not time_id:
                continue

            if start_time and not _time_in_range(time_id, start_time, end_time):
                continue

            val = values[0] if values else None
            if val is not None:
                record = {
                    "period_id": time_id,
                    "period_name": time_name,
                    "value": val
                }
                for dl in dim_labels:
                    record[dl["dim_name"]] = dl["value_name"]
                results.append(record)

    # 排序
    results.sort(key=_sort_key)

    return {
        "function_code": func_code,
        "table_name": code_info.get("name", func_code),
        "domain": code_info.get("domain", ""),
        "source": "行政院主計總處",
        "record_count": len(results),
        "dimensions": [dm["name"] for dm in dim_maps],
        "data": results
    }


def _sort_key(item):
    pid = item.get("period_id", "")
    if "-M" in pid:
        parts = pid.split("-M")
        return (parts[0], 1, int(parts[1]))
    elif "-Q" in pid:
        parts = pid.split("-Q")
        return (parts[0], 2, int(parts[1]))
    else:
        return (pid, 0, 0)


def _time_in_range(time_id, start_time, end_time):
    """檢查 time_id 是否在範圍內"""
    def normalize(t):
        if "-M" in t:
            parts = t.split("-M")
            return f"{parts[0]}-{int(parts[1]):02d}"
        if "-Q" in t:
            return t
        return t

    norm_id = normalize(time_id)
    norm_start = normalize(start_time) if start_time else ""
    norm_end = normalize(end_time) if end_time else "9999"

    # 週期類型須一致
    has_dash_id = "-" in norm_id
    has_dash_start = "-" in norm_start
    if norm_start and has_dash_start != has_dash_id:
        return False

    return norm_start <= norm_id <= norm_end


def search_tables(codes_data, keyword):
    """模糊搜尋資料表"""
    results = []
    all_codes = codes_data.get("codes", {})
    for code, info in all_codes.items():
        name = info.get("name", "")
        domain = info.get("domain", "")
        if keyword.lower() in name.lower() or keyword.lower() in domain.lower() or keyword.upper() in code.upper():
            results.append({"code": code, "name": name, "domain": domain})
    results.sort(key=lambda x: x["code"])
    return results


def list_domains(codes_data):
    """列出所有統計領域"""
    domains = codes_data.get("domains", {})
    result = []
    for d in sorted(domains.keys()):
        result.append({"domain": d, "table_count": len(domains[d])})
    return result


def list_domain_tables(codes_data, domain_name):
    """列出特定領域的所有資料表"""
    all_codes = codes_data.get("codes", {})
    results = []
    for code, info in all_codes.items():
        if domain_name in info.get("domain", ""):
            results.append({"code": code, "name": info["name"], "domain": info["domain"]})
    results.sort(key=lambda x: x["code"])
    return results


def format_markdown(result):
    """格式化為 Markdown"""
    if "error" in result:
        return f"**錯誤**: {result['error']}"

    lines = []
    lines.append(f"### {result['table_name']}")
    lines.append(f"**功能代碼**: {result['function_code']}  ")
    lines.append(f"**統計領域**: {result['domain']}  ")
    lines.append(f"**資料來源**: {result['source']}  ")
    lines.append(f"**筆數**: {result['record_count']}")
    lines.append("")

    if not result["data"]:
        lines.append("_查詢範圍內無資料_")
        return "\n".join(lines)

    # 取得所有欄位（除固定欄位外的維度欄位）
    fixed = {"period_id", "period_name", "value"}
    dim_cols = [k for k in result["data"][0].keys() if k not in fixed]

    # 表頭
    header = "| 統計期 |"
    sep = "|--------|"
    for dc in dim_cols:
        header += f" {dc} |"
        sep += "------|"
    header += " 數值 |"
    sep += "------|"
    lines.append(header)
    lines.append(sep)

    # 資料列
    for d in result["data"]:
        val = d["value"]
        if isinstance(val, (int, float)):
            val_str = f"{val:,.0f}" if val == int(val) else f"{val:,.2f}"
        else:
            val_str = str(val) if val is not None else "—"
        
        row = f"| {d['period_name']} |"
        for dc in dim_cols:
            row += f" {d.get(dc, '')} |"
        row += f" {val_str} |"
        lines.append(row)

    lines.append("")
    lines.append(f"資料來源：行政院主計總處")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="台灣總體統計資料庫通用查詢")
    parser.add_argument("--code", type=str, help="功能代碼 (如 A046201010)")
    parser.add_argument("--search", type=str, help="搜尋資料表關鍵字")
    parser.add_argument("--domain", type=str, help="列出指定領域的資料表")
    parser.add_argument("--list-domains", action="store_true", help="列出所有統計領域")
    parser.add_argument("--describe", action="store_true", help="描述資料表維度結構")
    parser.add_argument("--dim0", type=str, help="維度0篩選 (逗號分隔 id，如 1,2,3)")
    parser.add_argument("--dim1", type=str, help="維度1篩選")
    parser.add_argument("--dim2", type=str, help="維度2篩選")
    parser.add_argument("--start", type=str, help="起始時間 (如 2024, 2024-M1)")
    parser.add_argument("--end", type=str, help="結束時間")
    parser.add_argument("--format", choices=["json", "markdown"], default="markdown", help="輸出格式")

    args = parser.parse_args()
    codes_data = load_function_codes()

    # 列出所有領域
    if args.list_domains:
        domains = list_domains(codes_data)
        if args.format == "json":
            print(json.dumps({"domains": domains}, ensure_ascii=False, indent=2))
        else:
            print("## 總體統計資料庫 — 統計領域一覽\n")
            print("| # | 統計領域 | 資料表數 |")
            print("|---|---------|---------|")
            for i, d in enumerate(domains, 1):
                print(f"| {i} | {d['domain']} | {d['table_count']} |")
            print(f"\n共 {len(domains)} 個領域，{sum(d['table_count'] for d in domains)} 個資料表")
        return

    # 搜尋資料表
    if args.search:
        results = search_tables(codes_data, args.search)
        if args.format == "json":
            print(json.dumps({"results": results, "count": len(results)}, ensure_ascii=False, indent=2))
        else:
            print(f"## 搜尋「{args.search}」結果\n")
            if not results:
                print("_找不到相關資料表_")
            else:
                print("| 功能代碼 | 資料表名稱 | 統計領域 |")
                print("|---------|----------|---------|")
                for r in results:
                    print(f"| {r['code']} | {r['name']} | {r['domain']} |")
                print(f"\n共 {len(results)} 筆")
        return

    # 列出領域資料表
    if args.domain:
        results = list_domain_tables(codes_data, args.domain)
        if args.format == "json":
            print(json.dumps({"tables": results, "count": len(results)}, ensure_ascii=False, indent=2))
        else:
            print(f"## {args.domain} — 資料表清單\n")
            if not results:
                print(f"_找不到「{args.domain}」相關領域_")
                # 建議
                all_domains = list_domains(codes_data)
                similar = [d["domain"] for d in all_domains if args.domain[0:2] in d["domain"]]
                if similar:
                    print(f"\n您可能要找的是：{'、'.join(similar)}")
            else:
                print("| # | 功能代碼 | 資料表名稱 |")
                print("|---|---------|----------|")
                for i, r in enumerate(results, 1):
                    print(f"| {i} | {r['code']} | {r['name']} |")
                print(f"\n共 {len(results)} 個資料表")
        return

    # 需要功能代碼的操作
    if not args.code:
        parser.error("請指定 --code（功能代碼）、--search（搜尋）、--domain（領域）或 --list-domains")

    code_info = codes_data.get("codes", {}).get(args.code, {"name": args.code, "domain": "未知"})

    # 下載資料
    data = fetch_dataset(args.code)
    if isinstance(data, dict) and "error" in data:
        print(json.dumps(data, ensure_ascii=False, indent=2))
        sys.exit(1)

    # 描述維度結構
    if args.describe:
        print(describe_table(data, args.code, code_info))
        return

    # 解析維度篩選
    dim_filters = {}
    for i, dim_arg in enumerate([args.dim0, args.dim1, args.dim2]):
        if dim_arg:
            ids = [x.strip() for x in dim_arg.split(",")]
            dim_filters[i] = ids

    # 查詢與篩選
    result = filter_data(data, args.code, code_info, dim_filters, args.start, args.end)

    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(format_markdown(result))


if __name__ == "__main__":
    main()
