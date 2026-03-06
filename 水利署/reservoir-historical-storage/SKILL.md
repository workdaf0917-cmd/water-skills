---
name: reservoir-historical-storage
description: "水利署水庫歷史蓄水量查詢：從水利署防汛資訊網爬取水庫歷史蓄水量資料，查詢指定日期區間內任何水庫的每日進水量、出水量、蓄水量等資訊，並進行統計分析。資料範圍涵蓋 1970 年至今，支援台灣所有主要水庫。"
version: "1.0.0"
---

# 水利署水庫歷史蓄水量查詢 Skill

## 描述
此 skill 提供從水利署防汛資訊網（fhy.wra.gov.tw）爬取水庫歷史蓄水量資料的功能，可查詢指定日期區間內任何水庫的每日進水量、出水量、蓄水量等資訊，並進行統計分析。

## 觸發條件
當用戶需要：
- 查詢水庫的歷史蓄水資料
- 分析特定日期區間的進水量/出水量統計
- 計算水庫月平均、最大值、最小值
- 比較不同時期的水庫營運狀況
- 製作水庫歷史資料報表

## 資料來源

### 網站
```
https://fhy.wra.gov.tw/ReservoirPage_2011/StorageCapacity.aspx
```

### 資料範圍
- **時間範圍**: 1970年 ~ 至今
- **水庫範圍**: 台灣所有主要水庫（防汛重點水庫約21座）

### 可查詢欄位
| 欄位 | 說明 | 單位 |
|------|------|------|
| 水庫名稱 | 水庫識別名稱 | - |
| 有效容量 | 水庫有效蓄水容量 | 萬立方公尺 |
| 集水區降雨量 | 前一日累積降雨量 | 毫米 (mm) |
| 進水量 | 當日入流量 | 萬立方公尺 |
| 出水量 | 當日出流量 | 萬立方公尺 |
| 與昨日水位差 | 水位變化 | 公尺 (m) |
| 水位 | 即時水位 | 公尺 (m) |
| 有效蓄水量 | 當前有效蓄水量 | 萬立方公尺 |
| 蓄水量百分比 | 蓄水率 | % |

## 防汛重點水庫列表
| 水庫名稱 | 所在地區 |
|----------|----------|
| 石門水庫 | 桃園市 |
| 新山水庫 | 基隆市 |
| 翡翠水庫 | 新北市 |
| 寶山第二水庫 | 新竹縣 |
| 永和山水庫 | 苗栗縣 |
| 明德水庫 | 苗栗縣 |
| 鯉魚潭水庫 | 苗栗縣 |
| 德基水庫 | 台中市 |
| 石岡壩 | 台中市 |
| 霧社水庫 | 南投縣 |
| 日月潭水庫 | 南投縣 |
| 集集攔河堰 | 南投縣 |
| 湖山水庫 | 雲林縣 |
| 仁義潭水庫 | 嘉義縣 |
| 白河水庫 | 台南市 |
| 烏山頭水庫 | 台南市 |
| 曾文水庫 | 台南市/嘉義縣 |
| 南化水庫 | 台南市 |
| 阿公店水庫 | 高雄市 |
| 高屏溪攔河堰 | 高雄市/屏東縣 |
| 牡丹水庫 | 屏東縣 |

## 使用範例

### 範例 1: 查詢特定日期的阿公店水庫資料
```python
from reservoir_history import get_reservoir_data_by_date

# 查詢 2024年1月15日 阿公店水庫資料
data = get_reservoir_data_by_date(2024, 1, 15, reservoir_name="阿公店水庫")
if data:
    print(f"進水量: {data['inflow']} 萬m³")
    print(f"出水量: {data['outflow']} 萬m³")
```

### 範例 2: 查詢日期區間並統計
```python
from reservoir_history import get_reservoir_data_range, calculate_statistics

# 查詢 2024年1月 阿公店水庫所有資料
data = get_reservoir_data_range(
    start_date=(2024, 1, 1),
    end_date=(2024, 1, 31),
    reservoir_name="阿公店水庫"
)

# 計算統計
stats = calculate_statistics(data)
print(f"進水量 - 平均: {stats['inflow_avg']:.2f}, 最大: {stats['inflow_max']:.2f}, 最小: {stats['inflow_min']:.2f}")
print(f"出水量 - 平均: {stats['outflow_avg']:.2f}, 最大: {stats['outflow_max']:.2f}, 最小: {stats['outflow_min']:.2f}")
```

### 範例 3: 產生月報表
```python
from reservoir_history import generate_monthly_report

# 產生 2024年全年月報表
report = generate_monthly_report(2024, reservoir_name="阿公店水庫")
print(report)
```

### 範例 4: 匯出為 CSV
```python
from reservoir_history import export_to_csv

# 匯出 2024年 Q1 資料
export_to_csv(
    start_date=(2024, 1, 1),
    end_date=(2024, 3, 31),
    reservoir_name="阿公店水庫",
    filename="agongdian_2024Q1.csv"
)
```

## 注意事項
1. **爬取頻率**: 建議每次請求間隔至少 0.5 秒，避免對伺服器造成負擔
2. **資料完整性**: 部分日期可能無資料（如假日或維護期間）
3. **數值處理**: 「--」表示無資料，程式會自動處理為 None
4. **網路依賴**: 需要網路連線，建議加入錯誤處理機制
5. **星期六日資料**: 週末資料在週一統一輸入，可能有延遲

## 錯誤處理
```python
from reservoir_history import get_reservoir_data_by_date, ReservoirDataError

try:
    data = get_reservoir_data_by_date(2024, 1, 15, reservoir_name="阿公店水庫")
except ReservoirDataError as e:
    print(f"查詢失敗: {e}")
except Exception as e:
    print(f"未預期錯誤: {e}")
```

## 相關 Skill
- **水利署水庫每日營運狀況**: 查詢當日即時營運資料（無歷史紀錄）
- **水利署阿公店水庫水情**: 查詢阿公店水庫即時水情（每小時更新）
- **水利署河川流量監測**: 查詢河川流量測站資料
