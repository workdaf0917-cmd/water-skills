"""
曾文水庫 2024年水質數據分析
Tseng-Wen Reservoir Water Quality Analysis 2024
"""

import json
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import numpy as np

# 設定中文字型
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'Heiti TC', 'PingFang TC', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 載入數據
with open('/tmp/reservoir_2024.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 篩選曾文水庫數據
tsengwen = [r for r in data if 'Tseng-Wen' in r.get('siteengname', '')]

# 轉換為 DataFrame
df = pd.DataFrame(tsengwen)
df['sampledate'] = pd.to_datetime(df['sampledate'])
df['month'] = df['sampledate'].dt.strftime('%Y-%m')

# 將數值轉換為浮點數（處理 '-' 或空值）
def safe_float(x):
    try:
        if x == '-' or x == '' or x is None:
            return np.nan
        return float(x)
    except:
        return np.nan

df['value'] = df['itemvalue'].apply(safe_float)

# === 1. TOC 和 COD 數據表 ===
print("=" * 60)
print("曾文水庫 2024年 TOC/COD 水質數據表")
print("=" * 60)

toc_cod = df[df['itemengname'].isin(['Total Organic Carbon', 'Chemical Oxygen Demand'])]
toc_cod_pivot = toc_cod.pivot_table(
    index='month',
    columns='itemengname',
    values='value',
    aggfunc='mean'
).round(2)

toc_cod_pivot.columns = ['COD (mg/L)', 'TOC (mg/L)']
print("\n月平均值:")
print(toc_cod_pivot.to_string())

# === 2. 優養化指標數據表 ===
print("\n" + "=" * 60)
print("曾文水庫 2024年 優養化指標數據表")
print("=" * 60)

eutro_items = ['Carlson Trophic State Index', 'Chlorophyl-A', 'Total-Phosphate', 
               'Total Nitrogen', 'Transparency']
eutro = df[df['itemengname'].isin(eutro_items)]
eutro_pivot = eutro.pivot_table(
    index='month',
    columns='itemengname',
    values='value',
    aggfunc='mean'
).round(3)

# 重命名欄位
column_names = {
    'Carlson Trophic State Index': 'CTSI',
    'Chlorophyl-A': 'Chl-a (μg/L)',
    'Total-Phosphate': 'TP (mg/L)',
    'Total Nitrogen': 'TN (mg/L)',
    'Transparency': 'SD (m)'
}
eutro_pivot = eutro_pivot.rename(columns=column_names)
print("\n月平均值:")
print(eutro_pivot.to_string())

# === 3. 生成趨勢圖 ===
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('曾文水庫 2024年水質監測趨勢圖\nTseng-Wen Reservoir Water Quality Trends 2024', 
             fontsize=14, fontweight='bold')

# 圖1: TOC 和 COD 趨勢
ax1 = axes[0, 0]
if 'COD (mg/L)' in toc_cod_pivot.columns:
    ax1.plot(toc_cod_pivot.index, toc_cod_pivot['COD (mg/L)'], 'b-o', label='COD', linewidth=2, markersize=8)
if 'TOC (mg/L)' in toc_cod_pivot.columns:
    ax1.plot(toc_cod_pivot.index, toc_cod_pivot['TOC (mg/L)'], 'r-s', label='TOC', linewidth=2, markersize=8)
ax1.set_xlabel('Month')
ax1.set_ylabel('Concentration (mg/L)')
ax1.set_title('TOC & COD Monthly Trend')
ax1.legend()
ax1.grid(True, alpha=0.3)
ax1.tick_params(axis='x', rotation=45)

# 圖2: CTSI 優養狀態指標
ax2 = axes[0, 1]
if 'CTSI' in eutro_pivot.columns:
    ctsi_data = eutro_pivot['CTSI'].dropna()
    colors = ['green' if v < 40 else 'yellow' if v < 50 else 'orange' if v < 60 else 'red' for v in ctsi_data]
    ax2.bar(ctsi_data.index, ctsi_data.values, color=colors, edgecolor='black', linewidth=1.2)
    ax2.axhline(y=40, color='green', linestyle='--', alpha=0.7, label='貧養 (<40)')
    ax2.axhline(y=50, color='orange', linestyle='--', alpha=0.7, label='中養 (40-50)')
    ax2.axhline(y=60, color='red', linestyle='--', alpha=0.7, label='優養 (>50)')
ax2.set_xlabel('Month')
ax2.set_ylabel('CTSI Index')
ax2.set_title('Carlson Trophic State Index (CTSI)')
ax2.legend(loc='upper right', fontsize=8)
ax2.grid(True, alpha=0.3, axis='y')
ax2.tick_params(axis='x', rotation=45)

# 圖3: 葉綠素a 和 透明度
ax3 = axes[1, 0]
if 'Chl-a (μg/L)' in eutro_pivot.columns:
    ax3.plot(eutro_pivot.index, eutro_pivot['Chl-a (μg/L)'], 'g-^', label='Chl-a', linewidth=2, markersize=8)
ax3.set_xlabel('Month')
ax3.set_ylabel('Chlorophyll-a (μg/L)', color='green')
ax3.tick_params(axis='y', labelcolor='green')
ax3.tick_params(axis='x', rotation=45)

ax3_twin = ax3.twinx()
if 'SD (m)' in eutro_pivot.columns:
    ax3_twin.plot(eutro_pivot.index, eutro_pivot['SD (m)'], 'm-d', label='Transparency', linewidth=2, markersize=8)
ax3_twin.set_ylabel('Transparency (m)', color='purple')
ax3_twin.tick_params(axis='y', labelcolor='purple')

ax3.set_title('Chlorophyll-a & Transparency')
lines1, labels1 = ax3.get_legend_handles_labels()
lines2, labels2 = ax3_twin.get_legend_handles_labels()
ax3.legend(lines1 + lines2, labels1 + labels2, loc='upper right')
ax3.grid(True, alpha=0.3)

# 圖4: 總磷 和 總氮
ax4 = axes[1, 1]
if 'TP (mg/L)' in eutro_pivot.columns:
    ax4.plot(eutro_pivot.index, eutro_pivot['TP (mg/L)'] * 1000, 'c-o', label='TP (μg/L)', linewidth=2, markersize=8)
ax4.set_xlabel('Month')
ax4.set_ylabel('Total Phosphate (μg/L)', color='cyan')
ax4.tick_params(axis='y', labelcolor='cyan')
ax4.tick_params(axis='x', rotation=45)

ax4_twin = ax4.twinx()
if 'TN (mg/L)' in eutro_pivot.columns:
    ax4_twin.plot(eutro_pivot.index, eutro_pivot['TN (mg/L)'], 'brown', marker='s', label='TN (mg/L)', linewidth=2, markersize=8)
ax4_twin.set_ylabel('Total Nitrogen (mg/L)', color='brown')
ax4_twin.tick_params(axis='y', labelcolor='brown')

ax4.set_title('Total Phosphate & Total Nitrogen')
lines1, labels1 = ax4.get_legend_handles_labels()
lines2, labels2 = ax4_twin.get_legend_handles_labels()
ax4.legend(lines1 + lines2, labels1 + labels2, loc='upper right')
ax4.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('/Users/tfmacmini4/Documents/coludeskills/環保署水庫水質監測API-skill/tsengwen_2024_trends.png', 
            dpi=150, bbox_inches='tight', facecolor='white')
print("\n✅ 趨勢圖已儲存至: tsengwen_2024_trends.png")

# === 4. 輸出統計摘要 ===
print("\n" + "=" * 60)
print("統計摘要")
print("=" * 60)

stats_items = ['Chemical Oxygen Demand', 'Total Organic Carbon', 'Carlson Trophic State Index',
               'Chlorophyl-A', 'Total-Phosphate', 'Total Nitrogen', 'Transparency']

for item in stats_items:
    item_data = df[df['itemengname'] == item]['value'].dropna()
    if len(item_data) > 0:
        print(f"\n{item}:")
        print(f"  平均值: {item_data.mean():.3f}")
        print(f"  最大值: {item_data.max():.3f}")
        print(f"  最小值: {item_data.min():.3f}")
        print(f"  標準差: {item_data.std():.3f}")

# === 5. 優養化等級判定 ===
print("\n" + "=" * 60)
print("優養化等級判定")
print("=" * 60)

ctsi_values = df[df['itemengname'] == 'Carlson Trophic State Index']['value'].dropna()
if len(ctsi_values) > 0:
    avg_ctsi = ctsi_values.mean()
    if avg_ctsi < 40:
        status = "貧養 (Oligotrophic)"
    elif avg_ctsi < 50:
        status = "中養 (Mesotrophic)"
    else:
        status = "優養 (Eutrophic)"
    print(f"\n2024年平均 CTSI: {avg_ctsi:.1f}")
    print(f"水庫優養化狀態: {status}")

plt.show()
