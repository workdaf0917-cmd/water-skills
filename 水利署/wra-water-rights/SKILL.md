---
name: wra-water-rights
description: 台灣經濟部水利署水權統計資料 API - 提供中央主管機關有效水權件數及水量查詢，包括水源類別、用水標的、主管機關、各月份引水量等資訊。適用於水資源管理、水權查詢、用水統計分析等應用。
---

# 台灣水利署水權統計資料 API Skill

提供台灣經濟部水利署水權統計資料的完整 API 使用指南，包含資料查詢、分析範例及實際應用場景。

## 何時使用此 Skill

此 skill 適用於以下情境：

### 水資源管理
- 查詢台灣各縣市水權分布狀況
- 分析不同用水標的（農業、工業、民生）的水權配置
- 統計各主管機關核發的水權數量
- 追蹤水權使用趨勢

### 資料分析與研究
- 進行水資源利用研究
- 分析各月份引水量變化
- 比較不同地區的用水模式
- 製作水權統計報表

### 應用開發
- 開發水資源管理系統
- 建立水權查詢平台
- 製作水資源視覺化儀表板
- 整合水權資料至其他系統

### 政策規劃
- 評估水資源分配狀況
- 支援水權政策制定
- 監測水資源使用情形
- 進行區域水資源規劃

## 快速開始

### 基本 API 呼叫

```python
import requests

# 取得所有水權資料
url = "https://opendata.wra.gov.tw/api/v2/03be73eb-5da8-45d4-87d9-4e78d476a843"
response = requests.get(url)
data = response.json()

print(f"共有 {len(data)} 筆水權資料")
```

### 常見查詢範例

#### 1. 查詢特定縣市的水權資料

```python
# 篩選台北市的水權
taipei_data = [
    record for record in data 
    if record.get('countyofchanneledwaterloation') == '臺北市'
]
```

#### 2. 統計各用水標的

```python
from collections import Counter

purposes = [record.get('waterconsumptionpurpose') for record in data]
purpose_count = Counter(purposes)

for purpose, count in purpose_count.most_common():
    print(f"{purpose}: {count} 件")
```

#### 3. 計算月份引水量

```python
# 計算一月份總引水量
jan_total = sum(
    float(record.get('quantityofchanneledwaterinmonthjanuary', 0))
    for record in data
)
print(f"一月總引水量: {jan_total:,.0f} 立方公尺")
```

## 參考文件

此 skill 包含詳細的參考文件於 `references/` 目錄：

### **api_reference.md** - 完整 API 文件
包含：
- API 端點說明
- 完整資料欄位定義
- Python、JavaScript、curl 使用範例
- 實際應用場景範例
- 資料分析與視覺化範例

使用 `view_file` 工具查看詳細內容。

## 核心功能

### 1. 資料欄位

每筆水權記錄包含：
- **基本資訊**: 序號、統計年月、主管機關
- **地理資訊**: 引水地點縣市、水源支流
- **水權資訊**: 水權狀類別、水源類別、用水標的
- **用水量**: 12 個月份的引水量數據（立方公尺）

### 2. 用水標的分類

- 農業用水
- 工業用水
- 家用及公共給水
- 水力用水
- 其他用途

### 3. 主管機關

- 經濟部水利署
- 經濟部水利署北區水資源分署
- 經濟部水利署中區水資源分署
- 經濟部水利署南區水資源分署
- 其他地方主管機關

## 實用程式碼範例

### 資料轉換為 DataFrame

```python
import pandas as pd
import requests

url = "https://opendata.wra.gov.tw/api/v2/03be73eb-5da8-45d4-87d9-4e78d476a843"
response = requests.get(url)
data = response.json()

# 轉換為 pandas DataFrame
df = pd.DataFrame(data)

# 查看資料摘要
print(df.info())
print(df.describe())
```

### 匯出為 Excel

```python
import pandas as pd
import requests

url = "https://opendata.wra.gov.tw/api/v2/03be73eb-5da8-45d4-87d9-4e78d476a843"
response = requests.get(url)
data = response.json()

df = pd.DataFrame(data)
df.to_excel('water_rights.xlsx', index=False, engine='openpyxl')
print("資料已匯出至 water_rights.xlsx")
```

### 建立統計摘要

```python
import requests

def get_summary():
    url = "https://opendata.wra.gov.tw/api/v2/03be73eb-5da8-45d4-87d9-4e78d476a843"
    response = requests.get(url)
    data = response.json()
    
    return {
        '總水權件數': len(data),
        '涵蓋縣市': len(set(r['countyofchanneledwaterloation'] for r in data)),
        '主管機關數': len(set(r['authority'] for r in data)),
        '用水標的類別': len(set(r['waterconsumptionpurpose'] for r in data))
    }

summary = get_summary()
for key, value in summary.items():
    print(f"{key}: {value}")
```

## 進階應用

### 1. 時間序列分析

分析各月份用水量變化趨勢，識別季節性模式。

### 2. 地理分布分析

視覺化各縣市水權分布，製作互動式地圖。

### 3. 用水效率評估

比較不同用水標的的引水量，評估用水效率。

### 4. 預測模型

基於歷史資料建立用水量預測模型。

## 資料特性

### 更新頻率
- 每月更新一次
- 建議定期重新取得最新資料

### 資料規模
- 包含數千筆水權記錄
- 涵蓋全台各縣市
- 完整的月份用水量資料

### 資料品質
- 官方核准的正式水權資料
- 結構化 JSON 格式
- UTF-8 編碼，支援繁體中文

## 最佳實踐

### 1. 資料快取
```python
import requests
import json
from datetime import datetime, timedelta

def get_cached_data(cache_file='water_rights_cache.json', max_age_hours=24):
    """取得快取資料，超過時效則重新下載"""
    try:
        with open(cache_file, 'r', encoding='utf-8') as f:
            cache = json.load(f)
            cache_time = datetime.fromisoformat(cache['timestamp'])
            
            if datetime.now() - cache_time < timedelta(hours=max_age_hours):
                return cache['data']
    except (FileNotFoundError, KeyError, ValueError):
        pass
    
    # 下載新資料
    url = "https://opendata.wra.gov.tw/api/v2/03be73eb-5da8-45d4-87d9-4e78d476a843"
    response = requests.get(url)
    data = response.json()
    
    # 儲存快取
    with open(cache_file, 'w', encoding='utf-8') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'data': data
        }, f, ensure_ascii=False)
    
    return data
```

### 2. 錯誤處理
```python
import requests

def safe_get_water_rights():
    """安全地取得水權資料，包含錯誤處理"""
    url = "https://opendata.wra.gov.tw/api/v2/03be73eb-5da8-45d4-87d9-4e78d476a843"
    
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        print("請求逾時，請稍後再試")
        return None
    except requests.exceptions.RequestException as e:
        print(f"請求失敗: {e}")
        return None
    except json.JSONDecodeError:
        print("JSON 解析失敗")
        return None
```

### 3. 資料驗證
```python
def validate_record(record):
    """驗證水權記錄的完整性"""
    required_fields = [
        'serialnumber',
        'statisticsyear',
        'statisticsmonth',
        'authority',
        'countyofchanneledwaterloation',
        'waterconsumptionpurpose'
    ]
    
    return all(field in record for field in required_fields)
```

## 相關資源

- **API 文件**: https://opendata.wra.gov.tw/openapi/swagger/index.html
- **水利署開放資料平台**: https://opendata.wra.gov.tw/
- **水利署官網**: https://www.wra.gov.tw/

## 注意事項

1. **無需認證**: 此為開放 API，無需申請 API Key
2. **使用限制**: 請合理使用，避免過度頻繁請求
3. **資料授權**: 遵循政府資料開放授權條款
4. **編碼格式**: 回應為 UTF-8 編碼
5. **資料時效**: 建議定期更新資料以確保時效性

## 更新此 Skill

若需更新此 skill 的文件內容：

1. 修改 `configs/wra-water-rights.json` 配置檔
2. 執行 `python cli/doc_scraper.py --config configs/wra-water-rights.json`
3. Skill 將會重新建置並包含最新資訊

---

**版本**: 1.0  
**最後更新**: 2026-01-24  
**資料來源**: 經濟部水利署開放資料平台
