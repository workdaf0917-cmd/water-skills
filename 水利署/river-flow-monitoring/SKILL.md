---
name: river-flow-monitoring
description: "水利署河川流量與即時水位監測：整合經濟部水利署開放資料平台的河川流量測站站況 API 與即時水位資料 API，查詢測站基本資料（名稱、位置、警戒水位等）與各測站即時水位數據（每10分鐘更新）。"
version: "1.0.0"
---

# 水利署河川流量與即時水位監測 API Skill

## 描述
此 skill 整合經濟部水利署開放資料平台的兩個 API：
1. **河川流量測站站況 API** - 查詢測站基本資料（名稱、位置、警戒水位等）
2. **即時水位資料 API** - 查詢各測站的即時水位數據（每10分鐘更新）

## 觸發條件
當用戶需要：
- 查詢河川流量測站基本資料
- 獲取特定河川的監測站資訊
- 了解河川警戒水位設定
- **查詢河川即時水位**
- **監測特定測站的水位變化**
- 分析河川監測站分布情況

## API 基本資訊

### Base URL
```
https://opendata.wra.gov.tw/api/v2
```

### 無需 API Key
水利署開放資料平台**不需要 API Key**，可直接存取。

## 河川流量測站站況 API

### 端點
```
GET /api/v2/9332bd66-0213-4380-a5d5-a43e7be49255
```

### 完整 URL
```
https://opendata.wra.gov.tw/api/v2/9332bd66-0213-4380-a5d5-a43e7be49255
```

### 查詢參數
| 參數 | 類型 | 必填 | 說明 |
|------|------|------|------|
| page | integer | 否 | 頁碼 (1..N)，預設值: 1 |
| size | integer | 否 | 每頁筆數，上限 1000，預設值: 1000 |

### 主要回應欄位說明
| 欄位名稱 | 說明 |
|----------|------|
| `observatoryidentifier` | 測站識別碼 |
| `observatoryname` | 測站中文名稱 |
| `englishname` | 測站英文名稱 |
| `rivername` | 河川中文名稱 |
| `englishrivername` | 河川英文名稱 |
| `affiliatedbasin` | 所屬流域代碼 |
| `basinidentifier` | 流域識別碼 |
| `locationaddress` | 測站地址 |
| `englishaddress` | 測站英文地址 |
| `locationbytwd97_xy` | TWD97 座標 (X Y) |
| `alertlevel1` | 一級警戒水位 (公尺) |
| `alertlevel2` | 二級警戒水位 (公尺) |
| `alertlevel3` | 三級警戒水位 (公尺) |
| `elevationofwaterlevelzeropoint` | 水尺零點標高 (公尺) |
| `watershedarea` | 集水區面積 (平方公里) |
| `observationstatus` | 觀測現況 (現存/廢站) |
| `obervationitems` | 觀測項目代碼 |
| `equipmentstatus` | 設備狀態代碼 |
| `crossriverstructuresnameofequipment` | 設置之橋樑或構造物名稱 |

### 觀測項目代碼說明
| 代碼 | 說明 |
|------|------|
| 0 | 水位 |
| 1 | 流量 |
| 0,1 | 水位+流量 |

### 設備狀態代碼說明
| 代碼 | 說明 |
|------|------|
| 1 | 正常 |
| 2 | 故障 |
| 3 | 維修中 |

### 回應範例
```json
[
  {
    "observatoryidentifier": "3132005RV1140H102",
    "observatoryname": "虎寮潭橋站",
    "englishname": "Huliaotan",
    "rivername": "北勢溪",
    "englishrivername": "Beishi River",
    "affiliatedbasin": "1140",
    "basinidentifier": "1140H102",
    "locationaddress": "新北市坪林區虎寮潭橋",
    "englishaddress": "Hu Liao Tan Bridge, Pinglin Dist., New Taipei City",
    "locationbytwd97_xy": "324793.74 2760427.71",
    "alertlevel1": "",
    "alertlevel2": "",
    "alertlevel3": "",
    "elevationofwaterlevelzeropoint": "203.54",
    "watershedarea": "0.92",
    "observationstatus": "現存",
    "obervationitems": "0,1",
    "equipmentstatus": "1",
    "crossriverstructuresnameofequipment": "虎寮潭橋站"
  }
]
```

## 使用範例

### 範例 1: cURL 快速查詢
```bash
# 獲取所有河川流量測站資料
curl -s "https://opendata.wra.gov.tw/api/v2/9332bd66-0213-4380-a5d5-a43e7be49255" | jq

# 獲取前10筆測站資料
curl -s "https://opendata.wra.gov.tw/api/v2/9332bd66-0213-4380-a5d5-a43e7be49255?size=10" | jq
```

### 範例 2: Python 查詢所有流量測站
```python
import requests
from typing import List, Dict, Any, Optional

API_URL = "https://opendata.wra.gov.tw/api/v2/9332bd66-0213-4380-a5d5-a43e7be49255"

def get_all_flow_stations() -> List[Dict[str, Any]]:
    """獲取所有河川流量測站資料"""
    response = requests.get(API_URL, params={"size": 1000}, timeout=30)
    response.raise_for_status()
    return response.json()

# 使用範例
stations = get_all_flow_stations()
print(f"共有 {len(stations)} 個流量測站")

# 顯示前5個測站
for station in stations[:5]:
    print(f"- {station['observatoryname']} ({station['rivername']})")
```

### 範例 3: Python 依河川名稱查詢測站
```python
import requests
from typing import List, Dict, Any

API_URL = "https://opendata.wra.gov.tw/api/v2/9332bd66-0213-4380-a5d5-a43e7be49255"

def search_stations_by_river(river_name: str) -> List[Dict[str, Any]]:
    """依河川名稱搜尋測站"""
    response = requests.get(API_URL, params={"size": 1000}, timeout=30)
    response.raise_for_status()
    
    all_stations = response.json()
    return [s for s in all_stations if river_name in s.get('rivername', '')]

# 使用範例：查詢淡水河流域的測站
stations = search_stations_by_river("淡水河")
print(f"淡水河流域共有 {len(stations)} 個測站")
for s in stations:
    print(f"  - {s['observatoryname']}: {s['locationaddress']}")
```

### 範例 4: Python 查詢有警戒水位設定的測站
```python
import requests
from typing import List, Dict, Any

API_URL = "https://opendata.wra.gov.tw/api/v2/9332bd66-0213-4380-a5d5-a43e7be49255"

def get_stations_with_alert_levels() -> List[Dict[str, Any]]:
    """獲取有設定警戒水位的測站"""
    response = requests.get(API_URL, params={"size": 1000}, timeout=30)
    response.raise_for_status()
    
    all_stations = response.json()
    return [s for s in all_stations 
            if s.get('alertlevel1') or s.get('alertlevel2') or s.get('alertlevel3')]

# 使用範例
alert_stations = get_stations_with_alert_levels()
print(f"共有 {len(alert_stations)} 個測站設有警戒水位")

for s in alert_stations[:5]:
    print(f"\n【{s['observatoryname']}】- {s['rivername']}")
    if s.get('alertlevel1'):
        print(f"  一級警戒: {s['alertlevel1']} m")
    if s.get('alertlevel2'):
        print(f"  二級警戒: {s['alertlevel2']} m")
    if s.get('alertlevel3'):
        print(f"  三級警戒: {s['alertlevel3']} m")
```

### 範例 5: JavaScript/Node.js 範例
```javascript
async function getRiverFlowStations(riverName = null) {
    const url = 'https://opendata.wra.gov.tw/api/v2/9332bd66-0213-4380-a5d5-a43e7be49255';
    
    const response = await fetch(`${url}?size=1000`);
    if (!response.ok) throw new Error(`HTTP error: ${response.status}`);
    
    let stations = await response.json();
    
    // 若有指定河川名稱，進行篩選
    if (riverName) {
        stations = stations.filter(s => 
            s.rivername && s.rivername.includes(riverName)
        );
    }
    
    return stations;
}

// 使用範例
getRiverFlowStations('大漢溪').then(stations => {
    console.log(`大漢溪共有 ${stations.length} 個流量測站`);
    stations.forEach(s => {
        console.log(`- ${s.observatoryname}: ${s.locationaddress}`);
    });
});
```

---

## 即時水位資料 API

### 端點
```
GET /api/v2/73c4c3de-4045-4765-abeb-89f9f9cd5ff0
```

### 完整 URL
```
https://opendata.wra.gov.tw/api/v2/73c4c3de-4045-4765-abeb-89f9f9cd5ff0
```

### 查詢參數
| 參數 | 類型 | 必填 | 說明 |
|------|------|------|------|
| page | integer | 否 | 頁碼 (1..N)，預設值: 1 |
| size | integer | 否 | 每頁筆數，上限 1000，預設值: 1000 |

### 回應欄位說明
| 欄位名稱 | 說明 | 單位 |
|----------|------|------|
| `stationid` | 測站代碼 | - |
| `observatoryidentifier` | 測站識別碼 | - |
| `datetime` | 觀測時間 | ISO 8601 格式 |
| `waterlevel` | 即時水位 | 公尺 (m) |
| `checkresult` | 檢核結果 (1=正常) | - |
| `checkdesc` | 檢核說明 | - |
| `volt` | 電壓 | - |

### 回應範例
```json
[
  {
    "stationid": "1660H009",
    "checkresult": "1",
    "checkdesc": "",
    "observatoryidentifier": "1660H009_API",
    "volt": "",
    "datetime": "2026-01-22T21:20:00",
    "waterlevel": "5.3558"
  }
]
```

### 範例: Python 查詢特定測站即時水位
```python
import requests
from typing import List, Dict, Any, Optional

REALTIME_API_URL = "https://opendata.wra.gov.tw/api/v2/73c4c3de-4045-4765-abeb-89f9f9cd5ff0"

def get_realtime_water_level(station_id: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    獲取即時水位資料
    
    Args:
        station_id: 測站代碼（選填），如 "1660H009"
    
    Returns:
        即時水位資料列表
    """
    response = requests.get(REALTIME_API_URL, params={"size": 1000}, timeout=30)
    response.raise_for_status()
    
    data = response.json()
    
    if station_id:
        data = [d for d in data if station_id in d.get('stationid', '')]
    
    return data

# 使用範例：查詢所有即時水位
all_levels = get_realtime_water_level()
print(f"共有 {len(all_levels)} 筆即時水位資料")

# 使用範例：查詢特定測站
level = get_realtime_water_level("1660H009")
if level:
    print(f"站號: {level[0]['stationid']}")
    print(f"時間: {level[0]['datetime']}")
    print(f"水位: {level[0]['waterlevel']} m")
```

### 範例: Python 結合測站資料與即時水位
```python
import requests

STATION_API = "https://opendata.wra.gov.tw/api/v2/9332bd66-0213-4380-a5d5-a43e7be49255"
REALTIME_API = "https://opendata.wra.gov.tw/api/v2/73c4c3de-4045-4765-abeb-89f9f9cd5ff0"

def get_river_realtime_levels(river_name: str):
    """獲取特定河川的即時水位（含測站名稱）"""
    # 1. 獲取測站基本資料
    stations = requests.get(STATION_API, params={"size": 1000}, timeout=30).json()
    river_stations = {s['basinidentifier']: s for s in stations 
                      if river_name in s.get('rivername', '')}
    
    # 2. 獲取即時水位
    levels = requests.get(REALTIME_API, params={"size": 1000}, timeout=30).json()
    
    # 3. 結合資料
    results = []
    for level in levels:
        station_id = level.get('stationid', '')
        if station_id in river_stations:
            station = river_stations[station_id]
            results.append({
                "測站名稱": station.get('observatoryname'),
                "河川": station.get('rivername'),
                "地址": station.get('locationaddress'),
                "時間": level.get('datetime'),
                "水位": float(level.get('waterlevel', 0))
            })
    
    return results

# 使用範例：查詢二仁溪即時水位
levels = get_river_realtime_levels("二仁溪")
for l in levels:
    print(f"【{l['測站名稱']}】{l['河川']}")
    print(f"  時間: {l['時間']}, 水位: {l['水位']:.2f} m")
```

---

## 相關河川與排水 API 端點

| 資料集名稱 | API 端點 UUID | 說明 |
|------------|---------------|------|
| 河川流量測站站況 | `9332bd66-0213-4380-a5d5-a43e7be49255` | 測站基本資料 |
| **即時水位資料** | `73c4c3de-4045-4765-abeb-89f9f9cd5ff0` | **即時水位（每10分鐘）** |
| 河川水位測站站況 | `c4acc691-7416-40ca-9464-292c0c00da92` | 水位測站基本資料 |
| 甲仙攔河堰即時水情 | `637037ae-d125-4b21-805d-f0d1edb0b553` | 甲仙堰即時資料 |
| 高屏溪河堰即時水情 | `b2b7cbec-ec4a-4d08-ae41-b3b2cf96b99b` | 高屏溪堰即時資料 |

## 台灣主要河川流域代碼

| 流域代碼 | 河川名稱 |
|----------|----------|
| 1140 | 淡水河 |
| 1300 | 頭前溪 |
| 1350 | 後龍溪 |
| 1400 | 大安溪 |
| 1410 | 大甲溪 |
| 1420 | 烏溪 |
| 1430 | 濁水溪 |
| 1510 | 曾文溪 |
| 1520 | 二仁溪 |
| 1540 | 高屏溪 |

## 注意事項
1. 水利署 API **無需 API Key**，可直接存取
2. 資料為測站基本資料，非即時水位/流量資料
3. 若需即時水位資料，請使用「即時水位資料」API (73c4c3de-4045-4765-abeb-89f9f9cd5ff0)
4. size 參數上限為 1000 筆
5. 資料以 JSON 格式回傳
6. 部分測站可能無警戒水位設定（欄位為空字串）
7. observationstatus 欄位顯示測站是否仍在運作（現存/廢站）
