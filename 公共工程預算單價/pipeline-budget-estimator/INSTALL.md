# 管線工程預算估算器 - 安裝指南

## Claude Code Skill 安裝方式

### 方法一：複製到全域 Skills 目錄

```bash
# 找到 Claude Code 的 skills 目錄（通常在 ~/.claude/skills/）
# 將 pipeline-budget-estimator 目錄複製過去

cp -r pipeline-budget-estimator ~/.claude/skills/
```

### 方法二：在專案中使用

```bash
# 將 skill 複製到你的專案目錄
cp -r pipeline-budget-estimator ./skills/
```

### 方法三：作為 Python 套件安裝

```bash
# 進入 skill 目錄
cd pipeline-budget-estimator

# 安裝到當前 Python 環境
pip install -e .
```

## 使用方法

### 在 Claude Code 中使用

安裝後，Claude 會自動識別此 skill。你可以直接問：

- "查詢 1000mm 管線埋設單價"
- "推估 800mm 管線 500 公尺預算"
- "計算 1000mm 管線 2000 公尺 CLSM 回填量"

### 在 Python 中使用

```python
from pipeline_budget_estimator import PipelineBudgetEstimator

estimator = PipelineBudgetEstimator()

# 查詢單價
prices = estimator.query_1000mm_price("埋設")

# 推估預算
result = estimator.estimate_budget(
    length=500,
    diameter=800,
    geology="軟質土壤",
    environment="市區",
    road_type="一般道路"
)
print(f"總預算: {result['費用明細(元)']['總計(含稅5%)']:,}元")
```

## 檔案結構

```
pipeline-budget-estimator/
├── __init__.py           # 套件初始化
├── SKILL.md              # Skill 定義檔
├── README.md             # 完整說明文件
├── USAGE_GUIDE.md        # Claude 使用指南
├── INSTALL.md            # 本安裝指南
├── budget_calculator.py  # 核心計算模組
├── mcp_tools.py         # MCP 工具接口
└── test_budget.py       # 測試腳本
```

## 相依套件

- Python 3.7+
- 僅使用 Python 標準庫，無需額外套件

## 驗證安裝

```bash
cd pipeline-budget-estimator
python -c "from budget_calculator import PipelineBudgetEstimator; \
           e = PipelineBudgetEstimator(); \
           print('Skill 安裝成功!')"
```
