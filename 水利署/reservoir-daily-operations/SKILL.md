---
name: reservoir-daily-operations
description: "水利署水庫每日營運狀況查詢：存取經濟部水利署開放資料平台，查詢台灣 69 座水庫與堰壩的每日營運資料，包括入流量、出流量、蓄水量、集水區降雨量等資訊。支援查詢特定水庫（如阿公店、曾文、石門水庫）、比較不同水庫營運數據、分析集水區降雨與水情狀況。"
version: "1.0.0"
---

# 水利署水庫每日營運狀況 API Skill

## 描述
此 skill 提供存取經濟部水利署開放資料平台的水庫每日營運狀況 API，可查詢台灣各水庫與堰壩的每日營運資料，包括入流量、出流量、蓄水量、集水區降雨量等資訊。涵蓋全台 69 座水庫與堰壩。

## 觸發條件
當用戶需要：
- 查詢水庫每日營運狀況
- 了解水庫入流量與出流量
- 查詢水庫蓄水容量
- 分析水庫集水區降雨量
- 比較不同水庫的營運數據
- 查詢特定水庫（如阿公店水庫、曾文水庫、石門水庫等）的營運資料

## API 基本資訊

### Base URL
```
https://opendata.wra.gov.tw/api/v2
```

### 無需 API Key
水利署開放資料平台**不需要 API Key**，可直接存取。

## 水庫每日營運狀況 API

### 端點
```
GET /api/v2/51023e88-4c76-4dbc-bbb9-470da690d539
```

### 完整 URL
```
https://opendata.wra.gov.tw/api/v2/51023e88-4c76-4dbc-bbb9-470da690d539
```

### 查詢參數
| 參數 | 類型 | 必填 | 說明 |
|------|------|------|------|
| page | integer | 否 | 頁碼 (1..N)，預設值: 1 |
| size | integer | 否 | 每頁筆數，上限 1000，預設值: 1000 |

### 回應欄位說明
| 欄位名稱 | 說明 | 單位 |
|----------|------|------|
| `reservoiridentifier` | 水庫識別碼 | - |
| `reservoirname` | 水庫名稱 | - |
| `datetime` | 資料日期時間 | ISO 8601 格式 |
| `capacity` | 蓄水容量 | 萬立方公尺 |
| `inflow` | 入流量 | 萬立方公尺/日 |
| `outflow` | 出流量 | 萬立方公尺/日 |
| `outflowtotal` | 總出流量 | 萬立方公尺/日 |
| `crossflow` | 越域引水量 | 萬立方公尺/日 |
| `basinrainfall` | 集水區降雨量 | 毫米 (mm) |
| `dwl` | 呆水位 | 公尺 (m) |
| `nwlmax` | 最高正常蓄水位 | 公尺 (m) |
| `outflowdischarge` | 放流量 | - |
| `regulatorydischarge` | 調節性放流量 | - |

### 回應範例
```json
[
  {
    "reservoiridentifier": "10201",
    "reservoirname": "阿公店水庫",
    "datetime": "2026-01-21T00:00:00",
    "capacity": "1680.5",
    "inflow": "2.35",
    "outflow": "1.20",
    "outflowtotal": "3.55",
    "crossflow": "0.0",
    "basinrainfall": "0.0",
    "dwl": "25.0",
    "nwlmax": "40.0",
    "outflowdischarge": "",
    "regulatorydischarge": ""
  }
]
```

## 使用範例

### 範例 1: cURL 快速查詢
```bash
# 獲取所有水庫每日營運狀況
curl -s "https://opendata.wra.gov.tw/api/v2/51023e88-4c76-4dbc-bbb9-470da690d539" | jq

# 獲取前10筆資料
curl -s "https://opendata.wra.gov.tw/api/v2/51023e88-4c76-4dbc-bbb9-470da690d539?size=10" | jq
```

### 範例 2: Python 查詢所有水庫營運狀況
```python
import requests
from typing import List, Dict, Any

API_URL = "https://opendata.wra.gov.tw/api/v2/51023e88-4c76-4dbc-bbb9-470da690d539"

def get_all_reservoir_operations() -> List[Dict[str, Any]]:
    """獲取所有水庫每日營運狀況"""
    response = requests.get(API_URL, params={"size": 1000}, timeout=30)
    response.raise_for_status()
    return response.json()

# 使用範例
operations = get_all_reservoir_operations()
print(f"共有 {len(operations)} 座水庫/堰壩的營運資料")

# 顯示前5筆
for op in operations[:5]:
    print(f"- {op['reservoirname']}: 蓄水量 {op.get('capacity', 'N/A')} 萬m³")
```

### 範例 3: Python 查詢特定水庫營運狀況
```python
import requests
from typing import List, Dict, Any, Optional

API_URL = "https://opendata.wra.gov.tw/api/v2/51023e88-4c76-4dbc-bbb9-470da690d539"

def get_reservoir_operation(reservoir_name: str) -> Optional[Dict[str, Any]]:
    """查詢特定水庫的營運狀況"""
    response = requests.get(API_URL, params={"size": 1000}, timeout=30)
    response.raise_for_status()
    
    for op in response.json():
        if reservoir_name in op.get('reservoirname', ''):
            return op
    return None

# 使用範例：查詢阿公店水庫
agongdian = get_reservoir_operation("阿公店")
if agongdian:
    print(f"【{agongdian['reservoirname']}】")
    print(f"  資料日期: {agongdian['datetime']}")
    print(f"  蓄水容量: {agongdian.get('capacity', 'N/A')} 萬m³")
    print(f"  入流量: {agongdian.get('inflow', 'N/A')} 萬m³/日")
    print(f"  出流量: {agongdian.get('outflow', 'N/A')} 萬m³/日")
    print(f"  集水區降雨: {agongdian.get('basinrainfall', 'N/A')} mm")
```

### 範例 4: Python 查詢蓄水量最大的水庫
```python
import requests
from typing import List, Dict, Any

API_URL = "https://opendata.wra.gov.tw/api/v2/51023e88-4c76-4dbc-bbb9-470da690d539"

def get_top_reservoirs_by_capacity(top_n: int = 10) -> List[Dict[str, Any]]:
    """獲取蓄水量最大的水庫"""
    response = requests.get(API_URL, params={"size": 1000}, timeout=30)
    response.raise_for_status()
    
    data = response.json()
    # 過濾有蓄水量資料的水庫並排序
    with_capacity = [d for d in data if d.get('capacity') and d['capacity'] != '']
    sorted_data = sorted(with_capacity, 
                        key=lambda x: float(x['capacity']), 
                        reverse=True)
    return sorted_data[:top_n]

# 使用範例
top_reservoirs = get_top_reservoirs_by_capacity(10)
print("=== 蓄水量前10大水庫 ===")
for i, r in enumerate(top_reservoirs, 1):
    capacity = float(r['capacity'])
    print(f"{i}. {r['reservoirname']}: {capacity:,.2f} 萬m³ ({capacity/100:.2f} 百萬m³)")
```

### 範例 5: Python 查詢有降雨的水庫
```python
import requests
from typing import List, Dict, Any

API_URL = "https://opendata.wra.gov.tw/api/v2/51023e88-4c76-4dbc-bbb9-470da690d539"

def get_reservoirs_with_rainfall() -> List[Dict[str, Any]]:
    """獲取集水區有降雨的水庫"""
    response = requests.get(API_URL, params={"size": 1000}, timeout=30)
    response.raise_for_status()
    
    data = response.json()
    return [d for d in data 
            if d.get('basinrainfall') and float(d['basinrainfall']) > 0]

# 使用範例
rainy_reservoirs = get_reservoirs_with_rainfall()
if rainy_reservoirs:
    print(f"共有 {len(rainy_reservoirs)} 座水庫集水區有降雨：")
    for r in rainy_reservoirs:
        print(f"  - {r['reservoirname']}: {r['basinrainfall']} mm")
else:
    print("目前無水庫集水區有降雨")
```

### 範例 6: JavaScript/Node.js 範例
```javascript
async function getReservoirOperation(reservoirName = null) {
    const url = 'https://opendata.wra.gov.tw/api/v2/51023e88-4c76-4dbc-bbb9-470da690d539';
    
    const response = await fetch(`${url}?size=1000`);
    if (!response.ok) throw new Error(`HTTP error: ${response.status}`);
    
    let data = await response.json();
    
    if (reservoirName) {
        data = data.filter(d => 
            d.reservoirname && d.reservoirname.includes(reservoirName)
        );
    }
    
    return data;
}

// 使用範例：查詢曾文水庫
getReservoirOperation('曾文').then(ops => {
    if (ops.length > 0) {
        const op = ops[0];
        console.log(`${op.reservoirname} 營運狀況：`);
        console.log(`  蓄水量: ${op.capacity} 萬m³`);
        console.log(`  入流量: ${op.inflow} 萬m³/日`);
    }
});
```

## 台灣主要水庫列表

| 水庫名稱 | 水庫識別碼 | 所在地區 |
|----------|------------|----------|
| 石門水庫 | 10101 | 桃園市 |
| 翡翠水庫 | 10102 | 新北市 |
| 曾文水庫 | 10301 | 台南市/嘉義縣 |
| 南化水庫 | 10302 | 台南市 |
| 阿公店水庫 | 10201 | 高雄市 |
| 德基水庫 | 10401 | 台中市 |
| 日月潭水庫 | 10501 | 南投縣 |
| 鯉魚潭水庫 | 10402 | 苗栗縣 |
| 牡丹水庫 | 10601 | 屏東縣 |
| 湖山水庫 | 10701 | 雲林縣 |

## 相關水庫 API 端點

| 資料集名稱 | API 端點 UUID | 說明 |
|------------|---------------|------|
| **水庫每日營運狀況** | `51023e88-4c76-4dbc-bbb9-470da690d539` | **本 Skill 使用** |
| 水庫水情資料 | `2be9044c-6e44-4856-aad5-dd108c2e6679` | 即時水情 |
| 阿公店水庫即時水情 | `ecc4ce8d-0942-474a-8705-53e9aaa7c4e8` | 阿公店專用 |
| 曾文水庫即時水情 | `598befe9-a6fe-4126-a8cc-52ccbbecfc68` | 曾文專用 |
| 牡丹水庫即時水情 | `6d7ba910-b627-4844-882b-df232064db0c` | 牡丹專用 |
| 石門水庫濁度資料 | `7cd352ef-6518-4396-b2d6-61f1946a5611` | 石門濁度 |

## 注意事項
1. 水利署 API **無需 API Key**，可直接存取
2. 資料為每日營運統計，非即時資料
3. 部分欄位可能為空字串（表示該水庫無此項目資料）
4. capacity 單位為「萬立方公尺」，需換算為百萬立方公尺時除以 100
5. 資料以 JSON 格式回傳
6. size 參數上限為 1000 筆
7. 不同水庫的資料完整度可能不同（部分小型水庫資料較少）
