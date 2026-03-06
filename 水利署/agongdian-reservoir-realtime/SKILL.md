---
name: agongdian-reservoir-realtime
description: "水利署阿公店水庫即時水情查詢：存取經濟部水利署開放資料平台的阿公店水庫即時水情 API，查詢阿公店水庫的即時水位、有效蓄水量、時雨量、本日累積雨量等水情資料。資料每小時整點更新。"
version: "1.0.0"
---

# 水利署阿公店水庫即時水情 API Skill

## 描述
此 skill 提供存取經濟部水利署開放資料平台的阿公店水庫即時水情 API，可查詢阿公店水庫的即時水位、有效蓄水量、時雨量、本日累積雨量等水情資料。資料每小時整點更新。

## 觸發條件
當用戶需要：
- 查詢阿公店水庫即時水情
- 獲取阿公店水庫水位資訊
- 查詢阿公店水庫蓄水量
- 了解阿公店水庫雨量狀況
- 分析阿公店水庫水情趨勢

## API 基本資訊

### Base URL
```
https://opendata.wra.gov.tw/api/v2
```

### 無需 API Key
水利署開放資料平台**不需要 API Key**，可直接存取。

## 阿公店水庫即時水情 API

### 端點
```
GET /api/v2/ecc4ce8d-0942-474a-8705-53e9aaa7c4e8
```

### 完整 URL
```
https://opendata.wra.gov.tw/api/v2/ecc4ce8d-0942-474a-8705-53e9aaa7c4e8
```

### 查詢參數
| 參數 | 類型 | 必填 | 說明 |
|------|------|------|------|
| page | integer | 否 | 頁碼 (1..N)，預設值: 1 |
| size | integer | 否 | 每頁筆數，上限 1000，預設值: 1000 |

### 回應欄位說明
| 欄位名稱 | 說明 | 單位 |
|----------|------|------|
| `reservoirname` | 水庫名稱 | - |
| `reservoiridentifier` | 水庫代碼 | - |
| `datetime` | 觀測時間 | ISO 8601 格式 |
| `waterlevel` | 水位 | 公尺 (m) |
| `effectivewaterstoragecapacity` | 有效蓄水量 | 萬立方公尺 |
| `precipitationhourly` | 時雨量 | 毫米 (mm) |
| `basinrainfall` | 本日累積雨量 | 毫米 (mm) |

### 回應範例
```json
[
  {
    "basinrainfall": "0.0",
    "datetime": "2026-01-22T13:00:00",
    "effectivewaterstoragecapacity": "1099.0",
    "precipitationhourly": "0.0",
    "reservoiridentifier": "30802",
    "reservoirname": "阿公店水庫",
    "waterlevel": "35.66"
  }
]
```

## 使用範例

### 範例 1: cURL 快速查詢
```bash
# 獲取阿公店水庫最新水情
curl -s "https://opendata.wra.gov.tw/api/v2/ecc4ce8d-0942-474a-8705-53e9aaa7c4e8?size=1" | jq '.[0]'

# 獲取最近24小時水情
curl -s "https://opendata.wra.gov.tw/api/v2/ecc4ce8d-0942-474a-8705-53e9aaa7c4e8?size=24" | jq
```

### 範例 2: Python 查詢阿公店水庫即時水情
```python
import requests
from datetime import datetime

def get_agongdian_realtime():
    """獲取阿公店水庫即時水情"""
    url = "https://opendata.wra.gov.tw/api/v2/ecc4ce8d-0942-474a-8705-53e9aaa7c4e8"
    
    response = requests.get(url, params={"size": 1}, timeout=10)
    response.raise_for_status()
    
    data = response.json()
    if data:
        latest = data[0]
        return {
            "水庫名稱": latest["reservoirname"],
            "觀測時間": latest["datetime"],
            "水位(公尺)": float(latest["waterlevel"]),
            "有效蓄水量(萬立方公尺)": float(latest["effectivewaterstoragecapacity"]),
            "時雨量(mm)": float(latest["precipitationhourly"]),
            "本日累積雨量(mm)": float(latest["basinrainfall"])
        }
    return None

# 使用範例
info = get_agongdian_realtime()
if info:
    print(f"【{info['水庫名稱']}】即時水情")
    print(f"觀測時間: {info['觀測時間']}")
    print(f"水位: {info['水位(公尺)']} 公尺")
    print(f"有效蓄水量: {info['有效蓄水量(萬立方公尺)']} 萬立方公尺")
    print(f"時雨量: {info['時雨量(mm)']} mm")
    print(f"本日累積雨量: {info['本日累積雨量(mm)']} mm")
```

### 範例 3: Python 查詢歷史水情趨勢
```python
import requests
import pandas as pd

def get_agongdian_history(hours: int = 24):
    """獲取阿公店水庫歷史水情"""
    url = "https://opendata.wra.gov.tw/api/v2/ecc4ce8d-0942-474a-8705-53e9aaa7c4e8"
    
    response = requests.get(url, params={"size": hours}, timeout=30)
    response.raise_for_status()
    
    data = response.json()
    df = pd.DataFrame(data)
    df['datetime'] = pd.to_datetime(df['datetime'])
    df['waterlevel'] = df['waterlevel'].astype(float)
    df['effectivewaterstoragecapacity'] = df['effectivewaterstoragecapacity'].astype(float)
    
    return df.sort_values('datetime')

# 獲取最近48小時資料
df = get_agongdian_history(48)
print(df[['datetime', 'waterlevel', 'effectivewaterstoragecapacity']])
```

### 範例 4: JavaScript/Node.js 範例
```javascript
async function getAgongdianReservoir() {
    const url = 'https://opendata.wra.gov.tw/api/v2/ecc4ce8d-0942-474a-8705-53e9aaa7c4e8';
    
    const response = await fetch(`${url}?size=1`);
    if (!response.ok) throw new Error(`HTTP error: ${response.status}`);
    
    const data = await response.json();
    if (data.length > 0) {
        const latest = data[0];
        console.log(`【${latest.reservoirname}】即時水情`);
        console.log(`觀測時間: ${latest.datetime}`);
        console.log(`水位: ${latest.waterlevel} 公尺`);
        console.log(`有效蓄水量: ${latest.effectivewaterstoragecapacity} 萬立方公尺`);
    }
}

getAgongdianReservoir();
```

## 其他水庫即時水情 API 端點

| 水庫名稱 | API 端點 UUID | 完整 URL |
|----------|---------------|----------|
| 阿公店水庫 | `ecc4ce8d-0942-474a-8705-53e9aaa7c4e8` | `https://opendata.wra.gov.tw/api/v2/ecc4ce8d-0942-474a-8705-53e9aaa7c4e8` |
| 曾文水庫 | `598befe9-a6fe-4126-a8cc-52ccbbecfc68` | `https://opendata.wra.gov.tw/api/v2/598befe9-a6fe-4126-a8cc-52ccbbecfc68` |
| 牡丹水庫 | `6d7ba910-b627-4844-882b-df232064db0c` | `https://opendata.wra.gov.tw/api/v2/6d7ba910-b627-4844-882b-df232064db0c` |
| 石門水庫濁度 | `7cd352ef-6518-4396-b2d6-61f1946a5611` | `https://opendata.wra.gov.tw/api/v2/7cd352ef-6518-4396-b2d6-61f1946a5611` |
| 水庫每日營運狀況 | `51023e88-4c76-4dbc-bbb9-470da690d539` | `https://opendata.wra.gov.tw/api/v2/51023e88-4c76-4dbc-bbb9-470da690d539` |
| 水庫水情資料(綜合) | `2be9044c-6e44-4856-aad5-dd108c2e6679` | `https://opendata.wra.gov.tw/api/v2/2be9044c-6e44-4856-aad5-dd108c2e6679` |

## 阿公店水庫基本資料
- **水庫代碼**: 30802
- **管理單位**: 經濟部水利署南區水資源局
- **位置**: 高雄市燕巢區、田寮區
- **集水面積**: 31.87 平方公里
- **滿水位**: 40 公尺
- **有效容量**: 約 1800 萬立方公尺
- **資料更新頻率**: 每小時整點更新

## 資料說明
水位資料係於水庫適當位置設置水位計，於整點擷取水庫水位資料，並透過傳輸系統傳回管理單位資料庫。測得水庫水位資料後，並依據水庫淤積測量結果，即可得水庫有效蓄水量資料。時雨量資料則於水庫集水區適當位置設置多處雨量計，透過傳輸系統傳回管理單位資料庫，並經加權計算後即可得集水區(平均)時雨量資料。

## 注意事項
1. 水利署 API **無需 API Key**，可直接存取
2. 資料每小時整點更新一次
3. 即時資料為監測儀器之原始資料，部份資料未經檢核，使用者引用及參考時請謹慎注意
4. size 參數上限為 1000 筆
5. 資料以 JSON 格式回傳
