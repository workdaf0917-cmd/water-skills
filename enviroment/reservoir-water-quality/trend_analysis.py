"""
水庫水質趨勢分析模組
Reservoir Water Quality Trend Analysis Module

此模組提供水庫水質數據的趨勢圖繪製功能
"""

import requests
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from typing import List, Dict, Any, Optional
from datetime import datetime

# --- API 設定 ---
API_KEY = "e0a736f5-a240-4a28-8ca1-d8ae7604334d"
BASE_URL = "https://data.moenv.gov.tw/api/v2/wqx_p_03"


def get_reservoir_data(
    reservoir_keyword: str,
    year: Optional[str] = None,
    show_progress: bool = True
) -> List[Dict[str, Any]]:
    """
    獲取特定水庫的水質監測資料 (自動分頁遍歷)
    
    Args:
        reservoir_keyword: 水庫英文關鍵字 (如 "A-Kung-Tien", "Fei-Tsui")
        year: 年份篩選 (如 "2024"), 可選
        show_progress: 是否顯示進度
    
    Returns:
        符合條件的水質監測資料列表
    """
    all_records = []
    offset = 0
    
    if show_progress:
        print(f"開始下載 {reservoir_keyword} 資料...")
    
    while True:
        response = requests.get(
            BASE_URL,
            params={
                "api_key": API_KEY,
                "limit": 1000,
                "offset": offset,
                "format": "json"
            },
            timeout=30
        )
        
        if response.status_code != 200:
            print(f"API 請求失敗，狀態碼：{response.status_code}")
            break
            
        data = response.json()
        if not data:
            break
        
        # 客戶端篩選
        for record in data:
            site = record.get('siteengname', '') or ''
            date = record.get('sampledate', '') or ''
            
            if reservoir_keyword in site:
                if year is None or date.startswith(year):
                    all_records.append(record)
        
        if show_progress and offset % 50000 == 0:
            print(f"  已掃描: offset={offset}, 找到 {len(all_records)} 筆")
        
        if len(data) < 1000:
            break
        offset += 1000
    
    if show_progress:
        print(f"完成！共找到 {len(all_records)} 筆資料")
    
    return all_records


def plot_trend(
    data: List[Dict[str, Any]],
    item_name: str = "Chlorophyl-A",
    title: str = None,
    save_path: str = None,
    figsize: tuple = (12, 6)
) -> None:
    """
    繪製水質監測項目的時間趨勢圖
    
    Args:
        data: 水質監測資料列表
        item_name: 監測項目英文名稱 (如 "Chlorophyl-A", "Total-Phosphate")
        title: 圖表標題 (可選)
        save_path: 儲存路徑 (可選，若提供則儲存圖片)
        figsize: 圖表大小
    """
    # 篩選特定監測項目
    item_data = [r for r in data if r.get('itemengname') == item_name]
    
    if not item_data:
        print(f"找不到 {item_name} 的資料")
        return
    
    # 轉換為 DataFrame
    df = pd.DataFrame(item_data)
    df['sampledate'] = pd.to_datetime(df['sampledate'])
    df['itemvalue'] = pd.to_numeric(df['itemvalue'], errors='coerce')
    df = df.dropna(subset=['itemvalue'])
    df = df.sort_values('sampledate')
    
    # 設定中文字型
    plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'Microsoft JhengHei', 'SimHei', 'DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False
    
    # 建立圖表
    fig, ax = plt.subplots(figsize=figsize)
    
    # 取得測站列表
    stations = df['siteengname'].unique()
    colors = plt.cm.Set1(range(len(stations)))
    
    for i, station in enumerate(stations):
        station_df = df[df['siteengname'] == station]
        station_label = station.split()[-1] if 'Reservoir' in station else station
        ax.plot(
            station_df['sampledate'], 
            station_df['itemvalue'], 
            marker='o', 
            linestyle='-', 
            color=colors[i],
            label=station_label,
            markersize=4
        )
    
    # 設定圖表
    if title:
        ax.set_title(title, fontsize=14)
    else:
        reservoir = data[0].get('damename', 'Reservoir') if data else 'Reservoir'
        ax.set_title(f'{reservoir} - {item_name} 趨勢圖', fontsize=14)
    
    ax.set_xlabel('採樣日期', fontsize=12)
    ax.set_ylabel(f'{item_name} ({item_data[0].get("itemunit", "")})', fontsize=12)
    ax.legend(loc='upper right')
    ax.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # 儲存或顯示
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"圖表已儲存至: {save_path}")
    else:
        plt.show()
    
    plt.close()


def plot_eutrophication_trends(
    data: List[Dict[str, Any]],
    reservoir_name: str = "水庫",
    save_path: str = None
) -> None:
    """
    繪製優養化相關指標的綜合趨勢圖 (CTSI, Chl-a, TP, SD)
    
    Args:
        data: 水質監測資料列表
        reservoir_name: 水庫名稱 (用於標題)
        save_path: 儲存路徑 (可選)
    """
    # 優養化指標
    eutro_items = {
        'Carlson Trophic State Index': ('CTSI', '-'),
        'Chlorophyl-A': ('Chl-a', 'μg/L'),
        'Total-Phosphate': ('TP', 'mg/L'),
        'Transparency': ('SD', 'm')
    }
    
    # 設定中文字型
    plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'Microsoft JhengHei', 'SimHei', 'DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    axes = axes.flatten()
    
    for idx, (item_eng, (item_short, unit)) in enumerate(eutro_items.items()):
        ax = axes[idx]
        item_data = [r for r in data if r.get('itemengname') == item_eng]
        
        if not item_data:
            ax.text(0.5, 0.5, f'無 {item_short} 資料', ha='center', va='center')
            ax.set_title(f'{item_short}')
            continue
        
        df = pd.DataFrame(item_data)
        df['sampledate'] = pd.to_datetime(df['sampledate'])
        df['itemvalue'] = pd.to_numeric(df['itemvalue'], errors='coerce')
        df = df.dropna(subset=['itemvalue'])
        df = df.sort_values('sampledate')
        
        # 按測站繪製
        stations = df['siteengname'].unique()
        colors = plt.cm.Set1(range(len(stations)))
        
        for i, station in enumerate(stations):
            station_df = df[df['siteengname'] == station]
            label = station.split()[-1] if 'Reservoir' in station else station
            ax.plot(
                station_df['sampledate'],
                station_df['itemvalue'],
                marker='o',
                markersize=3,
                linestyle='-',
                color=colors[i],
                label=label
            )
        
        ax.set_title(f'{item_short} ({item_eng})', fontsize=11)
        ax.set_ylabel(f'{unit}' if unit != '-' else '', fontsize=10)
        ax.legend(loc='upper right', fontsize=8)
        ax.grid(True, alpha=0.3)
        ax.tick_params(axis='x', rotation=45)
    
    fig.suptitle(f'{reservoir_name} 優養化指標趨勢圖', fontsize=14, fontweight='bold')
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"圖表已儲存至: {save_path}")
    else:
        plt.show()
    
    plt.close()


# --- 使用範例 ---
if __name__ == "__main__":
    # 範例: 繪製阿公店水庫 2024 年葉綠素a趨勢圖
    
    # 1. 獲取資料
    data = get_reservoir_data("A-Kung-Tien", "2024")
    
    if data:
        # 2. 繪製單一指標趨勢圖
        plot_trend(
            data,
            item_name="Chlorophyl-A",
            title="阿公店水庫 2024年 葉綠素a (Chl-a) 趨勢圖",
            save_path="akung_2024_chla_trend.png"
        )
        
        # 3. 繪製優養化綜合趨勢圖
        plot_eutrophication_trends(
            data,
            reservoir_name="阿公店水庫 2024年",
            save_path="akung_2024_eutro_trends.png"
        )
