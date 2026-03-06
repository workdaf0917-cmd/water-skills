---
name: nstat-salary-query
description: 查詢行政院主計總處總體統計資料庫「每人每月總薪資」(A046201010)，支援依產業別、性別、統計期篩選
---

# 總體統計資料庫薪資查詢 Skill

## 描述
此 Skill 提供存取行政院主計總處「總體統計資料庫」API，查詢「A046201010 每人每月總薪資」統計表之能力。可依產業別、性別、統計期間進行篩選，輸出格式化薪資數據。

## 觸發條件
當用戶需要：
- 查詢台灣各產業每人每月總薪資
- 比較不同產業別的薪資水準
- 分析薪資趨勢（年度或月度）
- 查詢特定性別之薪資統計
- 取得工業及服務業薪資數據

## API 基本資訊

### Base URL
```
https://nstatdb.dgbas.gov.tw/dgbasAll/webMain.aspx?sdmx/
```

### 功能代碼
```
A046201010（每人每月總薪資）
```

### 驗證方式
匿名查詢，無需 API Key。

### URL 長度限制
1,000 字元以內。

## 查詢方式

### 1. 完整資料集下載（推薦）
```
https://nstatdb.dgbas.gov.tw/dgbasAll/webMain.aspx?sdmx/A046201010
```
- 回傳 API-JSON 格式（約 1.3 MB）
- 包含所有產業別、性別、及全部統計期間（1973年至今）
- **注意**：帶有維度篩選的 URL 格式（如 `$1.1.M&startTime=...`）目前僅回傳 HTML 頁面而非 JSON，因此建議下載完整資料集後在客戶端篩選。

### 2. 元資料結構查詢
```
https://nstatdb.dgbas.gov.tw/dgbasAll/webMain.aspx?sys=210&funid=A046201010
```
- 回傳 HTML 頁面，顯示統計項與複分類之樹狀結構

## 資料結構

### 維度 1：產業別 (keyPosition=0)
共 46 項，主要分類如下：

| id | 產業別 |
|----|--------|
| 1 | 工業及服務業 |
| 2 | 工業部門 |
| 4 | 製造業 |
| 22 | 電子零組件製造業 |
| 32 | 用水供應及污染整治業 |
| 33 | 營建工程業 |
| 34 | 服務業部門 |
| 35 | 批發及零售業 |
| 37 | 住宿及餐飲業 |
| 38 | 出版、影音製作、傳播及資通訊服務業 |
| 39 | 金融及保險業 |
| 41 | 專業、科學及技術服務業 |

### 維度 2：性別 (keyPosition=1)

| id | 性別 |
|----|------|
| 1 | 合計 |
| 2 | 男 |
| 3 | 女 |

### 統計期 (observation)
- 資料範圍：1973年（民國62年）至今
- 週期類型：年 (A) 及月 (M)
- 格式：`2024` 為年資料、`2024-M1` ~ `2024-M12` 為月資料
- 數值單位：**新台幣元**

## API-JSON 回應格式

回應結構包含三部分：
1. **meta**：查詢時間、資料產製者、API URL
2. **data.dataSets[0].series**：時間數列資料，key 格式為 `dim0_index:dim1_index`（0-based），每個 series 的 observations key 為時間期序號（0-based）
3. **data.structure.dimensions**：維度定義與項目清單

### Series Key 對應規則
- `"0:0"` → 產業別 id=1（工業及服務業）、性別 id=1（合計）
- `"0:1"` → 產業別 id=1（工業及服務業）、性別 id=2（男）
- `"0:2"` → 產業別 id=1（工業及服務業）、性別 id=3（女）
- `"3:0"` → 產業別 id=4（製造業）、性別 id=1（合計）
- 以此類推

### Observation Key 對應規則
- observations 的 key 為 0-based 索引，對應 `data.structure.dimensions.observation[0].values` 中同索引的時間期

## 工作流程

### 步驟 1：下載完整資料集
呼叫 `scripts/query_nstat.py` 下載並解析 A046201010 完整資料。

### 步驟 2：篩選與格式化
依用戶指定的產業別、性別、時間範圍進行客戶端篩選。

### 步驟 3：輸出結果
以 Markdown 表格或 JSON 格式輸出薪資數據，包含：
- 產業別名稱
- 性別
- 統計期（年份/月份）
- 每人每月總薪資（NT$）

## 腳本使用方式

```bash
# 查詢工業及服務業 2024 年月薪資（合計）
python scripts/query_nstat.py --industry 1 --gender 1 --start 2024-M1 --end 2024-M12

# 查詢電子零組件製造業 2020~2024 年度薪資
python scripts/query_nstat.py --industry 22 --gender 1 --start 2020 --end 2024

# 列出所有可用產業別
python scripts/query_nstat.py --list-industries

# 輸出 JSON 格式
python scripts/query_nstat.py --industry 1 --gender 1 --start 2024-M1 --end 2024-M12 --format json
```

## 注意事項
1. 完整資料集約 1.3 MB，建議快取以提升效能
2. 數值單位為新台幣「元」
3. 部分早期資料可能缺漏（顯示為 null）
4. 資料更新頻率依主計總處公告為準（通常每月更新）
5. API 為匿名查詢，無頻率限制但建議適度控制請求頻率
