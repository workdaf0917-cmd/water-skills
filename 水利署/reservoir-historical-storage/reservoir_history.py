#!/usr/bin/env python3
"""
水利署水庫歷史蓄水量查詢工具
資料來源：水利署防汛資訊網
網址：https://fhy.wra.gov.tw/ReservoirPage_2011/StorageCapacity.aspx
"""

import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Any, Optional, Tuple
from datetime import date, timedelta
import time
import csv


class ReservoirDataError(Exception):
    """水庫資料查詢錯誤"""
    pass


# 網站 URL
BASE_URL = "https://fhy.wra.gov.tw/ReservoirPage_2011/StorageCapacity.aspx"

# 請求標頭
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
    "Content-Type": "application/x-www-form-urlencoded",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}


def parse_number(value: str) -> Optional[float]:
    """解析數值，處理 '--' 和空值"""
    if not value or value.strip() in ('--', '', '-'):
        return None
    try:
        return float(value.strip().replace(',', '').replace('%', ''))
    except ValueError:
        return None


def get_reservoir_data_by_date(
    year: int, 
    month: int, 
    day: int,
    reservoir_name: Optional[str] = None,
    search_type: str = "防汛重點水庫",
    session: Optional[requests.Session] = None
) -> List[Dict[str, Any]]:
    """
    查詢指定日期的水庫蓄水資料
    
    Args:
        year: 年份 (1970-2027)
        month: 月份 (1-12)
        day: 日期 (1-31)
        reservoir_name: 水庫名稱（可選，用於篩選特定水庫）
        search_type: 查詢類型（防汛重點水庫/所有水庫/水庫及攔河堰）
        session: requests Session 物件（可重複使用）
    
    Returns:
        水庫資料列表
    """
    if session is None:
        session = requests.Session()
    
    try:
        # 先取得初始頁面和 viewstate
        init_response = session.get(BASE_URL, headers=HEADERS, timeout=30)
        init_response.raise_for_status()
        init_soup = BeautifulSoup(init_response.text, 'html.parser')
        
        # 取得隱藏欄位
        viewstate = init_soup.find('input', {'name': '__VIEWSTATE'})
        viewstate_val = viewstate['value'] if viewstate else ''
        eventvalidation = init_soup.find('input', {'name': '__EVENTVALIDATION'})
        eventvalidation_val = eventvalidation['value'] if eventvalidation else ''
        
        # 構建 POST 資料
        data = {
            "__VIEWSTATE": viewstate_val,
            "__EVENTVALIDATION": eventvalidation_val,
            "ctl00$cphMain$cboSearch": search_type,
            "ctl00$cphMain$ucDate$cboYear": str(year),
            "ctl00$cphMain$ucDate$cboMonth": str(month),
            "ctl00$cphMain$ucDate$cboDay": str(day),
            "__EVENTTARGET": "ctl00$cphMain$btnQuery",
        }
        
        response = session.post(BASE_URL, data=data, headers=HEADERS, timeout=30)
        response.raise_for_status()
        response.encoding = 'utf-8'
    except requests.RequestException as e:
        raise ReservoirDataError(f"網路請求失敗: {e}")
    
    # 解析 HTML
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table', {'id': 'ctl00_cphMain_gvList'})
    
    if not table:
        raise ReservoirDataError(f"找不到資料表格，日期: {year}-{month:02d}-{day:02d}")
    
    results = []
    rows = table.find_all('tr')
    
    for row in rows[2:]:  # 跳過標題列
        cells = row.find_all('td')
        if len(cells) < 10:
            continue
        
        name = cells[0].get_text(strip=True)
        if name == '附註':
            continue
        
        # 篩選特定水庫
        if reservoir_name and reservoir_name not in name:
            continue
        
        record = {
            "date": f"{year}-{month:02d}-{day:02d}",
            "reservoir_name": name,
            "capacity": parse_number(cells[1].get_text(strip=True)),
            "rainfall": parse_number(cells[3].get_text(strip=True)),
            "inflow": parse_number(cells[4].get_text(strip=True)),
            "outflow": parse_number(cells[5].get_text(strip=True)),
            "level_diff": parse_number(cells[6].get_text(strip=True)),
            "water_level": parse_number(cells[8].get_text(strip=True)),
            "storage": parse_number(cells[9].get_text(strip=True)),
            "storage_percent": parse_number(cells[10].get_text(strip=True)),
        }
        results.append(record)
    
    return results


def get_reservoir_data_range(
    start_date: Tuple[int, int, int],
    end_date: Tuple[int, int, int],
    reservoir_name: Optional[str] = None,
    delay: float = 0.5
) -> List[Dict[str, Any]]:
    """
    查詢日期區間的水庫資料
    
    Args:
        start_date: 開始日期 (year, month, day)
        end_date: 結束日期 (year, month, day)
        reservoir_name: 水庫名稱
        delay: 每次請求間隔秒數
    
    Returns:
        水庫資料列表
    """
    start = date(*start_date)
    end = date(*end_date)
    
    if start > end:
        raise ValueError("開始日期不能大於結束日期")
    
    all_data = []
    current = start
    total_days = (end - start).days + 1
    processed = 0
    
    print(f"開始查詢 {reservoir_name or '所有水庫'} 從 {start} 到 {end}")
    print(f"共 {total_days} 天資料")
    
    while current <= end:
        try:
            data = get_reservoir_data_by_date(
                current.year, 
                current.month, 
                current.day,
                reservoir_name
            )
            all_data.extend(data)
            processed += 1
            
            if processed % 10 == 0:
                print(f"進度: {processed}/{total_days} ({processed*100//total_days}%)")
            
        except ReservoirDataError as e:
            print(f"警告: {current} 查詢失敗 - {e}")
        
        current += timedelta(days=1)
        time.sleep(delay)
    
    print(f"查詢完成，共取得 {len(all_data)} 筆資料")
    return all_data


def calculate_statistics(data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    計算統計數據
    
    Args:
        data: 水庫資料列表
    
    Returns:
        統計結果字典
    """
    if not data:
        return {}
    
    # 提取有效數值
    inflows = [d['inflow'] for d in data if d['inflow'] is not None]
    outflows = [d['outflow'] for d in data if d['outflow'] is not None]
    storages = [d['storage'] for d in data if d['storage'] is not None]
    rainfalls = [d['rainfall'] for d in data if d['rainfall'] is not None]
    
    stats = {
        "record_count": len(data),
        "date_range": f"{data[0]['date']} ~ {data[-1]['date']}",
    }
    
    if inflows:
        stats["inflow_avg"] = sum(inflows) / len(inflows)
        stats["inflow_max"] = max(inflows)
        stats["inflow_min"] = min(inflows)
        stats["inflow_total"] = sum(inflows)
    
    if outflows:
        stats["outflow_avg"] = sum(outflows) / len(outflows)
        stats["outflow_max"] = max(outflows)
        stats["outflow_min"] = min(outflows)
        stats["outflow_total"] = sum(outflows)
    
    if storages:
        stats["storage_avg"] = sum(storages) / len(storages)
        stats["storage_max"] = max(storages)
        stats["storage_min"] = min(storages)
    
    if rainfalls:
        stats["rainfall_avg"] = sum(rainfalls) / len(rainfalls)
        stats["rainfall_max"] = max(rainfalls)
        stats["rainfall_total"] = sum(rainfalls)
    
    return stats


def generate_monthly_report(
    year: int,
    reservoir_name: str,
    delay: float = 0.5
) -> str:
    """
    產生年度月報表
    
    Args:
        year: 年份
        reservoir_name: 水庫名稱
        delay: 請求間隔
    
    Returns:
        格式化的報表字串
    """
    report_lines = []
    report_lines.append(f"\n{'='*70}")
    report_lines.append(f"  {reservoir_name} {year}年 月統計報表")
    report_lines.append(f"{'='*70}")
    report_lines.append(f"\n{'月份':<6}{'進水量(萬m³)':<18}{'出水量(萬m³)':<18}{'平均蓄水量':<15}")
    report_lines.append(f"{'':6}{'平均/最大/最小':<18}{'平均/最大/最小':<18}{'(萬m³)':<15}")
    report_lines.append("-" * 70)
    
    yearly_inflows = []
    yearly_outflows = []
    
    for month in range(1, 13):
        # 計算該月天數
        if month == 12:
            days_in_month = 31
        else:
            next_month = date(year, month + 1, 1)
            days_in_month = (next_month - date(year, month, 1)).days
        
        try:
            data = get_reservoir_data_range(
                (year, month, 1),
                (year, month, days_in_month),
                reservoir_name,
                delay
            )
            
            if data:
                stats = calculate_statistics(data)
                
                inflow_str = f"{stats.get('inflow_avg', 0):.1f}/{stats.get('inflow_max', 0):.1f}/{stats.get('inflow_min', 0):.1f}"
                outflow_str = f"{stats.get('outflow_avg', 0):.1f}/{stats.get('outflow_max', 0):.1f}/{stats.get('outflow_min', 0):.1f}"
                storage_str = f"{stats.get('storage_avg', 0):.1f}"
                
                report_lines.append(f"{month:>2}月    {inflow_str:<18}{outflow_str:<18}{storage_str:<15}")
                
                yearly_inflows.extend([d['inflow'] for d in data if d['inflow'] is not None])
                yearly_outflows.extend([d['outflow'] for d in data if d['outflow'] is not None])
            else:
                report_lines.append(f"{month:>2}月    {'無資料':<18}{'無資料':<18}{'無資料':<15}")
                
        except Exception as e:
            report_lines.append(f"{month:>2}月    {'查詢失敗':<18}{'查詢失敗':<18}{'查詢失敗':<15}")
    
    report_lines.append("-" * 70)
    
    if yearly_inflows and yearly_outflows:
        report_lines.append(f"\n年度統計：")
        report_lines.append(f"  進水量 - 平均: {sum(yearly_inflows)/len(yearly_inflows):.2f}, "
                          f"最大: {max(yearly_inflows):.2f}, 最小: {min(yearly_inflows):.2f} 萬m³")
        report_lines.append(f"  出水量 - 平均: {sum(yearly_outflows)/len(yearly_outflows):.2f}, "
                          f"最大: {max(yearly_outflows):.2f}, 最小: {min(yearly_outflows):.2f} 萬m³")
    
    report_lines.append(f"{'='*70}\n")
    
    return "\n".join(report_lines)


def export_to_csv(
    start_date: Tuple[int, int, int],
    end_date: Tuple[int, int, int],
    reservoir_name: str,
    filename: str,
    delay: float = 0.5
):
    """
    匯出資料為 CSV 檔案
    
    Args:
        start_date: 開始日期
        end_date: 結束日期
        reservoir_name: 水庫名稱
        filename: 輸出檔名
        delay: 請求間隔
    """
    data = get_reservoir_data_range(start_date, end_date, reservoir_name, delay)
    
    if not data:
        print("無資料可匯出")
        return
    
    fieldnames = [
        'date', 'reservoir_name', 'capacity', 'rainfall', 
        'inflow', 'outflow', 'level_diff', 'water_level', 
        'storage', 'storage_percent'
    ]
    
    with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    
    print(f"已匯出 {len(data)} 筆資料至 {filename}")


def format_statistics_table(stats: Dict[str, Any], reservoir_name: str) -> str:
    """格式化統計結果為表格"""
    lines = []
    lines.append(f"\n╔{'═'*60}╗")
    lines.append(f"║  {reservoir_name} 統計報表{' '*(47-len(reservoir_name)*2)}║")
    lines.append(f"╠{'═'*60}╣")
    lines.append(f"║  資料區間: {stats.get('date_range', 'N/A'):<46}║")
    lines.append(f"║  資料筆數: {stats.get('record_count', 0):<46}║")
    lines.append(f"╠{'═'*60}╣")
    lines.append(f"║  【進水量】(萬m³/日){' '*38}║")
    lines.append(f"║    平均: {stats.get('inflow_avg', 0):>10.2f}   "
                f"最大: {stats.get('inflow_max', 0):>10.2f}   "
                f"最小: {stats.get('inflow_min', 0):>10.2f}  ║")
    lines.append(f"╠{'═'*60}╣")
    lines.append(f"║  【出水量】(萬m³/日){' '*38}║")
    lines.append(f"║    平均: {stats.get('outflow_avg', 0):>10.2f}   "
                f"最大: {stats.get('outflow_max', 0):>10.2f}   "
                f"最小: {stats.get('outflow_min', 0):>10.2f}  ║")
    lines.append(f"╠{'═'*60}╣")
    lines.append(f"║  【有效蓄水量】(萬m³){' '*37}║")
    lines.append(f"║    平均: {stats.get('storage_avg', 0):>10.2f}   "
                f"最大: {stats.get('storage_max', 0):>10.2f}   "
                f"最小: {stats.get('storage_min', 0):>10.2f}  ║")
    lines.append(f"╚{'═'*60}╝")
    return "\n".join(lines)


def main():
    """主程式 - 示範查詢阿公店水庫最近7天資料"""
    print("=" * 60)
    print("  水利署水庫歷史蓄水量查詢工具")
    print("=" * 60)
    
    # 示範：查詢最近7天阿公店水庫資料
    from datetime import date, timedelta
    
    end = date.today()
    start = end - timedelta(days=6)
    
    print(f"\n範例：查詢阿公店水庫 {start} ~ {end} 資料")
    print("-" * 50)
    
    try:
        data = get_reservoir_data_range(
            (start.year, start.month, start.day),
            (end.year, end.month, end.day),
            reservoir_name="阿公店水庫",
            delay=0.3
        )
        
        if data:
            print("\n查詢結果：")
            print(f"{'日期':<12}{'進水量':<12}{'出水量':<12}{'蓄水量':<15}{'蓄水率':<10}")
            print("-" * 60)
            
            for d in data:
                inflow = f"{d['inflow']:.2f}" if d['inflow'] else "--"
                outflow = f"{d['outflow']:.2f}" if d['outflow'] else "--"
                storage = f"{d['storage']:.2f}" if d['storage'] else "--"
                percent = f"{d['storage_percent']:.1f}%" if d['storage_percent'] else "--"
                print(f"{d['date']:<12}{inflow:<12}{outflow:<12}{storage:<15}{percent:<10}")
            
            # 計算統計
            stats = calculate_statistics(data)
            print(format_statistics_table(stats, "阿公店水庫"))
        else:
            print("無資料")
            
    except ReservoirDataError as e:
        print(f"查詢錯誤: {e}")
    except Exception as e:
        print(f"發生錯誤: {e}")


if __name__ == "__main__":
    main()
