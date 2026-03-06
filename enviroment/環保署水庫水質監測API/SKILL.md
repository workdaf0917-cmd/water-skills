---
name: reservoir-water-quality
description: "環保署水庫水質監測查詢：存取台灣環境部環境資料開放平台的水庫水質監測 API，查詢台灣各水庫的水質監測數據，包括水溫、pH值、溶氧量、導電度、濁度、懸浮固體、葉綠素a、優養狀態指標等水質參數。"
version: 1.0.0
tags:
  - taiwan
  - reservoir
  - water-quality
  - environment
  - api
  - monitoring
---

# 環保署水庫水質監測 API Skill

## 描述
此 skill 提供存取台灣環境部環境資料開放平台的水庫水質監測 API，可查詢台灣各水庫的水質監測數據，包括水溫、pH值、溶氧量、導電度、濁度、懸浮固體、葉綠素a、優養狀態指標等水質參數。

## 觸發條件
當用戶需要：
- 查詢台灣水庫水質資料
- 獲取水庫水質監測數據
- 了解特定水庫的水質狀況
- 分析水庫優養化程度
- 查詢水庫水質監測站資訊

## API 基本資訊

### Base URL
```
https://data.moenv.gov.tw/api/v2
```

### API Key
```
e0a736f5-a240-4a28-8ca1-d8ae7604334d
```

## 主要端點

### 1. 水庫水質監測資料 (wqx_p_03)
獲取水庫水質監測的詳細數據。

**端點:** `GET /wqx_p_03`

**完整 URL:**
```
https://data.moenv.gov.tw/api/v2/wqx_p_03?api_key=e0a736f5-a240-4a28-8ca1-d8ae7604334d
```

**查詢參數:**
| 參數 | 類型 | 必填 | 說明 |
|------|------|------|----- |
| api_key | string | 是 | API 金鑰 |
| limit | integer | 否 | 回傳筆數限制 (最大 1000) |
| offset | integer | 否 | 資料偏移量 (用於分頁) |
| format | string | 否 | 回傳格式 (json/xml/csv) |

**⚠️ 重要限制:**
- API 每次請求最多回傳 **1000** 筆記錄
- 完整資料集約有 **16萬+** 筆記錄
- 查詢特定水庫必須**遍歷所有資料並在客戶端篩選**
- filters 參數對中文篩選支援不佳，不建議使用

**回應欄位:**
- `siteid` - 測站代碼
- `siteengname` - 測站英文名稱
- `damename` - 水庫英文名稱
- `countyen` - 縣市英文名稱
- `townshipen` - 鄉鎮英文名稱
- `twd97lon` - TWD97 經度
- `twd97lat` - TWD97 緯度
- `sampledate` - 採樣日期時間
- `samplelayeren` - 採樣層 (Surface water/Bottom water)
- `sampledepth` - 採樣深度 (m)
- `itemengname` - 監測項目英文名稱
- `itemengabbreviation` - 監測項目縮寫
- `itemvalue` - 監測值
- `itemunit` - 單位

### 2. 水庫水質監測點基本資料 (wqx_p_08)
獲取水庫水質監測站的基本資訊。

**端點:** `GET /wqx_p_08`

**完整 URL:**
```
https://data.moenv.gov.tw/api/v2/wqx_p_08?api_key=e0a736f5-a240-4a28-8ca1-d8ae7604334d
```

### 3. 水庫水質月監測資料 (wqx_p_117)
獲取水庫水質的月度監測數據。

**端點:** `GET /wqx_p_117`

**完整 URL:**
```
https://data.moenv.gov.tw/api/v2/wqx_p_117?api_key=e0a736f5-a240-4a28-8ca1-d8ae7604334d
```

## 使用範例

### 範例 1: 獲取所有水庫水質資料
```bash
curl "https://data.moenv.gov.tw/api/v2/wqx_p_03?api_key=e0a736f5-a240-4a28-8ca1-d8ae7604334d&limit=100&format=json"
```

### 範例 2: 分頁獲取資料
```bash
# 第一頁
curl "https://data.moenv.gov.tw/api/v2/wqx_p_03?api_key=e0a736f5-a240-4a28-8ca1-d8ae7604334d&limit=1000&offset=0"
# 第二頁
curl "https://data.moenv.gov.tw/api/v2/wqx_p_03?api_key=e0a736f5-a240-4a28-8ca1-d8ae7604334d&limit=1000&offset=1000"
```

### 範例 3: Python 程式碼範例 - 查詢特定水庫
```python
import requests

API_KEY = "e0a736f5-a240-4a28-8ca1-d8ae7604334d"
BASE_URL = "https://data.moenv.gov.tw/api/v2"

def get_reservoir_data(reservoir_keyword: str, year: str = None):
    """
    獲取特定水庫的水質監測資料
    
    Args:
        reservoir_keyword: 水庫英文關鍵字 (如 "A-Kung-Tien", "Fei-Tsui")
        year: 年份篩選 (如 "2024")
    
    Returns:
        水質監測資料列表
    """
    all_records = []
    offset = 0
    
    while True:
        response = requests.get(
            f"{BASE_URL}/wqx_p_03",
            params={
                "api_key": API_KEY,
                "limit": 1000,
                "offset": offset,
                "format": "json"
            },
            timeout=30
        )
        
        if response.status_code != 200:
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
        
        if len(data) < 1000:
            break
        offset += 1000
    
    return all_records

# 使用範例: 獲取阿公店水庫2024年資料
data = get_reservoir_data("A-Kung-Tien", "2024")
print(f"找到 {len(data)} 筆記錄")
```

### 範例 4: JavaScript/Node.js 程式碼範例
```javascript
const API_KEY = "e0a736f5-a240-4a28-8ca1-d8ae7604334d";
const BASE_URL = "https://data.moenv.gov.tw/api/v2";

async function getReservoirWaterQuality(reservoirName = null, limit = 100) {
    let url = `${BASE_URL}/wqx_p_03?api_key=${API_KEY}&limit=${limit}&format=json`;
    
    if (reservoirName) {
        url += `&filters=reservoir,EQ,${encodeURIComponent(reservoirName)}`;
    }
    
    const response = await fetch(url);
    
    if (!response.ok) {
        throw new Error(`API 請求失敗: ${response.status}`);
    }
    
    return response.json();
}

// 使用範例
getReservoirWaterQuality("石門水庫", 50)
    .then(data => console.log(data))
    .catch(err => console.error(err));
```

## 常見水庫名稱對照表
| 中文名稱 | API英文名稱 (siteengname關鍵字) |
|----------|-------------------------------|
| 翡翠水庫 | Fei-Tsui Reservoir |
| 石門水庫 | Shihmen Reservoir |
| 曾文水庫 | Tseng-Wen Reservoir |
| 日月潭水庫 | Sun Moon Lake Reservoir |
| 德基水庫 | Te-Chi Reservoir |
| 霧社水庫 | Wu-She Reservoir |
| 鯉魚潭水庫 | Li-Yu-Tan Reservoir |
| 南化水庫 | Nan-Hua Reservoir |
| 烏山頭水庫 | Wu-Shan-Tou Reservoir |
| 阿公店水庫 | A-Kung-Tien Reservoir |

## 常見監測項目 (itemengname)
| 中文名稱 | API英文名稱 | 縮寫 | 單位 |
|----------|-------------|------|------|
| 水溫 | Water Temperature | WT | °C |
| pH值 | pH | pH | - |
| 溶氧量 | Dissolved Oxygen | DO2 | mg/L |
| 導電度 | Conductivity | EC | μmho/cm |
| 濁度 | Turbidity | Tur | NTU |
| 懸浮固體 | Suspended Solids | SS | mg/L |
| 葉綠素a | Chlorophyl-A | Chl_a | μg/L |
| 總磷 | Total-Phosphate | TP | mg/L |
| 總氮 | Total Nitrogen | TN | mg/L |
| 優養指標 | Carlson Trophic State Index | CTSI | - |
| 透明度 | Transparency | SD | m |
| 總有機碳 | Total Organic Carbon | TOC | mg/L |
| 化學需氧量 | Chemical Oxygen Demand | COD | mg/L |

## 回應格式範例
```json
[
  {
    "siteid": "2095",
    "siteengname": "Fei-Tsui Reservoir VI",
    "damename": "Fei-Tsui Reservoir",
    "countyen": "New Taipei City",
    "townshipen": "Shihding District",
    "twd97lon": "121.6222770",
    "twd97lat": "24.9374720",
    "sampledate": "2025-10-01 10:43:00",
    "samplelayeren": "Surface water",
    "sampledepth": "0.5",
    "itemengname": "Chlorophyl-A",
    "itemengabbreviation": "Chl_a",
    "itemvalue": "4.7",
    "itemunit": "μg/L"
  }
]
```

## 錯誤處理
- **401 Unauthorized**: API Key 無效或缺失
- **404 Not Found**: 端點不存在
- **429 Too Many Requests**: 請求過於頻繁，請稍後再試
- **500 Internal Server Error**: 伺服器內部錯誤

## 注意事項
1. API Key 需妥善保管，不要公開分享
2. 建議設置適當的請求頻率限制
3. 資料更新頻率依據環境部公告為準 (通常每季更新)
4. **API 每次最多回傳 1000 筆，需使用 offset 分頁遍歷**
5. **篩選特定水庫需在客戶端進行，使用 siteengname 欄位比對**
6. 完整資料集約 16萬筆，遍歷需要數分鐘時間
7. 建議將查詢結果快取以提升效能
