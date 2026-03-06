#!/usr/bin/env python3
"""
阿公店水庫即時水情查詢工具
資料來源：經濟部水利署開放資料平台
API 端點：https://opendata.wra.gov.tw/api/v2/ecc4ce8d-0942-474a-8705-53e9aaa7c4e8
"""

import requests
from datetime import datetime
from typing import Optional, List, Dict, Any


# API 常數
AGONGDIAN_API_URL = "https://opendata.wra.gov.tw/api/v2/ecc4ce8d-0942-474a-8705-53e9aaa7c4e8"
RESERVOIR_NAME = "阿公店水庫"
RESERVOIR_CODE = "30802"


def get_realtime_water_info() -> Optional[Dict[str, Any]]:
    """
    獲取阿公店水庫最新即時水情
    
    Returns:
        包含水情資訊的字典，或 None（如果請求失敗）
    """
    try:
        response = requests.get(
            AGONGDIAN_API_URL,
            params={"size": 1},
            timeout=10
        )
        response.raise_for_status()
        
        data = response.json()
        if data and len(data) > 0:
            latest = data[0]
            return {
                "水庫名稱": latest.get("reservoirname", RESERVOIR_NAME),
                "水庫代碼": latest.get("reservoiridentifier", RESERVOIR_CODE),
                "觀測時間": latest.get("datetime"),
                "水位_公尺": float(latest.get("waterlevel", 0)),
                "有效蓄水量_萬立方公尺": float(latest.get("effectivewaterstoragecapacity", 0)),
                "時雨量_mm": float(latest.get("precipitationhourly", 0)),
                "本日累積雨量_mm": float(latest.get("basinrainfall", 0))
            }
        return None
        
    except requests.RequestException as e:
        print(f"API 請求錯誤: {e}")
        return None
    except (ValueError, KeyError) as e:
        print(f"資料解析錯誤: {e}")
        return None


def get_history_data(hours: int = 24) -> List[Dict[str, Any]]:
    """
    獲取阿公店水庫歷史水情資料
    
    Args:
        hours: 要獲取的小時數（最多1000筆）
    
    Returns:
        水情資料列表
    """
    try:
        response = requests.get(
            AGONGDIAN_API_URL,
            params={"size": min(hours, 1000)},
            timeout=30
        )
        response.raise_for_status()
        
        data = response.json()
        results = []
        
        for record in data:
            results.append({
                "datetime": record.get("datetime"),
                "waterlevel": float(record.get("waterlevel", 0)),
                "storage": float(record.get("effectivewaterstoragecapacity", 0)),
                "hourly_rain": float(record.get("precipitationhourly", 0)),
                "daily_rain": float(record.get("basinrainfall", 0))
            })
        
        # 按時間排序（由舊到新）
        results.sort(key=lambda x: x["datetime"])
        return results
        
    except requests.RequestException as e:
        print(f"API 請求錯誤: {e}")
        return []


def format_water_report(info: Dict[str, Any]) -> str:
    """
    格式化水情報告
    
    Args:
        info: 水情資訊字典
    
    Returns:
        格式化的報告字串
    """
    if not info:
        return "無法取得水情資料"
    
    report = f"""
╔══════════════════════════════════════════════╗
║          {info['水庫名稱']} 即時水情          ║
╠══════════════════════════════════════════════╣
║  觀測時間：{info['觀測時間']}
║  ──────────────────────────────────────────
║  📊 水位：{info['水位_公尺']:.2f} 公尺
║  💧 有效蓄水量：{info['有效蓄水量_萬立方公尺']:.0f} 萬立方公尺
║  🌧️ 時雨量：{info['時雨量_mm']:.1f} mm
║  ☔ 本日累積雨量：{info['本日累積雨量_mm']:.1f} mm
╚══════════════════════════════════════════════╝
"""
    return report


def main():
    """主程式"""
    print("正在查詢阿公店水庫即時水情...")
    print("-" * 50)
    
    # 獲取即時水情
    info = get_realtime_water_info()
    
    if info:
        print(format_water_report(info))
        
        # 顯示簡要統計
        print("\n📈 最近24小時水情趨勢：")
        history = get_history_data(24)
        
        if history:
            water_levels = [h["waterlevel"] for h in history]
            storages = [h["storage"] for h in history]
            total_rain = sum(h["hourly_rain"] for h in history)
            
            print(f"  水位範圍：{min(water_levels):.2f} ~ {max(water_levels):.2f} 公尺")
            print(f"  蓄水量範圍：{min(storages):.0f} ~ {max(storages):.0f} 萬立方公尺")
            print(f"  24小時累積雨量：{total_rain:.1f} mm")
    else:
        print("❌ 無法取得水情資料，請稍後再試")


if __name__ == "__main__":
    main()
