# 總體統計資料庫 API 參考指南

## API 端點

### 完整資料集下載（推薦）
```
GET https://nstatdb.dgbas.gov.tw/dgbasAll/webMain.aspx?sdmx/{功能代碼}
```
- 回傳 API-JSON 格式
- 包含所有維度項目與全部統計期間
- 適合客戶端篩選

### 帶維度篩選查詢
```
GET https://nstatdb.dgbas.gov.tw/dgbasAll/webMain.aspx?sdmx/{功能代碼}/{篩選式}.{週期}&startTime={起始}&endTime={結束}
```
- 維度間以 `.` 分隔，同維度項目以 `+` 串接
- 週期代碼：`A`（年）、`Q`（季）、`M`（月）
- 時間格式：`2024`（年）、`2024-M1`（月）、`2024-Q1`（季）
- **注意**：部分資料表此格式回傳 HTML，需改用完整下載模式

### 元資料查詢（HTML）
```
GET https://nstatdb.dgbas.gov.tw/dgbasAll/webMain.aspx?sys=210&funid={功能代碼}
```

## 查詢限制

- URL 長度上限：1,000 字元
- 匿名查詢，無需 API Key
- 無明確頻率限制，建議適度控制
- 單次僅能查詢單一功能代碼

## API-JSON 結構

### 完整結構
```json
{
  "meta": {
    "id": "唯一識別碼",
    "prepared": "2026-02-22 14:00:00",
    "sender": {"id": "dgbas", "name": "行政院主計總處"},
    "links": [{"href": "API URL", "rel": "request"}]
  },
  "data": {
    "dataSets": [{
      "action": "Information",
      "series": {
        "0:0": {"observations": {"0": [數值], "1": [數值]}},
        "0:1": {"observations": {"0": [數值], "1": [數值]}},
        "1:0": {"observations": {"0": [數值], "1": [數值]}}
      }
    }],
    "structure": {
      "links": [...],
      "name": "資料表名稱",
      "dimensions": {
        "series": [
          {
            "name": "維度名稱",
            "keyPosition": 0,
            "values": [
              {"id": "1", "name": "項目1"},
              {"id": "2", "name": "項目2"}
            ]
          }
        ],
        "observation": [
          {
            "name": "統計期",
            "values": [
              {"id": "2020", "name": "109年"},
              {"id": "2020-M1", "name": "109年1月"}
            ]
          }
        ]
      }
    }
  }
}
```

### Series Key 規則
- 格式：`{dim0_idx}:{dim1_idx}:...`
- 所有索引皆為 **0-based**
- 索引順序對應 `structure.dimensions.series` 陣列中各維度的 `values` 排列順序
- 範例：2 個維度（產業別 46 項、性別 3 項）→ series key `0:0` 到 `45:2`

### Observation Key 規則
- 格式：0-based 索引字串（如 `"0"`, `"1"`, `"688"`）
- 對應 `structure.dimensions.observation[0].values` 中同索引的時間期項目

### 注意事項
- `structure` 欄位可能位於 `data.structure`（實測）或頂層 `structure`
- 部分早期統計期數值可能為 `null`
- 功能代碼格式：`A` + 9 位數字（如 `A046201010`）

## 統計期格式

| 類型 | id 格式 | name 範例 |
|------|---------|----------|
| 年 | `2024` | 113年 |
| 月 | `2024-M1` ~ `2024-M12` | 113年1月 |
| 季 | `2024-Q1` ~ `2024-Q4` | 113年第1季 |

## 維度篩選語法（帶篩選模式）

```
維度1項目.維度2項目.維度3項目.週期
```

- 項目以數字編碼（1-based），如 `1+2+3` 選擇前三項
- 留空表示全選，如 `1..M` 表示維度1選第1項、維度2全選、月資料
- 範例：`A040101020/1+2.1..M&startTime=2022-M1&endTime=2022-M12`
  - 維度1（統計項）：1+2（勞動力+就業者）
  - 維度2（性別）：1（合計）
  - 維度3（教育程度）：全選
  - 週期：M（月）
