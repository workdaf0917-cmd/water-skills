# 台灣水利署水權統計資料 API Skill

## 概述

此 Skill 提供台灣經濟部水利署水權統計資料 API 的完整使用指南，包含資料查詢、分析範例及實際應用場景。

## 功能特色

### 📊 資料查詢
- 取得全台水權統計資料
- 查詢特定縣市的水權分布
- 篩選不同用水標的（農業、工業、民生等）
- 分析各月份引水量變化

### 🔍 資料分析
- 統計各縣市水權件數
- 分析用水趨勢
- 比較不同地區用水模式
- 製作水權統計報表

### 💻 程式範例
- Python 完整使用範例
- JavaScript/Node.js 範例
- curl 命令列範例
- pandas 資料分析範例

### 📈 應用場景
- 水資源管理分析
- 用水趨勢預測
- 水權資料匯出
- 即時監控儀表板

## API 資訊

**端點**: `https://opendata.wra.gov.tw/api/v2/03be73eb-5da8-45d4-87d9-4e78d476a843`

**方法**: GET

**回傳格式**: JSON

**認證**: 無需認證（開放資料）

## 資料欄位

每筆水權記錄包含：
- 序號、統計年月
- 主管機關
- 引水地點縣市
- 水權狀類別
- 水源類別與支流
- 用水標的
- 12 個月份的引水量（立方公尺）

## 快速開始

### Python 基本範例

```python
import requests

# 取得所有水權資料
url = "https://opendata.wra.gov.tw/api/v2/03be73eb-5da8-45d4-87d9-4e78d476a843"
response = requests.get(url)
data = response.json()

print(f"共有 {len(data)} 筆水權資料")

# 篩選台北市的水權
taipei_data = [
    record for record in data 
    if record.get('countyofchanneledwaterloation') == '臺北市'
]
print(f"台北市水權: {len(taipei_data)} 件")
```

### 統計分析範例

```python
from collections import Counter

# 統計各用水標的
purposes = [record.get('waterconsumptionpurpose') for record in data]
purpose_count = Counter(purposes)

for purpose, count in purpose_count.most_common():
    print(f"{purpose}: {count} 件")
```

## 檔案結構

```
wra-water-rights/
├── SKILL.md                    # 主要技能文件
├── references/
│   ├── api_reference.md        # 完整 API 參考文件
│   └── index.md                # 參考索引
└── README.md                   # 本說明文件
```

## 使用方式

### 1. 上傳至 Claude

1. 前往 https://claude.ai/skills
2. 點擊「Upload Skill」
3. 選擇 `wra-water-rights.zip`
4. 完成上傳

### 2. 在對話中使用

直接詢問 Claude 關於水權資料的問題，例如：

- "幫我查詢台北市的水權資料"
- "分析各縣市的用水量分布"
- "製作一個水權統計報表"
- "如何使用水利署 API 取得資料？"

## 參考文件

### SKILL.md
主要技能文件，包含：
- 使用情境說明
- 快速開始指南
- 常見查詢範例
- 實用程式碼範例
- 最佳實踐建議

### references/api_reference.md
完整 API 參考文件，包含：
- API 端點詳細說明
- 完整資料欄位定義
- Python、JavaScript、curl 範例
- 實際應用場景
- 資料分析與視覺化範例

## 應用範例

### 1. 水資源管理分析

```python
import pandas as pd

# 轉換為 DataFrame
df = pd.DataFrame(data)

# 各縣市水權統計
county_stats = df.groupby('countyofchanneledwaterloation').agg({
    'serialnumber': 'count',
    'quantityofchanneledwaterinmonthjanuary': 'sum'
})
```

### 2. 匯出為 Excel

```python
df = pd.DataFrame(data)
df.to_excel('water_rights.xlsx', index=False)
```

### 3. 資料快取

```python
import json
from datetime import datetime, timedelta

def get_cached_data(cache_file='cache.json', max_age_hours=24):
    # 實作快取邏輯
    # 詳見 SKILL.md
    pass
```

## 資料特性

- **更新頻率**: 每月更新
- **資料規模**: 數千筆水權記錄
- **涵蓋範圍**: 全台各縣市
- **資料品質**: 官方核准的正式水權資料
- **編碼格式**: UTF-8，支援繁體中文

## 注意事項

1. **無需認證**: 此為開放 API，無需申請 API Key
2. **使用限制**: 請合理使用，避免過度頻繁請求
3. **資料授權**: 遵循政府資料開放授權條款
4. **資料時效**: 建議定期更新以確保資料最新

## 相關資源

- **API 文件**: https://opendata.wra.gov.tw/openapi/swagger/index.html
- **水利署開放資料平台**: https://opendata.wra.gov.tw/
- **水利署官網**: https://www.wra.gov.tw/

## 技術支援

如有問題或建議，請參考：
- 水利署開放資料平台說明
- API 文件中的常見問題
- Skill 內建的範例程式碼

## 版本資訊

- **版本**: 1.0
- **建立日期**: 2026-01-24
- **資料來源**: 經濟部水利署開放資料平台
- **Skill 類型**: API 參考與使用指南

## 授權

本 Skill 文件遵循 MIT License。

資料來源為經濟部水利署開放資料，請遵循政府資料開放授權條款使用。

---

**製作工具**: Skill Seeker  
**最後更新**: 2026-01-24
