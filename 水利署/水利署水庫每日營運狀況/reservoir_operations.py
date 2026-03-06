#!/usr/bin/env python3
"""
水利署水庫每日營運狀況查詢工具
資料來源：經濟部水利署開放資料平台
API 端點：https://opendata.wra.gov.tw/api/v2/51023e88-4c76-4dbc-bbb9-470da690d539
"""

import requests
from typing import List, Dict, Any, Optional


# API 常數
RESERVOIR_OPERATION_API_URL = "https://opendata.wra.gov.tw/api/v2/51023e88-4c76-4dbc-bbb9-470da690d539"


def get_all_operations() -> List[Dict[str, Any]]:
    """
    獲取所有水庫每日營運狀況
    
    Returns:
        水庫營運資料列表
    """
    try:
        response = requests.get(
            RESERVOIR_OPERATION_API_URL,
            params={"size": 1000},
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"API 請求錯誤: {e}")
        return []


def get_reservoir_operation(reservoir_name: str) -> Optional[Dict[str, Any]]:
    """
    查詢特定水庫的營運狀況
    
    Args:
        reservoir_name: 水庫名稱關鍵字
    
    Returns:
        水庫營運資料，找不到則返回 None
    """
    operations = get_all_operations()
    for op in operations:
        if reservoir_name in op.get('reservoirname', ''):
            return op
    return None


def get_top_reservoirs_by_capacity(top_n: int = 10) -> List[Dict[str, Any]]:
    """
    獲取蓄水量最大的水庫
    
    Args:
        top_n: 返回前幾名
    
    Returns:
        蓄水量最大的水庫列表
    """
    operations = get_all_operations()
    with_capacity = [d for d in operations 
                     if d.get('capacity') and d['capacity'] != '']
    sorted_data = sorted(with_capacity, 
                        key=lambda x: float(x['capacity']), 
                        reverse=True)
    return sorted_data[:top_n]


def get_reservoirs_with_rainfall() -> List[Dict[str, Any]]:
    """
    獲取集水區有降雨的水庫
    
    Returns:
        有降雨的水庫列表
    """
    operations = get_all_operations()
    return [d for d in operations 
            if d.get('basinrainfall') and float(d.get('basinrainfall', 0)) > 0]


def get_reservoirs_with_inflow() -> List[Dict[str, Any]]:
    """
    獲取有入流量的水庫
    
    Returns:
        有入流量的水庫列表
    """
    operations = get_all_operations()
    return [d for d in operations 
            if d.get('inflow') and float(d.get('inflow', 0)) > 0]


def format_operation_info(op: Dict[str, Any]) -> str:
    """
    格式化水庫營運資訊
    
    Args:
        op: 水庫營運資料字典
    
    Returns:
        格式化的資訊字串
    """
    capacity = op.get('capacity', '')
    capacity_str = f"{float(capacity):,.2f} 萬m³" if capacity else 'N/A'
    
    inflow = op.get('inflow', '')
    inflow_str = f"{float(inflow):,.2f} 萬m³/日" if inflow else 'N/A'
    
    outflow = op.get('outflow', '')
    outflow_str = f"{float(outflow):,.2f} 萬m³/日" if outflow else 'N/A'
    
    info = f"""
╔══════════════════════════════════════════════════════════╗
║  水庫名稱：{op.get('reservoirname', 'N/A')}
║  水庫代碼：{op.get('reservoiridentifier', 'N/A')}
╠══════════════════════════════════════════════════════════╣
║  資料日期：{op.get('datetime', 'N/A')}
╠══════════════════════════════════════════════════════════╣
║  【蓄水資訊】
║    蓄水容量：{capacity_str}
║    呆水位：{op.get('dwl', 'N/A')} m
║    最高正常蓄水位：{op.get('nwlmax', 'N/A')} m
╠══════════════════════════════════════════════════════════╣
║  【流量資訊】
║    入流量：{inflow_str}
║    出流量：{outflow_str}
║    總出流量：{op.get('outflowtotal', 'N/A')} 萬m³/日
║    越域引水量：{op.get('crossflow', 'N/A')} 萬m³/日
╠══════════════════════════════════════════════════════════╣
║  【降雨資訊】
║    集水區降雨量：{op.get('basinrainfall', 'N/A')} mm
╚══════════════════════════════════════════════════════════╝"""
    return info


def print_summary():
    """列印水庫營運摘要"""
    operations = get_all_operations()
    
    # 統計
    with_capacity = [d for d in operations 
                     if d.get('capacity') and d['capacity'] != '']
    with_rainfall = get_reservoirs_with_rainfall()
    with_inflow = get_reservoirs_with_inflow()
    
    print("=" * 60)
    print("        水利署水庫每日營運狀況摘要")
    print("=" * 60)
    print(f"\n📊 水庫/堰壩總數：{len(operations)} 座")
    print(f"💧 有蓄水量資料：{len(with_capacity)} 座")
    print(f"🌧️ 集水區有降雨：{len(with_rainfall)} 座")
    print(f"📥 有入流量：{len(with_inflow)} 座")
    
    # 蓄水量前5大
    if with_capacity:
        print("\n📈 蓄水量前5大水庫：")
        top5 = get_top_reservoirs_by_capacity(5)
        for i, r in enumerate(top5, 1):
            capacity = float(r['capacity'])
            print(f"   {i}. {r['reservoirname']}: {capacity:,.2f} 萬m³")
    
    print("\n" + "=" * 60)


def main():
    """主程式"""
    print("正在查詢水利署水庫每日營運狀況...")
    print("-" * 50)
    
    # 列印統計摘要
    print_summary()
    
    # 範例：查詢阿公店水庫
    print("\n🔍 範例查詢：阿公店水庫")
    print("-" * 40)
    
    agongdian = get_reservoir_operation("阿公店")
    if agongdian:
        print(format_operation_info(agongdian))
    else:
        print("  未找到阿公店水庫資料")
    
    # 範例：查詢曾文水庫
    print("\n🔍 範例查詢：曾文水庫")
    print("-" * 40)
    
    zengwen = get_reservoir_operation("曾文")
    if zengwen:
        print(format_operation_info(zengwen))
    else:
        print("  未找到曾文水庫資料")
    
    # 查詢有降雨的水庫
    print("\n🌧️ 集水區有降雨的水庫：")
    print("-" * 40)
    
    rainy = get_reservoirs_with_rainfall()
    if rainy:
        for r in rainy[:5]:
            print(f"  - {r['reservoirname']}: {r['basinrainfall']} mm")
        if len(rainy) > 5:
            print(f"  ... 共 {len(rainy)} 座")
    else:
        print("  目前無水庫集水區有降雨")


if __name__ == "__main__":
    main()
