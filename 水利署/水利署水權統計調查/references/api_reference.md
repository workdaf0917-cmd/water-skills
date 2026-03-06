# 台灣經濟部水利署水權統計資料 API

**API 版本:** v2  
**基礎 URL:** https://opendata.wra.gov.tw/api/v2/

---

## 目錄

- [API 概述](#api-概述)
- [水權統計資料端點](#水權統計資料端點)
- [資料欄位說明](#資料欄位說明)
- [使用範例](#使用範例)
- [應用場景](#應用場景)

---

## API 概述

水利署水權統計資料 API 提供台灣中央主管機關有效水權件數及水量的查詢服務。本資料集包含已核准通過的水權資料，涵蓋不同水源類別、用水標的、主管機關等資訊。

### 主要特點

- **RESTful API**: 使用 HTTP GET 方法
- **回傳格式**: JSON
- **資料更新**: 每月更新
- **免費使用**: 開放資料，無需認證

### 伺服器位址

```
https://opendata.wra.gov.tw
```

---

## 水權統計資料端點

### 取得水權統計資料

**端點:** `/api/v2/03be73eb-5da8-45d4-87d9-4e78d476a843`

**方法:** GET

**完整 URL:**
```
https://opendata.wra.gov.tw/api/v2/03be73eb-5da8-45d4-87d9-4e78d476a843
```

**說明:**  
本端點提供中央主管機關有效水權件數及水量供民眾查詢。資料內容為中央主管機關已核准通過之水權資料。

**請求參數:**  
無需參數，直接 GET 請求即可取得所有資料。

**回應格式:**  
JSON 陣列，包含多筆水權統計記錄。

---

## 資料欄位說明

每筆水權記錄包含以下欄位:

| 欄位名稱     | 英文欄位                                   | 資料型別 | 說明                      | 範例                                     |
| ------------ | ------------------------------------------ | -------- | ------------------------- | ---------------------------------------- |
| 序號         | `serialnumber`                             | String   | 記錄序號                  | "349"                                    |
| 統計年份     | `statisticsyear`                           | String   | 資料統計年份              | "2025"                                   |
| 統計月份     | `statisticsmonth`                          | String   | 資料統計月份              | "11"                                     |
| 主管機關     | `authority`                                | String   | 核發水權的主管機關        | "經濟部水利署"                           |
| 引水地點縣市 | `countyofchanneledwaterloation`            | String   | 引水地點所在縣市          | "花蓮縣"                                 |
| 水權狀類別   | `licenseclass`                             | String   | 水權證照類別              | "水權狀", "臨時用水"                     |
| 水源類別     | `watersourceclass`                         | String   | 水源分類代碼              | "0"                                      |
| 水源支流     | `minorstreamofchanneledwatersource`        | String   | 引水來源支流名稱          | "和平南溪"                               |
| 用水標的     | `waterconsumptionpurpose`                  | String   | 用水目的類別              | "農業用水", "工業用水", "家用及公共給水" |
| 一月引水量   | `quantityofchanneledwaterinmonthjanuary`   | Number   | 一月份引水量 (立方公尺)   | 347388.48                                |
| 二月引水量   | `quantityofchanneledwaterinmonthfebruary`  | Number   | 二月份引水量 (立方公尺)   | 6743278.08                               |
| 三月引水量   | `quantityofchanneledwaterinmonthmarch`     | Number   | 三月份引水量 (立方公尺)   | 8544765.60                               |
| 四月引水量   | `quantityofchanneledwaterinmonthapril`     | Number   | 四月份引水量 (立方公尺)   | 8269128.00                               |
| 五月引水量   | `quantityofchanneledwaterinmonthmay`       | Number   | 五月份引水量 (立方公尺)   | 8544765.60                               |
| 六月引水量   | `quantityofchanneledwaterinmonthjune`      | Number   | 六月份引水量 (立方公尺)   | 8269128.00                               |
| 七月引水量   | `quantityofchanneledwaterinmonthjuly`      | Number   | 七月份引水量 (立方公尺)   | 8471243.52                               |
| 八月引水量   | `quantityofchanneledwaterinmonthaugust`    | Number   | 八月份引水量 (立方公尺)   | 8544765.60                               |
| 九月引水量   | `quantityofchanneledwaterinmonthseptember` | Number   | 九月份引水量 (立方公尺)   | 8269128.00                               |
| 十月引水量   | `quantityofchanneledwaterinmonthoctober`   | Number   | 十月份引水量 (立方公尺)   | 8544765.60                               |
| 十一月引水量 | `quantityofchanneledwaterninmonthnovember` | Number   | 十一月份引水量 (立方公尺) | 8269128.00                               |
| 十二月引水量 | `quantityofchanneledwaterinmonthdecember`  | Number   | 十二月份引水量 (立方公尺) | 0.00                                     |

### 用水標的分類

- **農業用水**: 農田灌溉、畜牧等農業相關用水
- **工業用水**: 工廠製程、冷卻等工業用水
- **家用及公共給水**: 民生用水、公共設施用水
- **水力用水**: 水力發電用水
- **其他**: 其他特殊用途用水

### 水權狀類別

- **水權狀**: 正式核發的長期水權證照
- **臨時用水**: 臨時性、短期的用水許可

---

## 使用範例

### Python 範例

#### 基本請求

```python
import requests
import json

# API 端點
url = "https://opendata.wra.gov.tw/api/v2/03be73eb-5da8-45d4-87d9-4e78d476a843"

# 發送 GET 請求
response = requests.get(url)

# 檢查回應狀態
if response.status_code == 200:
    data = response.json()
    print(f"取得 {len(data)} 筆水權資料")
    
    # 顯示第一筆資料
    if data:
        print("\n第一筆資料範例:")
        print(json.dumps(data[0], indent=2, ensure_ascii=False))
else:
    print(f"請求失敗: {response.status_code}")
```

#### 篩選特定縣市的水權資料

```python
import requests

url = "https://opendata.wra.gov.tw/api/v2/03be73eb-5da8-45d4-87d9-4e78d476a843"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    
    # 篩選花蓮縣的水權資料
    hualien_data = [
        record for record in data 
        if record.get('countyofchanneledwaterloation') == '花蓮縣'
    ]
    
    print(f"花蓮縣水權資料: {len(hualien_data)} 筆")
    
    # 計算總引水量
    total_water = sum(
        float(record.get('quantityofchanneledwaterinmonthjanuary', 0))
        for record in hualien_data
    )
    print(f"花蓮縣一月總引水量: {total_water:,.2f} 立方公尺")
```

#### 分析不同用水標的

```python
import requests
from collections import defaultdict

url = "https://opendata.wra.gov.tw/api/v2/03be73eb-5da8-45d4-87d9-4e78d476a843"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    
    # 按用水標的分類統計
    purpose_stats = defaultdict(int)
    
    for record in data:
        purpose = record.get('waterconsumptionpurpose', '未分類')
        purpose_stats[purpose] += 1
    
    print("各用水標的水權件數統計:")
    for purpose, count in sorted(purpose_stats.items(), key=lambda x: x[1], reverse=True):
        print(f"  {purpose}: {count} 件")
```

#### 計算年度總引水量

```python
import requests

url = "https://opendata.wra.gov.tw/api/v2/03be73eb-5da8-45d4-87d9-4e78d476a843"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    
    # 月份欄位名稱
    month_fields = [
        'quantityofchanneledwaterinmonthjanuary',
        'quantityofchanneledwaterinmonthfebruary',
        'quantityofchanneledwaterinmonthmarch',
        'quantityofchanneledwaterinmonthapril',
        'quantityofchanneledwaterinmonthmay',
        'quantityofchanneledwaterinmonthjune',
        'quantityofchanneledwaterinmonthjuly',
        'quantityofchanneledwaterinmonthaugust',
        'quantityofchanneledwaterinmonthseptember',
        'quantityofchanneledwaterinmonthoctober',
        'quantityofchanneledwaterninmonthnovember',
        'quantityofchanneledwaterinmonthdecember'
    ]
    
    # 計算每筆記錄的年度總引水量
    for record in data[:5]:  # 只顯示前 5 筆
        annual_total = sum(
            float(record.get(field, 0)) 
            for field in month_fields
        )
        
        print(f"序號 {record.get('serialnumber')}:")
        print(f"  縣市: {record.get('countyofchanneledwaterloation')}")
        print(f"  用途: {record.get('waterconsumptionpurpose')}")
        print(f"  年度總引水量: {annual_total:,.2f} 立方公尺")
        print()
```

### JavaScript 範例

```javascript
// 使用 fetch API
const url = 'https://opendata.wra.gov.tw/api/v2/03be73eb-5da8-45d4-87d9-4e78d476a843';

fetch(url)
  .then(response => response.json())
  .then(data => {
    console.log(`取得 ${data.length} 筆水權資料`);
    
    // 篩選農業用水
    const agriculturalWater = data.filter(
      record => record.waterconsumptionpurpose === '農業用水'
    );
    
    console.log(`農業用水: ${agriculturalWater.length} 件`);
  })
  .catch(error => console.error('錯誤:', error));
```

### curl 範例

```bash
# 基本請求
curl "https://opendata.wra.gov.tw/api/v2/03be73eb-5da8-45d4-87d9-4e78d476a843"

# 格式化輸出 (需要 jq)
curl "https://opendata.wra.gov.tw/api/v2/03be73eb-5da8-45d4-87d9-4e78d476a843" | jq '.'

# 只顯示前 3 筆
curl "https://opendata.wra.gov.tw/api/v2/03be73eb-5da8-45d4-87d9-4e78d476a843" | jq '.[:3]'

# 篩選特定縣市
curl "https://opendata.wra.gov.tw/api/v2/03be73eb-5da8-45d4-87d9-4e78d476a843" | \
  jq '[.[] | select(.countyofchanneledwaterloation == "臺北市")]'
```

---

## 應用場景

### 1. 水資源管理分析

```python
# 分析各縣市水權分布
import requests
import pandas as pd

url = "https://opendata.wra.gov.tw/api/v2/03be73eb-5da8-45d4-87d9-4e78d476a843"
response = requests.get(url)
data = response.json()

# 轉換為 DataFrame
df = pd.DataFrame(data)

# 各縣市水權件數統計
county_stats = df.groupby('countyofchanneledwaterloation').agg({
    'serialnumber': 'count',
    'quantityofchanneledwaterinmonthjanuary': 'sum'
}).rename(columns={
    'serialnumber': '水權件數',
    'quantityofchanneledwaterinmonthjanuary': '一月總引水量'
})

print(county_stats.sort_values('水權件數', ascending=False))
```

### 2. 用水趨勢分析

```python
# 分析月份用水變化
import requests
import matplotlib.pyplot as plt

url = "https://opendata.wra.gov.tw/api/v2/03be73eb-5da8-45d4-87d9-4e78d476a843"
response = requests.get(url)
data = response.json()

# 計算各月份總引水量
months = ['january', 'february', 'march', 'april', 'may', 'june',
          'july', 'august', 'september', 'october', 'november', 'december']

monthly_totals = []
for month in months:
    field = f'quantityofchanneledwaterinmonth{month}'
    if month == 'november':
        field = 'quantityofchanneledwaterninmonthnovember'
    
    total = sum(float(record.get(field, 0)) for record in data)
    monthly_totals.append(total)

# 繪製圖表
plt.figure(figsize=(12, 6))
plt.bar(range(1, 13), monthly_totals)
plt.xlabel('月份')
plt.ylabel('總引水量 (立方公尺)')
plt.title('各月份總引水量統計')
plt.xticks(range(1, 13))
plt.show()
```

### 3. 水權資料匯出

```python
# 匯出為 CSV 檔案
import requests
import csv

url = "https://opendata.wra.gov.tw/api/v2/03be73eb-5da8-45d4-87d9-4e78d476a843"
response = requests.get(url)
data = response.json()

# 匯出為 CSV
if data:
    with open('water_rights.csv', 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
    
    print("資料已匯出至 water_rights.csv")
```

### 4. 即時監控儀表板

```python
# 建立簡單的統計摘要
import requests
from datetime import datetime

def get_water_rights_summary():
    url = "https://opendata.wra.gov.tw/api/v2/03be73eb-5da8-45d4-87d9-4e78d476a843"
    response = requests.get(url)
    data = response.json()
    
    summary = {
        '更新時間': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        '總水權件數': len(data),
        '涵蓋縣市數': len(set(r.get('countyofchanneledwaterloation') for r in data)),
        '主管機關數': len(set(r.get('authority') for r in data)),
        '用水標的類別': len(set(r.get('waterconsumptionpurpose') for r in data))
    }
    
    return summary

# 執行
summary = get_water_rights_summary()
for key, value in summary.items():
    print(f"{key}: {value}")
```

---

## 相關資源

- **API 文件**: https://opendata.wra.gov.tw/openapi/swagger/index.html
- **水利署開放資料平台**: https://opendata.wra.gov.tw/
- **水利署官網**: https://www.wra.gov.tw/

---

## 注意事項

1. **資料更新頻率**: 資料每月更新，建議定期重新取得最新資料
2. **資料量**: 完整資料集可能包含數千筆記錄，請注意處理效能
3. **編碼**: 回應為 UTF-8 編碼，包含繁體中文內容
4. **無需認證**: 此為開放 API，無需申請 API Key
5. **使用限制**: 請合理使用，避免過度頻繁請求造成伺服器負擔

---

**最後更新**: 2026-01-24
