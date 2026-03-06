# API 端點參考文件

## 目錄
1. [政府資料開放平臺](#政府資料開放平臺)
2. [標案資料 API](#標案資料-api)
3. [新北市開放資料 API](#新北市開放資料-api)
4. [臺中市開放資料 API](#臺中市開放資料-api)
5. [臺北市開放資料 API](#臺北市開放資料-api)

---

## 政府資料開放平臺

### 大宗資材價格 CSV 下載

**端點**: `https://pcic.pcc.gov.tw/pwc-web/api/service/opendata-file/document/大宗資材及其漲跌幅彙整表.csv`

**方法**: GET

**認證**: 無需認證

**回應格式**: CSV

**範例請求**:
```bash
curl -X GET "https://pcic.pcc.gov.tw/pwc-web/api/service/opendata-file/document/大宗資材及其漲跌幅彙整表.csv" \
  -H "Accept: text/csv"
```

**回應欄位**:
| 欄位 | 類型 | 說明 |
|------|------|------|
| 調查項目 | string | 材料名稱 |
| 調查地區 | string | 地理區域 |
| 單位 | string | 計價單位 |
| 114.8價格(A) | number | 當期價格 |
| 109.03價格(C) | number | 基準期價格 |
| 半年漲跌 | percentage | 半年漲跌幅 |
| 108.09價格(D) | number | 去年同期價格 |
| 一年漲跌 | percentage | 一年漲跌幅 |
| 107.09價格(E) | number | 兩年前同期價格 |
| 兩年漲跌 | percentage | 兩年漲跌幅 |

---

## 標案資料 API

### 基本資訊

**基礎網址**: `https://pcc.g0v.ronny.tw`

**CORS**: 開放

**授權**: 政府採購網著作權聲明

### 前端展示

**網址**: https://ronnywang.github.io/pcc-viewer/index.html

### GitHub 原始碼

- **後端 API**: https://github.com/ronnywang/pcc.g0v.ronny.tw
- **前端展示**: https://github.com/ronnywang/pcc-viewer

---

## 新北市開放資料 API

### 營造工程物價指數

**端點**: `https://data.ntpc.gov.tw/api/datasets/9d0483b6-513a-46b2-92e3-5f9b315999bb/{format}`

**支援格式**:
- JSON: `/json`
- CSV: `/csv`
- XML: `/xml`

**方法**: GET

**認證**: 無需認證

**查詢參數**:
| 參數 | 類型 | 說明 | 預設值 |
|------|------|------|--------|
| page | integer | 頁碼 | 1 |
| size | integer | 每頁筆數 | 1000 |

**範例請求**:
```bash
# JSON 格式
curl -X GET "https://data.ntpc.gov.tw/api/datasets/9d0483b6-513a-46b2-92e3-5f9b315999bb/json?page=1&size=10"

# CSV 格式
curl -X GET "https://data.ntpc.gov.tw/api/datasets/9d0483b6-513a-46b2-92e3-5f9b315999bb/csv"
```

**回應範例 (JSON)**:
```json
[
  {
    "年_月": "2024_01",
    "總指數原始值": "112.35",
    "總指數年增率_百分比_": "3.2"
  }
]
```

---

## 臺中市開放資料 API

### API 文件

**Swagger UI**: https://datacenter.taichung.gov.tw/swagger/api-docs/387200000A

**Swagger YAML**: https://datacenter.taichung.gov.tw/swagger/yaml/387200000A

### 營造工程物價指數

**資料集 ID**: 21141-00-01-2

**方法**: GET

**認證**: 無需認證

**回應格式**: JSON

### 建築改良物標準單價表

**資料集 ID**: 4691fbef-17a0-46b7-a264-826849525bd5

**支援格式**:
- JSON
- XML
- CSV

**範例請求**:
```bash
# 建築改良物標準單價表 - JSON
curl -X GET "https://datacenter.taichung.gov.tw/api/4691fbef-17a0-46b7-a264-826849525bd5/json"

# 建築改良物標準單價表 - CSV
curl -X GET "https://datacenter.taichung.gov.tw/api/4691fbef-17a0-46b7-a264-826849525bd5/csv"
```

**回應欄位 (建築改良物)**:
| 欄位 | 類型 | 說明 |
|------|------|------|
| 編號 | string | 項目編號 |
| 機關代碼 | string | 機關代碼 |
| 構造類別 | string | 建築構造類別 |
| 地上樓層數 | integer | 樓層數 |
| 標準單價-元每平方公尺 | number | 每平方公尺單價 |

---

## 臺北市開放資料 API

### 資料大平臺

**網址**: https://data.taipei

### 營造工程物價總指數

**資料集 ID**: 80dd61cf-0b21-4ed5-80bf-d5c2817c5292

**格式**: CSV

**下載網址**: 
```
https://data.taipei/api/v1/dataset/80dd61cf-0b21-4ed5-80bf-d5c2817c5292?scope=resourceAquire
```

### 常用工程基本單價

**資料集 ID**: 147067

**格式**: XML

**下載方式**: 透過政府資料開放平臺下載

---

## 資料集對照表

| 資料來源 | 資料集名稱 | 資料集 ID | 格式 | 更新頻率 |
|---------|-----------|-----------|------|---------|
| 行政院工程會 | 大宗資材價格彙整表 | 7374 | CSV | 每月 |
| 行政院工程會 | 鋼板價格調查 | 6578 | CSV | 每月 |
| 行政院工程會 | 砂石價格調查 | 6818 | CSV | 每月 |
| 行政院工程會 | 鋼筋價格調查 | 6820 | CSV | 每月 |
| 行政院工程會 | H型鋼價格調查 | 6577 | CSV | 每月 |
| 行政院工程會 | 混凝土價格調查 | 6819 | CSV | 每月 |
| 新北市政府 | 營造工程物價指數 | 9d0483b6-513a-46b2-92e3-5f9b315999bb | JSON/CSV/XML | 每月 |
| 臺中市政府 | 營造工程物價指數 | 21141-00-01-2 | JSON/CSV | 不定期 |
| 臺中市政府 | 建築改良物標準單價表 | 4691fbef-17a0-46b7-a264-826849525bd5 | JSON/XML/CSV | 不定期 |
| 臺北市政府 | 營造工程物價總指數 | 80dd61cf-0b21-4ed5-80bf-d5c2817c5292 | CSV | 每月 |
| 臺北市政府 | 常用工程基本單價 | 147067 | XML | 每半年 |

---

## 錯誤處理

### 常見 HTTP 狀態碼

| 狀態碼 | 說明 | 處理建議 |
|--------|------|---------|
| 200 | 成功 | 正常處理回應資料 |
| 400 | 錯誤請求 | 檢查請求參數格式 |
| 404 | 找不到資源 | 檢查資料集 ID 是否正確 |
| 429 | 請求過多 | 降低請求頻率，加入延遲 |
| 500 | 伺服器錯誤 | 稍後再試或聯繫資料提供機關 |

### 錯誤回應格式

```json
{
  "error": {
    "code": "DATASET_NOT_FOUND",
    "message": "指定的資料集不存在",
    "details": "請確認資料集 ID 是否正確"
  }
}
```
