# 管線工程預算估算器 (Pipeline Budget Estimator)

基於台灣自來水公司「嘉義科學園區供水北線工程-管(一)」預算書資料開發的預算查詢與推估工具。

## 功能特色

- **單價查詢**：快速查詢1000mm管線各施工項目單價
- **預算推估**：依據參考預算書推估不同管徑、長度的工程預算
- **材料計算**：計算CLSM回填、管材數量等工程數量
- **管徑比較**：比較不同管徑的單價差異

## 安裝方式

1. 確保已安裝 Python 3.7+
2. 不需額外套件，純Python標準庫實作
3. 將 `skills/pipeline-budget-estimator` 目錄複製到您的專案

## 快速開始

### 1. 查詢1000mm管線單價

```python
from skills.pipeline_budget_estimator.budget_calculator import PipelineBudgetEstimator

estimator = PipelineBudgetEstimator()

# 查詢所有項目
prices = estimator.query_1000mm_price()

# 查詢特定關鍵字
prices = estimator.query_1000mm_price("埋設")
```

### 2. 推估工程預算

```python
# 推估800mm管線，500公尺，市區施工
result = estimator.estimate_budget(
    length=500,           # 管線長度(M)
    diameter=800,         # 管徑(mm)
    geology="軟質土壤",    # 地質條件
    environment="市區",    # 施工環境
    road_type="一般道路"   # 路面類型
)

print(f"總預算: {result['費用明細(元)']['總計(含稅5%)']:,}元")
```

### 3. 計算單位長度單價

```python
# 計算600mm管徑每公尺單價
unit_price = estimator.calculate_unit_price_per_meter(600)
print(f"每公尺單價: {unit_price['綜合單價(基本項目)']}元/M")
```

### 4. 計算CLSM回填數量

```python
# 計算1000mm管線2000M的CLSM回填
clsm = estimator.calculate_clsm_volume(2000, 1000)
print(f"CLSM體積: {clsm['計算結果']['CLSM回填體積(M³)']}M³")
```

## 主要單價參考（1000mm管線）

### 管材及安裝
| 項目 | 單位 | 單價(元) |
|-----|------|---------|
| 直管埋設 | M | 890 |
| 推進工法 | M | 80,000 |
| 延性鑄鐵管(DIP) | M | 95,800 |

### 接頭相關
| 項目 | 單位 | 單價(元) |
|-----|------|---------|
| 機械接頭(K型) | 口 | 1,850 |
| 機械接頭(K型含配件) | 口 | 9,750 |
| 凸緣接頭(含配件) | 口 | 17,650 |
| 鑄鐵管切管 | 口 | 2,050 |
| 鋼管工地焊接 | 口 | 21,100 |

### 檢測費用
| 項目 | 單位 | 單價(元) |
|-----|------|---------|
| 試壓費用 | M | 192 |
| 洗管費用 | M | 80 |
| CCTV檢視 | M | 330 |

### 臨時工程
| 項目 | 單位 | 單價(元) |
|-----|------|---------|
| CLSM回填 | M³ | 1,100 |
| 鋼板樁(L=7m) | 片 | 920 |
| 門型擋土樁 | M | 810 |
| 點井費用 | M | 750 |
| 抽水費用 | M | 130 |

### 路面工程
| 項目 | 單位 | 單價(元) |
|-----|------|---------|
| 瀝青刨除(10cm) | M² | 155 |
| 瀝青刨除(20cm) | M² | 250 |
| 瀝青舖面(10cm) | M² | 890 |
| 瀝青舖面(20cm) | M² | 1,700 |

## 管徑成本係數

依據1000mm管線為基準(1.0)：

| 管徑(mm) | 成本係數 |
|---------|---------|
| 150 | 0.25 |
| 200 | 0.30 |
| 250 | 0.35 |
| 300 | 0.40 |
| 400 | 0.50 |
| 500 | 0.60 |
| 600 | 0.70 |
| 800 | 0.90 |
| 1000 | 1.00 |
| 1200 | 1.25 |
| 1500 | 1.65 |

## 調整因子

### 地質條件
- 軟質土壤：1.0
- 礫石層：1.15
- 岩盤：1.30

### 施工環境
- 郊區：1.0
- 市區：1.20
- 高鐵/捷運敏感區：1.35

### 路面類型
- 一般道路：1.0
- 高速公路：1.25
- 鐵路穿越：1.40

## 預算推估公式

```
總預算 = 管線長度(M) × 管徑係數 × 基準單價(50,603元/M) × 調整因子

其中調整因子 = 地質係數 × 環境係數 × 路面係數
```

## 使用範例

### 範例1：查詢單價

```python
from skills.pipeline_budget_estimator.budget_calculator import query_price

# 查詢所有與"接頭"相關的項目
results = query_price("接頭")
for item in results:
    print(f"{item['項目名稱']}: {item['單價']}元/{item['單位']}")
```

### 範例2：完整預算推估

```python
from skills.pipeline_budget_estimator.budget_calculator import estimate

result = estimate(
    length=1000,      # 1000公尺
    diameter=600,     # 600mm管徑
    geology="軟質土壤",
    environment="市區",
    road_type="一般道路"
)

print("基本參數:", result['基本參數'])
print("費用明細:", result['費用明細(元)'])
print("單位長度單價:", result['單位長度單價'])
```

### 範例3：計算CLSM數量

```python
from skills.pipeline_budget_estimator.budget_calculator import calculate_clsm

result = calculate_clsm(length=2000, diameter=1000)
print(f"CLSM體積: {result['計算結果']['CLSM回填體積(M³)']} M³")
print(f"總價: {result['計算結果']['總價(元)']:,} 元")
```

## MCP工具使用

本工具也提供MCP（Model Context Protocol）標準接口：

```python
from skills.pipeline_budget_estimator.mcp_tools import execute_tool

# 查詢單價
result = execute_tool("query_1000mm_unit_price", item_keyword="埋設")

# 推估預算
result = execute_tool(
    "estimate_pipeline_budget",
    length=500,
    diameter=800,
    geology="軟質土壤",
    environment="市區",
    road_type="一般道路"
)

# 計算CLSM
result = execute_tool("calculate_clsm_backfill", length=2000, diameter=1000)

# 比較管徑
result = execute_tool("compare_diameter_prices", diameters=[600, 800, 1000, 1200])
```

## 注意事項

1. 以上單價基於嘉義科學園區供水北線工程-管(一)預算書
2. 實際單價會因物價指數、施工條件、工期等因素調整
3. 推進工法單價遠高於明挖工法，選擇時需綜合考量
4. 路面修復費用會因道路等級、瀝青厚度而異
5. 臨時擋土設施費用會因地質條件、開挖深度而調整

## 參考資料

- 工程名稱：嘉義科學園區供水北線工程-管(一)
- 工程編號：WR11405010027
- 施工總長度：4,952 M（明挖）+ 358 M（推進）
- 總預算：258,226,500元（含稅）

## 授權

本工具僅供參考使用，實際工程預算應以正式預算書為準。
