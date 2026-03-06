# 環保署水庫水質監測 API 完整參考

## API 端點詳細說明

### wqx_p_03 - 水庫水質監測資料

**請求方式:** GET

**URL:** `https://data.moenv.gov.tw/api/v2/wqx_p_03`

**查詢參數完整說明:**

| 參數 | 類型 | 必填 | 預設值 | 說明 |
|------|------|------|--------|------|
| api_key | string | 是 | - | API 授權金鑰 |
| limit | integer | 否 | 1000 | 回傳筆數上限，最大 1000 |
| offset | integer | 否 | 0 | 資料起始位置偏移量 |
| format | string | 否 | json | 回傳格式: json, xml, csv |
| filters | string | 否 | - | 篩選條件，格式: 欄位名稱,運算子,值 |
| sort | string | 否 | - | 排序欄位 |

**篩選運算子:**
- `EQ` - 等於
- `NE` - 不等於
- `GT` - 大於
- `GE` - 大於等於
- `LT` - 小於
- `LE` - 小於等於
- `LIKE` - 包含

**篩選範例:**
```
# 篩選翡翠水庫資料
filters=reservoir,EQ,翡翠水庫

# 篩選 pH 值大於 7 的資料
filters=itemname,EQ,pH;itemvalue,GT,7

# 多條件篩選 (用分號分隔)
filters=reservoir,EQ,石門水庫;itemname,EQ,水溫
```

### wqx_p_08 - 水庫水質監測點基本資料

**請求方式:** GET

**URL:** `https://data.moenv.gov.tw/api/v2/wqx_p_08`

**回應欄位:**
- `reservoir` - 水庫名稱
- `sitename` - 測站名稱
- `twd97lon` - TWD97 經度
- `twd97lat` - TWD97 緯度
- `wgs84lon` - WGS84 經度
- `wgs84lat` - WGS84 緯度

### wqx_p_117 - 水庫水質月監測資料

**請求方式:** GET

**URL:** `https://data.moenv.gov.tw/api/v2/wqx_p_117`

**特色:**
- 提供月度彙整資料
- 適合長期趨勢分析

## 進階使用技巧

### 分頁處理
```python
def get_all_data(endpoint, api_key, page_size=1000):
    """分頁獲取所有資料"""
    all_records = []
    offset = 0
    
    while True:
        url = f"https://data.moenv.gov.tw/api/v2/{endpoint}"
        params = {
            "api_key": api_key,
            "limit": page_size,
            "offset": offset,
            "format": "json"
        }
        
        response = requests.get(url, params=params)
        data = response.json()
        
        records = data.get("records", [])
        if not records:
            break
            
        all_records.extend(records)
        offset += page_size
        
        # 如果取得的筆數小於 page_size，表示已經是最後一頁
        if len(records) < page_size:
            break
    
    return all_records
```

### 資料快取策略
```python
import json
import os
from datetime import datetime, timedelta

CACHE_DIR = "./cache"
CACHE_EXPIRY_HOURS = 24

def get_cached_data(cache_key):
    """從快取讀取資料"""
    cache_file = os.path.join(CACHE_DIR, f"{cache_key}.json")
    
    if os.path.exists(cache_file):
        with open(cache_file, 'r', encoding='utf-8') as f:
            cached = json.load(f)
            
        cache_time = datetime.fromisoformat(cached['timestamp'])
        if datetime.now() - cache_time < timedelta(hours=CACHE_EXPIRY_HOURS):
            return cached['data']
    
    return None

def save_to_cache(cache_key, data):
    """儲存資料到快取"""
    os.makedirs(CACHE_DIR, exist_ok=True)
    cache_file = os.path.join(CACHE_DIR, f"{cache_key}.json")
    
    with open(cache_file, 'w', encoding='utf-8') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'data': data
        }, f, ensure_ascii=False)
```

### 錯誤重試機制
```python
import time

def api_request_with_retry(url, params, max_retries=3, delay=1):
    """帶重試機制的 API 請求"""
    for attempt in range(max_retries):
        try:
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            if attempt < max_retries - 1:
                time.sleep(delay * (attempt + 1))
            else:
                raise e
```

## 資料分析範例

### 計算水庫優養化指標
```python
import pandas as pd

def analyze_eutrophication(reservoir_name, api_key):
    """分析水庫優養化狀態"""
    url = "https://data.moenv.gov.tw/api/v2/wqx_p_03"
    params = {
        "api_key": api_key,
        "filters": f"reservoir,EQ,{reservoir_name}",
        "limit": 1000,
        "format": "json"
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    df = pd.DataFrame(data['records'])
    
    # 樞紐分析：按日期和監測項目整理
    pivot = df.pivot_table(
        index='sampledate',
        columns='itemname',
        values='itemvalue',
        aggfunc='first'
    )
    
    return pivot

# 使用範例
analysis = analyze_eutrophication("翡翠水庫", API_KEY)
print(analysis)
```

### 繪製水質趨勢圖
```python
import matplotlib.pyplot as plt

def plot_water_quality_trend(data, item_name):
    """繪製水質指標趨勢圖"""
    filtered = data[data['itemname'] == item_name]
    
    plt.figure(figsize=(12, 6))
    plt.plot(filtered['sampledate'], filtered['itemvalue'].astype(float))
    plt.title(f'{item_name} 變化趨勢')
    plt.xlabel('採樣日期')
    plt.ylabel(f'{item_name} ({filtered["itemunit"].iloc[0]})')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
```
