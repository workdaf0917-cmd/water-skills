#!/usr/bin/env python3
"""
總體統計資料庫 - 每人每月總薪資查詢腳本
功能代碼: A046201010

用法:
  python query_nstat.py --industry 1 --gender 1 --start 2024-M1 --end 2024-M12
  python query_nstat.py --list-industries
  python query_nstat.py --industry 22 --gender 1 --start 2020 --end 2024 --format json
"""

import json
import sys
import argparse

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

API_URL = "https://nstatdb.dgbas.gov.tw/dgbasAll/webMain.aspx?sdmx/A046201010"


def fetch_dataset():
    """下載完整 A046201010 資料集"""
    if not HAS_REQUESTS:
        print(json.dumps({
            "error": "缺少 requests 套件，請執行: pip install requests",
            "fallback": "可手動於瀏覽器開啟以下網址下載 JSON：",
            "url": API_URL
        }, ensure_ascii=False, indent=2))
        sys.exit(1)

    try:
        resp = requests.get(API_URL, timeout=60)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.Timeout:
        print(json.dumps({"error": "API 請求逾時（60秒），請稍後再試"}, ensure_ascii=False, indent=2))
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(json.dumps({"error": f"API 請求失敗: {str(e)}"}, ensure_ascii=False, indent=2))
        sys.exit(1)
    except json.JSONDecodeError:
        print(json.dumps({"error": "API 回應非 JSON 格式"}, ensure_ascii=False, indent=2))
        sys.exit(1)


def parse_structure(data):
    """解析 API-JSON 結構，回傳維度與時間期對照表"""
    structure = data.get("data", {}).get("structure", {})
    dimensions = structure.get("dimensions", {})

    # 產業別與性別
    series_dims = dimensions.get("series", [])
    industry_map = {}
    gender_map = {}
    for dim in series_dims:
        if dim.get("keyPosition") == 0:
            for v in dim.get("values", []):
                industry_map[v["id"]] = v["name"]
        elif dim.get("keyPosition") == 1:
            for v in dim.get("values", []):
                gender_map[v["id"]] = v["name"]

    # 統計期
    obs_dims = dimensions.get("observation", [])
    time_map = {}
    for o in obs_dims:
        for idx, v in enumerate(o.get("values", [])):
            time_map[str(idx)] = {"id": v["id"], "name": v["name"]}

    return industry_map, gender_map, time_map


def filter_data(data, industry_id, gender_id, start_time, end_time):
    """篩選指定產業、性別、時間範圍的薪資數據"""
    industry_map, gender_map, time_map = parse_structure(data)

    # 產業別 index (0-based): id=1 → index=0, id=2 → index=1, ...
    industry_ids = sorted(industry_map.keys(), key=lambda x: int(x))
    gender_ids = sorted(gender_map.keys(), key=lambda x: int(x))

    try:
        ind_idx = industry_ids.index(str(industry_id))
    except ValueError:
        return {"error": f"找不到產業別 id={industry_id}，請用 --list-industries 查看可用選項"}

    try:
        gen_idx = gender_ids.index(str(gender_id))
    except ValueError:
        return {"error": f"找不到性別 id={gender_id}，可用值: 1=合計, 2=男, 3=女"}

    series_key = f"{ind_idx}:{gen_idx}"
    datasets = data.get("data", {}).get("dataSets", [])
    if not datasets:
        return {"error": "API 回應無資料集"}

    series = datasets[0].get("series", {})
    if series_key not in series:
        return {"error": f"找不到 series key={series_key}"}

    observations = series[series_key].get("observations", {})

    # 篩選時間範圍
    results = []
    for obs_idx, values in observations.items():
        time_info = time_map.get(obs_idx, {})
        time_id = time_info.get("id", "")
        time_name = time_info.get("name", "")

        if not time_id:
            continue

        # 時間範圍比對
        if start_time and not _time_in_range(time_id, start_time, end_time):
            continue

        salary = values[0] if values else None
        if salary is not None:
            results.append({
                "period_id": time_id,
                "period_name": time_name,
                "salary": salary
            })

    # 排序（按正規化時間排序，確保月份正確排列）
    def sort_key(item):
        pid = item["period_id"]
        if "-M" in pid:
            parts = pid.split("-M")
            return (parts[0], int(parts[1]))
        elif "-Q" in pid:
            parts = pid.split("-Q")
            return (parts[0], int(parts[1]))
        else:
            return (pid, 0)
    results.sort(key=sort_key)

    return {
        "function_code": "A046201010",
        "table_name": "每人每月總薪資",
        "industry": industry_map.get(str(industry_id), f"id={industry_id}"),
        "gender": gender_map.get(str(gender_id), f"id={gender_id}"),
        "unit": "新台幣元",
        "record_count": len(results),
        "data": results
    }


def _time_in_range(time_id, start_time, end_time):
    """檢查 time_id 是否在 start ~ end 範圍內"""
    def normalize(t):
        # 將 2024-M1 → 2024-01, 2024-Q1 → 2024-Q1, 2024 → 2024
        if "-M" in t:
            parts = t.split("-M")
            return f"{parts[0]}-{int(parts[1]):02d}"
        return t

    norm_id = normalize(time_id)
    norm_start = normalize(start_time) if start_time else ""
    norm_end = normalize(end_time) if end_time else "9999"

    # 年資料 vs 月資料判斷
    if "-" in norm_start and "-" not in norm_id:
        return False  # start 是月資料但 time_id 是年資料
    if "-" not in norm_start and "-" in norm_id:
        return False  # start 是年資料但 time_id 是月資料

    return norm_start <= norm_id <= norm_end


def list_industries(data):
    """列出所有可用產業別"""
    industry_map, _, _ = parse_structure(data)
    result = []
    for k in sorted(industry_map.keys(), key=lambda x: int(x)):
        result.append({"id": int(k), "name": industry_map[k]})
    return {"industries": result, "total": len(result)}


def format_markdown(result):
    """將查詢結果格式化為 Markdown 表格"""
    if "error" in result:
        return f"**錯誤**: {result['error']}"

    lines = []
    lines.append(f"## {result['table_name']}")
    lines.append(f"- **產業別**: {result['industry']}")
    lines.append(f"- **性別**: {result['gender']}")
    lines.append(f"- **單位**: {result['unit']}")
    lines.append(f"- **筆數**: {result['record_count']}")
    lines.append("")
    lines.append("| 統計期 | 每人每月總薪資 (NT$) |")
    lines.append("|--------|---------------------|")
    for d in result["data"]:
        salary_str = f"{d['salary']:,.0f}" if d['salary'] else "—"
        lines.append(f"| {d['period_name']} | {salary_str} |")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="查詢總體統計資料庫 A046201010 每人每月總薪資")
    parser.add_argument("--industry", type=int, help="產業別 id (1=工業及服務業, 4=製造業, ...)")
    parser.add_argument("--gender", type=int, default=1, help="性別 id (1=合計, 2=男, 3=女)")
    parser.add_argument("--start", type=str, help="開始時間 (如 2024, 2024-M1)")
    parser.add_argument("--end", type=str, help="結束時間 (如 2024, 2024-M12)")
    parser.add_argument("--format", choices=["json", "markdown"], default="markdown", help="輸出格式")
    parser.add_argument("--list-industries", action="store_true", help="列出所有可用產業別")

    args = parser.parse_args()

    # 下載資料
    data = fetch_dataset()

    if args.list_industries:
        result = list_industries(data)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    if args.industry is None:
        parser.error("請指定 --industry 或使用 --list-industries 查看可用產業別")

    result = filter_data(data, args.industry, args.gender, args.start, args.end)

    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(format_markdown(result))


if __name__ == "__main__":
    main()
