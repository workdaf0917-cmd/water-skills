#!/usr/bin/env python3
"""
水利署水資源物聯網（IoW）集水區雨量查詢工具
資料來源：經濟部水利署水資源物聯網入口網
API 端點：https://iot.wra.gov.tw/precipitation/basins
資料內容：全台約 352 個測站即時時雨量

使用前請先設定環境變數 WRA_IOW_TOKEN（JWT Bearer Token）。
帳號申請：https://iot.wra.gov.tw/ （需申請高階會員）
"""

import os
import requests
from typing import Optional, List, Dict, Any


# API 常數
WRA_IOW_BASE_URL = "https://iot.wra.gov.tw"
PRECIPITATION_BASINS_URL = f"{WRA_IOW_BASE_URL}/precipitation/basins"
RIVER_BASINS_URL = f"{WRA_IOW_BASE_URL}/river/basins"

# 阿公店水庫集水區鄉鎮
AGONGDIAN_TOWNS = ["燕巢區", "田寮區"]
AGONGDIAN_NEARBY_TOWNS = ["岡山區", "阿蓮區", "橋頭區", "大社區"]


def _get_token(token: Optional[str] = None) -> str:
    """取得 JWT Token，優先使用傳入值，其次環境變數"""
    if token:
        return token
    t = os.environ.get("WRA_IOW_TOKEN")
    if not t:
        raise ValueError(
            "請設定環境變數 WRA_IOW_TOKEN 或傳入 token 參數。\n"
            "帳號申請：https://iot.wra.gov.tw/"
        )
    return t


def get_all_basin_rainfall(
    token: Optional[str] = None,
) -> Optional[List[Dict[str, Any]]]:
    """
    查詢全台集水區時雨量（約 352 個測站）。

    Args:
        token: JWT Bearer Token

    Returns:
        測站時雨量資料列表
    """
    t = _get_token(token)

    try:
        response = requests.get(
            PRECIPITATION_BASINS_URL,
            headers={"Authorization": f"Bearer {t}"},
            timeout=30,
        )

        if response.status_code == 401:
            print("認證失敗：Token 可能已過期，請重新登入取得新 Token。")
            return None

        response.raise_for_status()
        data = response.json()

        results = []
        for s in data:
            measurements = s.get("Measurements", [])
            m = measurements[0] if measurements else {}

            results.append({
                "測站名稱": s.get("Name"),
                "StationId": s.get("StationId"),
                "縣市": s.get("CountyName"),
                "鄉鎮區": s.get("TownName"),
                "緯度": s.get("Latitude"),
                "經度": s.get("Longtiude"),  # API 原始拼寫
                "觀測時間": m.get("TimeStamp"),
                "時雨量_mm": m.get("Value"),
            })

        return results

    except requests.RequestException as e:
        print(f"API 請求錯誤: {e}")
        return None
    except (ValueError, KeyError) as e:
        print(f"資料解析錯誤: {e}")
        return None


def get_county_rainfall(
    county_name: str = "高雄市",
    token: Optional[str] = None,
) -> Optional[List[Dict[str, Any]]]:
    """
    查詢指定縣市的集水區時雨量。

    Args:
        county_name: 縣市名稱，如 "高雄市"、"臺南市"
        token: JWT Bearer Token

    Returns:
        該縣市測站時雨量資料列表
    """
    all_data = get_all_basin_rainfall(token)
    if all_data is None:
        return None

    return [s for s in all_data if s.get("縣市") == county_name]


def get_agongdian_basin_rainfall(
    include_nearby: bool = True,
    token: Optional[str] = None,
) -> Optional[List[Dict[str, Any]]]:
    """
    查詢阿公店水庫集水區及鄰近測站的時雨量。

    Args:
        include_nearby: 是否包含鄰近鄉鎮（岡山、阿蓮、橋頭、大社）
        token: JWT Bearer Token

    Returns:
        集水區測站時雨量資料列表
    """
    all_data = get_all_basin_rainfall(token)
    if all_data is None:
        return None

    target_towns = AGONGDIAN_TOWNS.copy()
    if include_nearby:
        target_towns.extend(AGONGDIAN_NEARBY_TOWNS)

    return [
        s for s in all_data
        if s.get("縣市") == "高雄市" and s.get("鄉鎮區") in target_towns
    ]


def get_river_basins() -> Optional[List[Dict[str, str]]]:
    """
    查詢水系列表（免驗證）。

    Returns:
        水系列表 [{"Code": "167000", "Name": "阿公店溪"}, ...]
    """
    try:
        response = requests.get(RIVER_BASINS_URL, timeout=15)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"API 請求錯誤: {e}")
        return None


def format_rainfall_report(results: List[Dict[str, Any]], title: str = "集水區時雨量") -> str:
    """
    將時雨量查詢結果格式化為報告字串。

    Args:
        results: 測站時雨量資料列表
        title: 報告標題

    Returns:
        格式化報告字串
    """
    if not results:
        return "無雨量資料"

    lines = []
    lines.append("═" * 60)
    lines.append(f"  {title}")
    lines.append("═" * 60)

    # 按縣市分組
    by_county: Dict[str, List[Dict]] = {}
    for r in results:
        county = r.get("縣市", "未知")
        if county not in by_county:
            by_county[county] = []
        by_county[county].append(r)

    for county, stations in by_county.items():
        lines.append(f"\n  【{county}】")
        lines.append("  " + "─" * 50)

        total = 0.0
        for s in stations:
            val = s.get("時雨量_mm", 0) or 0
            total += val
            ts = s.get("觀測時間", "N/A")
            if ts and len(ts) > 19:
                ts = ts[:19]  # 截短 ISO 時間
            lines.append(f"    {s.get('鄉鎮區', ''):8s} | {ts} | {val:6.2f} mm")

        lines.append("  " + "─" * 50)
        lines.append(f"    區域合計: {total:.2f} mm | 測站數: {len(stations)}")

    lines.append("\n" + "═" * 60)
    return "\n".join(lines)


def main():
    """主程式：查詢阿公店水庫集水區時雨量"""
    print("正在查詢阿公店水庫集水區時雨量...")

    try:
        results = get_agongdian_basin_rainfall()
        if results:
            print(format_rainfall_report(results, "阿公店水庫集水區時雨量"))
        else:
            print("無法取得雨量資料。")
            print("可能原因：")
            print("  1. Token 已過期（有效期約 30 分鐘）")
            print("  2. 未設定環境變數 WRA_IOW_TOKEN")
            print("  3. 帳號非高階會員")
    except ValueError as e:
        print(f"錯誤: {e}")


if __name__ == "__main__":
    main()
