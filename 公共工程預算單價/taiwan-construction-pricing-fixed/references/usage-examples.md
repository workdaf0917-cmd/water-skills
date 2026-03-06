# 使用範例

## 目錄
1. [Python 範例](#python-範例)
2. [JavaScript 範例](#javascript-範例)
3. [Excel 範例](#excel-範例)
4. [工程預算計算範例](#工程預算計算範例)

---

## Python 範例

### 1. 基本資料抓取

#### 1.1 抓取大宗資材價格

```python
import pandas as pd
import requests
from io import StringIO

# 下載大宗資材價格 CSV
url = "https://pcic.pcc.gov.tw/pwc-web/api/service/opendata-file/document/大宗資材及其漲跌幅彙整表.csv"

response = requests.get(url, timeout=30)
response.encoding = 'utf-8'

# 讀取 CSV 資料
df = pd.read_csv(StringIO(response.text))

# 顯示前 5 筆資料
print(df.head())

# 顯示資料統計資訊
print(f"\n資料筆數: {len(df)}")
print(f"資料欄位: {df.columns.tolist()}")
```

#### 1.2 查詢特定材料價格

```python
# 查詢鋼筋價格
steel_df = df[df['調查項目'].str.contains('鋼筋', na=False)]
print("\n鋼筋價格:")
print(steel_df[['調查項目', '調查地區', '114.8價格(A)', '單位']])

# 查詢北部地區混凝土價格
concrete_north = df[
    (df['調查項目'].str.contains('混凝土', na=False)) & 
    (df['調查地區'] == '北部地區')
]
print("\n北部地區混凝土價格:")
print(concrete_north[['調查項目', '114.8價格(A)', '單位']])
```

#### 1.3 價格趨勢分析

```python
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
matplotlib.rcParams['axes.unicode_minus'] = False

# 查詢特定材料在各區域的價格
material = '鋼筋#D19~D25'
material_df = df[df['調查項目'] == material]

# 繪製價格比較圖
plt.figure(figsize=(10, 6))
plt.bar(material_df['調查地區'], material_df['114.8價格(A)'])
plt.title(f'{material} 各地區價格比較')
plt.xlabel('地區')
plt.ylabel('價格 (元/公噸)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
```

### 2. API 資料抓取

#### 2.1 新北市物價指數 API

```python
import json

# 新北市物價指數 API
api_url = "https://data.ntpc.gov.tw/api/datasets/9d0483b6-513a-46b2-92e3-5f9b315999bb/json"

response = requests.get(api_url, params={'page': 1, 'size': 100})
data = response.json()

# 轉換為 DataFrame
df_ntpc = pd.DataFrame(data)

# 顯示最新資料
print("新北市營造工程物價指數:")
print(df_ntpc.tail(5))

# 計算平均年增率
avg_growth = df_ntpc['總指數年增率_百分比_'].astype(float).mean()
print(f"\n平均年增率: {avg_growth:.2f}%")
```

#### 2.2 臺中市 API 資料抓取

```python
# 臺中市建築改良物標準單價表
api_url = "https://datacenter.taichung.gov.tw/api/4691fbef-17a0-46b7-a264-826849525bd5/json"

response = requests.get(api_url)
data = response.json()

df_tc = pd.DataFrame(data)

# 依構造類別分組計算平均單價
avg_price = df_tc.groupby('構造類別')['標準單價-元每平方公尺'].mean()
print("各構造類別平均單價:")
print(avg_price)
```

### 3. 工程預算計算

```python
def calculate_construction_budget(quantities, prices, management_rate=0.15, profit_rate=0.08):
    """
    計算工程預算
    
    參數:
        quantities: dict, 各工項數量
        prices: dict, 各工項單價
        management_rate: float, 管理費率 (預設 15%)
        profit_rate: float, 利潤率 (預設 8%)
    
    返回:
        dict, 預算明細
    """
    # 計算直接工程費
    direct_cost = sum(qty * prices[item] for item, qty in quantities.items())
    
    # 加入管理費
    cost_with_management = direct_cost * (1 + management_rate)
    
    # 加入利潤
    total_cost = cost_with_management * (1 + profit_rate)
    
    return {
        '直接工程費': direct_cost,
        '管理費': direct_cost * management_rate,
        '利潤': cost_with_management * profit_rate,
        '總預算': total_cost
    }

# 使用範例
project_quantities = {
    '混凝土': 100,  # 立方公尺
    '鋼筋': 50,     # 公噸
    '模板': 200     # 平方公尺
}

project_prices = {
    '混凝土': 2500,  # 元/立方公尺
    '鋼筋': 18500,   # 元/公噸
    '模板': 800      # 元/平方公尺
}

budget = calculate_construction_budget(project_quantities, project_prices)
print("\n工程預算明細:")
for item, amount in budget.items():
    print(f"{item}: {amount:,.2f} 元")
```

---

## JavaScript 範例

### 1. 前端網頁應用

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>工程單價查詢系統</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body>
    <h1>工程單價查詢系統</h1>
    
    <div>
        <h2>新北市物價指數</h2>
        <canvas id="priceChart"></canvas>
    </div>
    
    <script>
        // 抓取新北市物價指數
        async function fetchNTPCPriceIndex() {
            try {
                const response = await fetch(
                    'https://data.ntpc.gov.tw/api/datasets/9d0483b6-513a-46b2-92e3-5f9b315999bb/json?page=1&size=50'
                );
                const data = await response.json();
                return data;
            } catch (error) {
                console.error('資料抓取錯誤:', error);
                return [];
            }
        }
        
        // 繪製圖表
        async function drawChart() {
            const data = await fetchNTPCPriceIndex();
            
            const labels = data.map(item => item['年_月']);
            const values = data.map(item => parseFloat(item['總指數原始值']));
            
            const ctx = document.getElementById('priceChart').getContext('2d');
            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [{
                        label: '營造工程物價指數',
                        data: values,
                        borderColor: 'rgb(75, 192, 192)',
                        tension: 0.1
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        y: {
                            beginAtZero: false
                        }
                    }
                }
            });
        }
        
        drawChart();
    </script>
</body>
</html>
```

### 2. Node.js 後端應用

```javascript
const express = require('express');
const axios = require('axios');
const cors = require('cors');

const app = express();
app.use(cors());
app.use(express.json());

// 新北市物價指數 API
app.get('/api/price-index/ntpc', async (req, res) => {
    try {
        const response = await axios.get(
            'https://data.ntpc.gov.tw/api/datasets/9d0483b6-513a-46b2-92e3-5f9b315999bb/json',
            {
                params: {
                    page: req.query.page || 1,
                    size: req.query.size || 100
                }
            }
        );
        res.json(response.data);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// 工程預算計算 API
app.post('/api/budget/calculate', (req, res) => {
    const { quantities, prices, managementRate = 0.15, profitRate = 0.08 } = req.body;
    
    let directCost = 0;
    const details = [];
    
    for (const [item, qty] of Object.entries(quantities)) {
        const price = prices[item] || 0;
        const cost = qty * price;
        directCost += cost;
        details.push({
            item,
            quantity: qty,
            unitPrice: price,
            cost
        });
    }
    
    const managementFee = directCost * managementRate;
    const profit = (directCost + managementFee) * profitRate;
    const totalBudget = directCost + managementFee + profit;
    
    res.json({
        details,
        summary: {
            directCost,
            managementFee,
            profit,
            totalBudget
        }
    });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
```

---

## Excel 範例

### 1. 從 CSV 匯入資料

1. **開啟 Excel**
2. **資料** → **從文字/CSV**
3. **選擇檔案** 或 **輸入網址**
   ```
   https://pcic.pcc.gov.tw/pwc-web/api/service/opendata-file/document/大宗資材及其漲跌幅彙整表.csv
   ```
4. **設定編碼**: UTF-8
5. **載入**

### 2. 建立查詢公式

```excel
// VLOOKUP 範例 - 查詢鋼筋價格
=VLOOKUP("*鋼筋*", A:D, 3, FALSE)

// INDEX + MATCH 範例
=INDEX(C:C, MATCH("*鋼筋#D19~D25*", A:A, 0))

// SUMIF 範例 - 計算北部地區材料總價
=SUMIF(B:B, "北部地區", C:C)
```

### 3. 建立樞紐分析表

1. **選擇資料範圍**
2. **插入** → **樞紐分析表**
3. **設定欄位**:
   - 列: 調查項目
   - 欄: 調查地區
   - 值: 114.8價格(A)

---

## 工程預算計算範例

### 範例 1: 混凝土工程預算

```python
# 工程項目
project = {
    'name': '基礎混凝土工程',
    'items': [
        {'name': '基礎開挖', 'quantity': 500, 'unit': '立方公尺', 'price': 350},
        {'name': '鋼筋混凝土(210kgf/cm²)', 'quantity': 300, 'unit': '立方公尺', 'price': 2500},
        {'name': '鋼筋#D19~D25', 'quantity': 30, 'unit': '公噸', 'price': 18500},
        {'name': '模板', 'quantity': 800, 'unit': '平方公尺', 'price': 800},
    ]
}

# 計算各項金額
for item in project['items']:
    item['amount'] = item['quantity'] * item['price']

# 計算小計
subtotal = sum(item['amount'] for item in project['items'])

# 加入其他費用
management_fee = subtotal * 0.15  # 管理費 15%
profit = (subtotal + management_fee) * 0.08  # 利潤 8%
total = subtotal + management_fee + profit

print(f"工程名稱: {project['name']}")
print("-" * 60)
for item in project['items']:
    print(f"{item['name']:30s} {item['quantity']:8.2f} {item['unit']:8s} × {item['price']:10,.2f} = {item['amount']:15,.2f}")
print("-" * 60)
print(f"{'小計':30s} {'':8s} {'':8s}   {'':10s} = {subtotal:15,.2f}")
print(f"{'管理費(15%)':30s} {'':8s} {'':8s}   {'':10s} = {management_fee:15,.2f}")
print(f"{'利潤(8%)':30s} {'':8s} {'':8s}   {'':10s} = {profit:15,.2f}")
print("-" * 60)
print(f"{'總計':30s} {'':8s} {'':8s}   {'':10s} = {total:15,.2f}")
```

### 範例 2: 考量物價指數調整

```python
# 原始預算
original_budget = 10000000  # 1,000萬元

# 基期物價指數
base_index = 105.5

# 當期物價指數
current_index = 112.3

# 計算調整係數
adjustment_factor = current_index / base_index

# 調整後預算
adjusted_budget = original_budget * adjustment_factor

# 計算調整金額
adjustment_amount = adjusted_budget - original_budget

print(f"原始預算: {original_budget:,.2f} 元")
print(f"基期物價指數: {base_index}")
print(f"當期物價指數: {current_index}")
print(f"調整係數: {adjustment_factor:.4f}")
print(f"調整後預算: {adjusted_budget:,.2f} 元")
print(f"調整金額: {adjustment_amount:,.2f} 元 ({adjustment_amount/original_budget*100:+.2f}%)")
```

### 範例 3: 區域價差比較

```python
import pandas as pd

# 載入資料
df = pd.read_csv('大宗資材及其漲跌幅彙整表.csv')

# 選擇特定材料
material = '預拌混凝土(210kgf/cm²)'
material_prices = df[df['調查項目'] == material]

# 計算區域價差
price_stats = material_prices.groupby('調查地區')['114.8價格(A)'].agg(['mean', 'min', 'max'])
price_stats['range'] = price_stats['max'] - price_stats['min']

print(f"{material} 各地區價格統計:")
print(price_stats)

# 找出最高和最低價格區域
max_price_region = price_stats['mean'].idxmax()
min_price_region = price_stats['mean'].idxmin()
price_diff = price_stats.loc[max_price_region, 'mean'] - price_stats.loc[min_price_region, 'mean']

print(f"\n最高價格區域: {max_price_region} ({price_stats.loc[max_price_region, 'mean']:,.2f} 元)")
print(f"最低價格區域: {min_price_region} ({price_stats.loc[min_price_region, 'mean']:,.2f} 元)")
print(f"價差: {price_diff:,.2f} 元 ({price_diff/price_stats.loc[min_price_region, 'mean']*100:.2f}%)")
```
