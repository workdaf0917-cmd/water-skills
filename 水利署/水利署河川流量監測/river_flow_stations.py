#!/usr/bin/env python3
"""
水利署河川流量測站查詢工具
資料來源：經濟部水利署開放資料平台
API 端點：https://opendata.wra.gov.tw/api/v2/9332bd66-0213-4380-a5d5-a43e7be49255
"""

import requests
from typing import List, Dict, Any, Optional


# API 常數
FLOW_STATION_API_URL = "https://opendata.wra.gov.tw/api/v2/9332bd66-0213-4380-a5d5-a43e7be49255"
REALTIME_LEVEL_API_URL = "https://opendata.wra.gov.tw/api/v2/73c4c3de-4045-4765-abeb-89f9f9cd5ff0"


def get_all_stations() -> List[Dict[str, Any]]:
    """
    獲取所有河川流量測站資料
    
    Returns:
        測站資料列表
    """
    try:
        response = requests.get(
            FLOW_STATION_API_URL,
            params={"size": 1000},
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"API 請求錯誤: {e}")
        return []


def search_by_river(river_name: str) -> List[Dict[str, Any]]:
    """
    依河川名稱搜尋測站
    
    Args:
        river_name: 河川名稱關鍵字
    
    Returns:
        符合條件的測站列表
    """
    stations = get_all_stations()
    return [s for s in stations if river_name in s.get('rivername', '')]


def search_by_location(keyword: str) -> List[Dict[str, Any]]:
    """
    依地址關鍵字搜尋測站
    
    Args:
        keyword: 地址關鍵字（如縣市名稱）
    
    Returns:
        符合條件的測站列表
    """
    stations = get_all_stations()
    return [s for s in stations if keyword in s.get('locationaddress', '')]


def get_stations_with_alert() -> List[Dict[str, Any]]:
    """
    獲取有設定警戒水位的測站
    
    Returns:
        有警戒水位設定的測站列表
    """
    stations = get_all_stations()
    return [s for s in stations 
            if s.get('alertlevel1') or s.get('alertlevel2') or s.get('alertlevel3')]


def get_active_stations() -> List[Dict[str, Any]]:
    """
    獲取現存（運作中）的測站
    
    Returns:
        現存測站列表
    """
    stations = get_all_stations()
    return [s for s in stations if s.get('observationstatus') == '現存']


def get_realtime_water_levels(station_id: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    獲取即時水位資料
    
    Args:
        station_id: 測站代碼（選填），如 "1660H009"
    
    Returns:
        即時水位資料列表
    """
    try:
        response = requests.get(
            REALTIME_LEVEL_API_URL,
            params={"size": 1000},
            timeout=30
        )
        response.raise_for_status()
        data = response.json()
        
        if station_id:
            data = [d for d in data if station_id in d.get('stationid', '')]
        
        return data
    except requests.RequestException as e:
        print(f"API 請求錯誤: {e}")
        return []


def get_river_realtime_levels(river_name: str) -> List[Dict[str, Any]]:
    """
    獲取特定河川的即時水位（結合測站資料）
    
    Args:
        river_name: 河川名稱關鍵字
    
    Returns:
        包含測站名稱和即時水位的列表
    """
    # 獲取測站基本資料
    stations = get_all_stations()
    river_stations = {s['basinidentifier']: s for s in stations 
                      if river_name in s.get('rivername', '')}
    
    # 獲取即時水位
    levels = get_realtime_water_levels()
    
    # 結合資料
    results = []
    for level in levels:
        station_id = level.get('stationid', '')
        if station_id in river_stations:
            station = river_stations[station_id]
            results.append({
                "測站名稱": station.get('observatoryname'),
                "站號": station_id,
                "河川": station.get('rivername'),
                "地址": station.get('locationaddress'),
                "時間": level.get('datetime'),
                "水位_m": float(level.get('waterlevel', 0))
            })
    
    return results


def get_area_realtime_levels(area_keyword: str) -> List[Dict[str, Any]]:
    """
    獲取特定地區的即時水位
    
    Args:
        area_keyword: 地址關鍵字（如縣市名稱）
    
    Returns:
        包含測站名稱和即時水位的列表
    """
    # 獲取測站基本資料
    stations = get_all_stations()
    area_stations = {s['basinidentifier']: s for s in stations 
                     if area_keyword in s.get('locationaddress', '')}
    
    # 獲取即時水位
    levels = get_realtime_water_levels()
    
    # 結合資料
    results = []
    for level in levels:
        station_id = level.get('stationid', '')
        if station_id in area_stations:
            station = area_stations[station_id]
            results.append({
                "測站名稱": station.get('observatoryname'),
                "站號": station_id,
                "河川": station.get('rivername'),
                "地址": station.get('locationaddress'),
                "時間": level.get('datetime'),
                "水位_m": float(level.get('waterlevel', 0))
            })
    
    return results


def format_station_info(station: Dict[str, Any]) -> str:
    """
    格式化測站資訊
    
    Args:
        station: 測站資料字典
    
    Returns:
        格式化的資訊字串
    """
    info = f"""
╔══════════════════════════════════════════════════════════╗
║  測站名稱：{station.get('observatoryname', 'N/A')}
║  英文名稱：{station.get('englishname', 'N/A')}
╠══════════════════════════════════════════════════════════╣
║  河川名稱：{station.get('rivername', 'N/A')} ({station.get('englishrivername', '')})
║  流域代碼：{station.get('affiliatedbasin', 'N/A')}
║  測站地址：{station.get('locationaddress', 'N/A')}
║  TWD97座標：{station.get('locationbytwd97_xy', 'N/A')}
╠══════════════════════════════════════════════════════════╣
║  水尺零點標高：{station.get('elevationofwaterlevelzeropoint', 'N/A')} m
║  集水區面積：{station.get('watershedarea', 'N/A')} km²
║  觀測項目：{_parse_observation_items(station.get('obervationitems', ''))}
║  設備狀態：{_parse_equipment_status(station.get('equipmentstatus', ''))}
║  觀測現況：{station.get('observationstatus', 'N/A')}
"""
    
    # 警戒水位
    if station.get('alertlevel1') or station.get('alertlevel2') or station.get('alertlevel3'):
        info += "╠══════════════════════════════════════════════════════════╣\n"
        info += "║  【警戒水位】\n"
        if station.get('alertlevel1'):
            info += f"║    一級警戒：{station['alertlevel1']} m\n"
        if station.get('alertlevel2'):
            info += f"║    二級警戒：{station['alertlevel2']} m\n"
        if station.get('alertlevel3'):
            info += f"║    三級警戒：{station['alertlevel3']} m\n"
    
    info += "╚══════════════════════════════════════════════════════════╝"
    return info


def _parse_observation_items(code: str) -> str:
    """解析觀測項目代碼"""
    items = []
    if '0' in code:
        items.append('水位')
    if '1' in code:
        items.append('流量')
    return '、'.join(items) if items else 'N/A'


def _parse_equipment_status(code: str) -> str:
    """解析設備狀態代碼"""
    status_map = {
        '1': '正常',
        '2': '故障',
        '3': '維修中'
    }
    return status_map.get(code, f'未知({code})')


def print_summary():
    """列印測站統計摘要"""
    stations = get_all_stations()
    active = [s for s in stations if s.get('observationstatus') == '現存']
    with_alert = get_stations_with_alert()
    
    # 統計各河川測站數量
    river_counts = {}
    for s in active:
        river = s.get('rivername', '未知')
        river_counts[river] = river_counts.get(river, 0) + 1
    
    # 排序取前10
    top_rivers = sorted(river_counts.items(), key=lambda x: x[1], reverse=True)[:10]
    
    print("=" * 60)
    print("        水利署河川流量測站統計摘要")
    print("=" * 60)
    print(f"\n📊 測站總數：{len(stations)} 站")
    print(f"✅ 現存測站：{len(active)} 站")
    print(f"⚠️ 有警戒水位設定：{len(with_alert)} 站")
    
    print("\n📍 各河川測站數量 (前10名)：")
    for river, count in top_rivers:
        print(f"   {river}: {count} 站")
    
    print("\n" + "=" * 60)


def main():
    """主程式"""
    print("正在查詢水利署河川流量測站資料...")
    print("-" * 50)
    
    # 列印統計摘要
    print_summary()
    
    # 範例：查詢特定河川的測站
    print("\n🔍 範例查詢：淡水河流域測站")
    print("-" * 40)
    
    tamsui_stations = search_by_river("淡水河")
    if tamsui_stations:
        for s in tamsui_stations[:3]:
            print(f"  • {s['observatoryname']} - {s['locationaddress']}")
        if len(tamsui_stations) > 3:
            print(f"  ... 共 {len(tamsui_stations)} 個測站")
    
    # 即時水位查詢範例
    print("\n" + "=" * 60)
    print("        即時水位資料查詢")
    print("=" * 60)
    
    # 查詢二仁溪即時水位（阿公店水庫鄰近區域）
    print("\n📊 二仁溪流域即時水位（阿公店水庫鄰近）：")
    print("-" * 40)
    
    erren_levels = get_river_realtime_levels("二仁溪")
    if erren_levels:
        for l in erren_levels:
            print(f"【{l['測站名稱']}】{l['河川']}")
            print(f"  地址: {l['地址']}")
            print(f"  時間: {l['時間']}")
            print(f"  水位: {l['水位_m']:.2f} m")
            print()
    else:
        print("  無即時水位資料")
    
    # 查詢高雄地區即時水位
    print("\n📊 高雄地區即時水位：")
    print("-" * 40)
    
    kaohsiung_levels = get_area_realtime_levels("高雄")
    if kaohsiung_levels:
        for l in kaohsiung_levels[:5]:
            print(f"【{l['測站名稱']}】{l['河川']} - {l['水位_m']:.2f} m ({l['時間']})")
        if len(kaohsiung_levels) > 5:
            print(f"  ... 共 {len(kaohsiung_levels)} 個測站有即時資料")


if __name__ == "__main__":
    main()
