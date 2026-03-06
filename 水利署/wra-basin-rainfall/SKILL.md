---
name: wra-basin-rainfall
description: "水利署集水區雨量查詢：查詢經濟部水利署水資源物聯網平臺之集水區降雨資料，提供全台約352個測站的即時時雨量數據，涵蓋各縣市鄉鎮區，可用於集水區降雨監測與分析。"
version: "1.0.0"
---

# 水利署集水區雨量查詢技能

## 概述
查詢經濟部水利署水資源物聯網（IoW）平臺之集水區降雨資料。此 API 提供全台約 352 個測站的即時時雨量數據，涵蓋各縣市鄉鎮區，可用於集水區降雨監測與分析。

## 資料來源
- **平臺名稱**：水資源物聯網入口網（IoW）
- **管理單位**：經濟部水利署
- **平臺網址**：https://iot.wra.gov.tw/
- **API 文件**：https://iot.wra.gov.tw/swagger/index.html
- **帳號申請**：https://iot.wra.gov.tw/ （需申請高階會員）

## 認證方式

### JWT Bearer Token
此 API 需要 JWT Bearer Token 認證（**僅高階會員可使用**）。

1. 至 https://iot.wra.gov.tw/ 註冊帳號並申請高階會員
2. 登入後取得 JWT Token
3. 將 Token 放入 HTTP Header：`Authorization: Bearer <token>`

> **注意**：Token 有效期約 30 分鐘，過期需重新取得。
> 建議將 Token 存於環境變數 `WRA_IOW_TOKEN`。

## API 端點

### 基礎 URL
```
https://iot.wra.gov.tw
```

### 端點列表
| 端點 | 說明 | 認證 |
|------|------|------|
| `GET /precipitation/basins` | 集水區降雨資料（時雨量） | Bearer Token（高階會員） |
| `GET /precipitation/CwaFormat` | 集水區降雨資料（氣象署雨量格式） | Bearer Token（更高權限） |
| `GET /river/basins` | 水系列表（免驗證） | 無 |

### 請求標頭
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

## 回應結構

### `/precipitation/basins` 回應範例
```json
[
  {
    "IoWStationId": "0557a688-30c7-4d10-bbf4-ad42de6dd0e7",
    "StationId": "A130600WT6400027",
    "Name": "高雄市永安區",
    "CountyCode": "64000",
    "CountyName": "高雄市",
    "TownCode": "64000270",
    "TownName": "永安區",
    "Latitude": 22.825092,
    "Longtiude": 120.2263,
    "AdminName": "水利署",
    "Measurements": [
      {
        "IoWPhysicalQuantityId": "4189a98b-3758-430a-addb-8c9f64fad87c",
        "TimeStamp": "2026-02-26T14:00:00+08:00",
        "Name": "時雨量",
        "SIUnit": "mm",
        "Value": 0.0
      }
    ],
    "HydroStationType": 2
  }
]
```

### 回應欄位說明
| 欄位 | 類型 | 說明 |
|------|------|------|
| `IoWStationId` | string (UUID) | IoW 平臺測站唯一識別碼 |
| `StationId` | string | 測站代碼 |
| `Name` | string | 測站名稱（通常為「縣市＋鄉鎮區」） |
| `CountyCode` | string | 縣市代碼 |
| `CountyName` | string | 縣市名稱 |
| `TownCode` | string | 鄉鎮區代碼 |
| `TownName` | string | 鄉鎮區名稱 |
| `Latitude` | number | 緯度（WGS84） |
| `Longtiude` | number | 經度（WGS84）（注意 API 拼寫為 Longtiude） |
| `AdminName` | string | 管理單位 |
| `Measurements` | array | 觀測值陣列 |
| `Measurements[].TimeStamp` | string | 觀測時間（ISO 8601，台灣時間 +08:00） |
| `Measurements[].Name` | string | 觀測項目名稱（固定為「時雨量」） |
| `Measurements[].SIUnit` | string | 單位（mm） |
| `Measurements[].Value` | number | 時雨量值（毫米） |
| `HydroStationType` | integer | 水文測站類型（2 = 雨量站） |

### `/river/basins` 回應範例（免驗證）
```json
[
  {"Code": "167000", "Name": "阿公店溪"},
  {"Code": "173000", "Name": "高屏溪"}
]
```

## 阿公店水庫集水區相關測站

阿公店水庫位於高雄市燕巢區，集水區涵蓋燕巢區、田寮區。以下為集水區內及鄰近測站：

| 測站名稱 | StationId | 鄉鎮區 | 備註 |
|----------|-----------|--------|------|
| 高雄市燕巢區 | A130600WT6400021 | 燕巢區 | 集水區內（水庫所在地） |
| 高雄市田寮區 | A130600WT6400022 | 田寮區 | 集水區內 |
| 高雄市岡山區 | A130600WT6400019 | 岡山區 | 水庫下游 |
| 高雄市阿蓮區 | A130600WT6400023 | 阿蓮區 | 鄰近 |
| 高雄市橋頭區 | A130600WT6400020 | 橋頭區 | 鄰近 |
| 高雄市大社區 | A130600WT6400016 | 大社區 | 鄰近 |

> **水系代碼**：阿公店溪 = `167000`（可由 `/river/basins` 查得）

## 使用範例

### 範例 1: cURL 查詢
```bash
# 查詢全台集水區時雨量（需 Bearer Token）
curl -s -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  "https://iot.wra.gov.tw/precipitation/basins"

# 查詢水系列表（免驗證）
curl -s "https://iot.wra.gov.tw/river/basins"
```

### 範例 2: Python 查詢集水區雨量
```python
import os
import requests

def get_basin_rainfall(token: str = None):
    """
    查詢全台集水區時雨量

    Args:
        token: JWT Bearer Token，未提供則從環境變數 WRA_IOW_TOKEN 讀取
    """
    if token is None:
        token = os.environ.get("WRA_IOW_TOKEN")
        if not token:
            raise ValueError("請設定環境變數 WRA_IOW_TOKEN 或傳入 token 參數")

    url = "https://iot.wra.gov.tw/precipitation/basins"
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()
    return response.json()

# 使用範例
data = get_basin_rainfall()
print(f"共 {len(data)} 個測站")
for s in data:
    m = s["Measurements"][0]
    print(f"  {s['Name']} | {m['TimeStamp']} | {m['Name']}: {m['Value']} {m['SIUnit']}")
```

### 範例 3: Python 篩選阿公店集水區測站
```python
import os
import requests

AGONGDIAN_TOWNS = ["燕巢區", "田寮區", "岡山區", "阿蓮區"]

def get_agongdian_basin_rainfall(token: str = None):
    """查詢阿公店水庫集水區鄰近測站時雨量"""
    if token is None:
        token = os.environ.get("WRA_IOW_TOKEN")

    url = "https://iot.wra.gov.tw/precipitation/basins"
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()
    data = response.json()

    # 篩選高雄市集水區內測站
    results = [
        s for s in data
        if s.get("CountyName") == "高雄市"
        and s.get("TownName") in AGONGDIAN_TOWNS
    ]

    print("═" * 55)
    print("  阿公店水庫集水區時雨量")
    print("═" * 55)
    for s in results:
        m = s["Measurements"][0]
        print(f"  {s['Name']:12s} | {m['TimeStamp']} | {m['Value']:6.2f} mm")
    print("═" * 55)

    return results

get_agongdian_basin_rainfall()
```

### 範例 4: Python 全台高雨量測站排名
```python
import os
import requests

def get_rainfall_ranking(token: str = None, top_n: int = 10):
    """查詢全台集水區時雨量排名"""
    if token is None:
        token = os.environ.get("WRA_IOW_TOKEN")

    url = "https://iot.wra.gov.tw/precipitation/basins"
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()
    data = response.json()

    ranked = []
    for s in data:
        for m in s.get("Measurements", []):
            if m["Value"] > 0:
                ranked.append({
                    "name": s["Name"],
                    "town": s.get("TownName", ""),
                    "value": m["Value"],
                    "time": m["TimeStamp"]
                })

    ranked.sort(key=lambda x: x["value"], reverse=True)

    print(f"全台時雨量排名 (Top {top_n}):")
    for i, r in enumerate(ranked[:top_n], 1):
        print(f"  {i:2d}. {r['name']:14s} | {r['value']:6.2f} mm | {r['time']}")

    return ranked

get_rainfall_ranking(top_n=10)
```

## 資料特性

### 更新頻率
- 即時更新（約每小時）
- 觀測時間以 ISO 8601 格式呈現（台灣時間 +08:00）

### 資料品質
- 水利署官方物聯網感測資料
- 全台約 352 個測站
- 觀測項目為「時雨量」（mm），即該小時累積降雨量

### 覆蓋範圍
- 全台各縣市鄉鎮區
- 高雄市共 38 個測站
- 阿公店水庫集水區（燕巢區、田寮區）皆有測站

## 注意事項
1. **需要 JWT Token**：至 https://iot.wra.gov.tw/ 註冊高階會員取得
2. **Token 有效期短**：約 30 分鐘，過期需重新登入取得
3. **建議存環境變數**：`WRA_IOW_TOKEN`，勿硬編碼於程式中
4. **API 欄位拼寫**：經度欄位為 `Longtiude`（非 Longitude），使用時注意
5. **資料為即時快照**：每次查詢回傳當下最新一筆時雨量，非歷史序列
6. **歷史資料需求**：若需歷史雨量，建議搭配「水利署阿公店水庫即時水情」技能

## 相關技能
- **氣象署每日雨量**：查詢氣象署署屬測站每日雨量（C-B0025-001 資料集）
- **水利署阿公店水庫即時水情**：查詢水庫即時水位、蓄水量及集水區累積雨量
- **水利署水庫歷史蓄水量**：查詢水庫歷史蓄水量統計資料

## 免驗證端點參考

以下端點不需認證即可使用：

| 端點 | 說明 |
|------|------|
| `GET /river/basins` | 水系列表 |
| `GET /river/stations` | 河川水位站 |
| `GET /groundwaterlevel/stations` | 地下水位站 |
| `GET /erosiondepth/stations` | 沖刷深度站 |
| `GET /cumulativeflow/stations` | 累計流量站 |
| `GET /damstructure/stations` | 堤防結構安全站 |
| `GET /dustemission/stations` | 揚塵站 |
| `GET /watergate/stations` | 閘門站 |

免驗證端點共用查詢參數：`countyCode`, `townCode`, `countyName`, `townName`, `basinName`, `centerLat`, `centerLong`, `radius`
