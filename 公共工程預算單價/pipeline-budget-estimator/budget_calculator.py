#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
管線工程預算計算器
基於嘉義科學園區供水北線工程-管(一)預算書資料
"""

import json
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass

@dataclass
class BudgetItem:
    """預算項目資料類別"""
    項次: str
    工作項目: str
    單位: str
    數量: float
    單價: float
    複價: float
    備註: str = ""

class PipelineBudgetEstimator:
    """管線工程預算估算器"""
    
    # 基準參數（1000mm管線）
    BASE_DIAMETER = 1000  # mm
    BASE_UNIT_PRICE = 50603  # 元/公尺（含所有費用）
    
    # 管徑成本係數
    DIAMETER_FACTORS = {
        150: 0.25,
        200: 0.30,
        250: 0.35,
        300: 0.40,
        400: 0.50,
        500: 0.60,
        600: 0.70,
        700: 0.80,
        800: 0.90,
        1000: 1.00,
        1200: 1.25,
        1350: 1.45,
        1500: 1.65,
    }
    
    # 地質調整因子
    GEOLOGY_FACTORS = {
        "軟質土壤": 1.0,
        "礫石層": 1.15,
        "岩盤": 1.30,
    }
    
    # 施工環境調整因子
    ENVIRONMENT_FACTORS = {
        "郊區": 1.0,
        "市區": 1.20,
        "高鐵敏感區": 1.35,
        "捷運敏感區": 1.35,
    }
    
    # 路面類型調整因子
    ROAD_FACTORS = {
        "一般道路": 1.0,
        "高速公路": 1.25,
        "鐵路穿越": 1.40,
    }
    
    # 1000mm管線主要項目單價（來自預算書）
    UNIT_PRICES_1000MM = {
        "直管埋設": {"單價": 890, "單位": "元/M", "數量": 4860},
        "推進工法": {"單價": 80000, "單位": "元/M", "數量": 358},
        "延性鑄鐵管": {"單價": 95800, "單位": "元/M", "數量": 358},
        "機械接頭_K型": {"單價": 1850, "單位": "元/口", "數量": 811},
        "機械接頭_K型含配件": {"單價": 9750, "單位": "元/口", "數量": 65},
        "凸緣接頭_含配件": {"單價": 17650, "單位": "元/口", "數量": 28},
        "鑄鐵管切管": {"單價": 2050, "單位": "元/口", "數量": 40},
        "鋼管焊接": {"單價": 21100, "單位": "元/口", "數量": 36},
        "試壓費用": {"單價": 192, "單位": "元/M", "數量": 5375},
        "洗管費用": {"單價": 80, "單位": "元/M", "數量": 4952},
        "CCTV檢視": {"單價": 330, "單位": "元/M", "數量": 5375},
        "點井費用": {"單價": 750, "單位": "元/M", "數量": 4952},
        "抽水費用": {"單價": 130, "單位": "元/M", "數量": 4952},
        "CLSM回填": {"單價": 1100, "單位": "元/M³", "數量": 20553},
        "瀝青刨除_10cm": {"單價": 155, "單位": "元/M²", "數量": 10833},
        "瀝青刨除_20cm": {"單價": 250, "單位": "元/M²", "數量": 1867},
        "瀝青舖面_10cm": {"單價": 890, "單位": "元/M²", "數量": 10833},
        "瀝青舖面_20cm": {"單價": 1700, "單位": "元/M²", "數量": 1867},
        "鋼板樁_L7m": {"單價": 920, "單位": "元/片", "數量": 20926},
        "門型擋土樁": {"單價": 810, "單位": "元/M", "數量": 50},
    }
    
    def __init__(self, budget_data_path: str = None):
        """初始化估算器"""
        self.budget_data = []
        if budget_data_path:
            self.load_budget_data(budget_data_path)
    
    def load_budget_data(self, filepath: str):
        """載入預算資料"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                self.budget_data = json.load(f)
        except Exception as e:
            print(f"載入預算資料失敗: {e}")
    
    def get_unit_price(self, item_name: str) -> Optional[Dict]:
        """查詢特定項目單價"""
        return self.UNIT_PRICES_1000MM.get(item_name)
    
    def query_1000mm_price(self, item_keyword: str = None) -> List[Dict]:
        """
        查詢1000mm管線相關項目單價
        
        Args:
            item_keyword: 項目關鍵字（如"埋設"、"接頭"等）
            
        Returns:
            符合條件的項目列表
        """
        results = []
        
        if item_keyword:
            for name, data in self.UNIT_PRICES_1000MM.items():
                if item_keyword in name or item_keyword in data.get("工作項目", ""):
                    results.append({
                        "項目名稱": name,
                        **data
                    })
        else:
            # 返回所有項目
            for name, data in self.UNIT_PRICES_1000MM.items():
                results.append({
                    "項目名稱": name,
                    **data
                })
        
        return results
    
    def calculate_unit_price_per_meter(self, diameter: int = 1000) -> Dict:
        """
        計算指定管徑的單位長度綜合單價
        
        Args:
            diameter: 管徑(mm)
            
        Returns:
            單位長度各項費用明細
        """
        if diameter not in self.DIAMETER_FACTORS:
            # 使用線性插值計算係數
            diameters = sorted(self.DIAMETER_FACTORS.keys())
            if diameter < diameters[0]:
                factor = self.DIAMETER_FACTORS[diameters[0]] * (diameter / diameters[0])
            elif diameter > diameters[-1]:
                factor = self.DIAMETER_FACTORS[diameters[-1]] * (diameter / diameters[-1]) ** 0.5
            else:
                # 線性插值
                for i in range(len(diameters) - 1):
                    if diameters[i] <= diameter <= diameters[i + 1]:
                        d1, d2 = diameters[i], diameters[i + 1]
                        f1, f2 = self.DIAMETER_FACTORS[d1], self.DIAMETER_FACTORS[d2]
                        factor = f1 + (f2 - f1) * (diameter - d1) / (d2 - d1)
                        break
        else:
            factor = self.DIAMETER_FACTORS[diameter]
        
        # 計算各項費用
        base_prices = {
            "管材及埋設": 890,
            "機械接頭": 309,
            "凸緣接頭": 129,
            "試壓費用": 192,
            "洗管費用": 80,
            "CCTV檢視": 330,
            "抽水費用": 130,
            "點井費用": 750,
        }
        
        result = {}
        for item, base_price in base_prices.items():
            result[item] = round(base_price * factor, 2)
        
        result["綜合單價(基本項目)"] = round(sum(result.values()), 2)
        result["管徑係數"] = round(factor, 4)
        
        return result
    
    def estimate_budget(
        self,
        length: float,
        diameter: int,
        geology: str = "軟質土壤",
        environment: str = "郊區",
        road_type: str = "一般道路",
        include_contingency: bool = True
    ) -> Dict:
        """
        推估管線工程預算
        
        Args:
            length: 管線長度(M)
            diameter: 管徑(mm)
            geology: 地質條件
            environment: 施工環境
            road_type: 路面類型
            include_contingency: 是否包含雜項費用(15%)
            
        Returns:
            預算明細
        """
        # 取得管徑係數
        if diameter in self.DIAMETER_FACTORS:
            diameter_factor = self.DIAMETER_FACTORS[diameter]
        else:
            # 線性插值
            diameters = sorted(self.DIAMETER_FACTORS.keys())
            if diameter < diameters[0]:
                diameter_factor = self.DIAMETER_FACTORS[diameters[0]] * (diameter / diameters[0])
            elif diameter > diameters[-1]:
                diameter_factor = self.DIAMETER_FACTORS[diameters[-1]] * (diameter / diameters[-1]) ** 0.5
            else:
                for i in range(len(diameters) - 1):
                    if diameters[i] <= diameter <= diameters[i + 1]:
                        d1, d2 = diameters[i], diameters[i + 1]
                        f1, f2 = self.DIAMETER_FACTORS[d1], self.DIAMETER_FACTORS[d2]
                        diameter_factor = f1 + (f2 - f1) * (diameter - d1) / (d2 - d1)
                        break
        
        # 取得調整因子
        geology_factor = self.GEOLOGY_FACTORS.get(geology, 1.0)
        env_factor = self.ENVIRONMENT_FACTORS.get(environment, 1.0)
        road_factor = self.ROAD_FACTORS.get(road_type, 1.0)
        
        total_factor = geology_factor * env_factor * road_factor
        
        # 計算各項費用
        base_unit_price = self.BASE_UNIT_PRICE
        adjusted_unit_price = base_unit_price * diameter_factor * total_factor
        
        # 分項計算
        pipe_cost = length * 890 * diameter_factor * geology_factor
        joint_cost = length * 438 * diameter_factor  # 接頭費用
        testing_cost = length * (192 + 80 + 330) * diameter_factor  # 試壓+洗管+CCTV
        dewatering_cost = length * (130 + 750) * diameter_factor * geology_factor  # 抽水+點井
        
        # 臨時工程（擋土、路面等）
        temp_work_cost = length * adjusted_unit_price * 0.35 * road_factor
        
        # 雜項費用
        if include_contingency:
            subtotal = pipe_cost + joint_cost + testing_cost + dewatering_cost + temp_work_cost
            contingency = subtotal * 0.15
        else:
            contingency = 0
        
        total = pipe_cost + joint_cost + testing_cost + dewatering_cost + temp_work_cost + contingency
        
        return {
            "基本參數": {
                "管線長度(M)": length,
                "管徑(mm)": diameter,
                "管徑係數": round(diameter_factor, 4),
                "地質條件": geology,
                "地質係數": geology_factor,
                "施工環境": environment,
                "環境係數": env_factor,
                "路面類型": road_type,
                "路面係數": road_factor,
                "總調整因子": round(total_factor, 4),
            },
            "費用明細(元)": {
                "管線主體(含埋設)": round(pipe_cost),
                "接頭及配件": round(joint_cost),
                "試壓洗管檢測": round(testing_cost),
                "抽水點井": round(dewatering_cost),
                "臨時工程(擋土路面等)": round(temp_work_cost),
                "雜項費用(15%)": round(contingency),
                "總計(未稅)": round(total),
                "總計(含稅5%)": round(total * 1.05),
            },
            "單位長度單價": {
                "每公尺單價(未稅)": round(total / length),
                "每公尺單價(含稅)": round(total * 1.05 / length),
            }
        }
    
    def calculate_clsm_volume(
        self,
        length: float,
        diameter: int,
        trench_width: float = 2.25,
        soil_type: str = "一般土壤"
    ) -> Dict:
        """
        計算CLSM回填數量
        
        Args:
            length: 管線長度(M)
            diameter: 管徑(mm)
            trench_width: 開挖寬度(M)
            soil_type: 土壤類型
            
        Returns:
            CLSM數量計算結果
        """
        # 管外徑（1000mm管約1.04M）
        pipe_od = diameter / 1000 * 1.04
        
        # 管底深度（假設1.2M）
        pipe_depth = 1.2
        
        # 路面厚度（假設0.1M）
        pavement = 0.1
        
        # CLSM回填體積計算
        # 公式: [(開挖寬度) × (管底深度 + 路面厚度 - 路面厚) - π/4 × 管外徑²] × 長度
        trench_area = trench_width * (pipe_depth + pavement - pavement)
        pipe_area = 3.14159 / 4 * pipe_od ** 2
        clsm_volume = (trench_area - pipe_area) * length
        
        # 單價
        unit_price = 1100  # 元/M³
        total_cost = clsm_volume * unit_price
        
        return {
            "計算參數": {
                "管線長度(M)": length,
                "管徑(mm)": diameter,
                "管外徑(M)": round(pipe_od, 3),
                "開挖寬度(M)": trench_width,
                "管底深度(M)": pipe_depth,
            },
            "計算結果": {
                "開挖斷面積(M²)": round(trench_area, 3),
                "管體斷面積(M²)": round(pipe_area, 3),
                "CLSM回填體積(M³)": round(clsm_volume, 2),
                "單價(元/M³)": unit_price,
                "總價(元)": round(total_cost),
            }
        }
    
    def get_price_summary(self) -> str:
        """取得價格摘要報告"""
        report = []
        report.append("=" * 60)
        report.append("1000mm管線工程單價摘要")
        report.append("=" * 60)
        report.append("")
        report.append("【主要施工項目】")
        report.append(f"  直管埋設: 890元/M")
        report.append(f"  推進工法: 80,000元/M")
        report.append(f"  延性鑄鐵管材料: 95,800元/M")
        report.append("")
        report.append("【接頭相關】")
        report.append(f"  機械接頭(K型): 1,850元/口")
        report.append(f"  機械接頭(K型含配件): 9,750元/口")
        report.append(f"  凸緣接頭(含配件): 17,650元/口")
        report.append(f"  鑄鐵管切管: 2,050元/口")
        report.append("")
        report.append("【試壓檢測】")
        report.append(f"  試壓費用: 192元/M")
        report.append(f"  洗管費用: 80元/M")
        report.append(f"  CCTV檢視: 330元/M")
        report.append("")
        report.append("【臨時工程】")
        report.append(f"  CLSM回填: 1,100元/M³")
        report.append(f"  鋼板樁(L=7m): 920元/片")
        report.append(f"  門型擋土樁: 810元/M")
        report.append("")
        report.append("【路面工程】")
        report.append(f"  瀝青刨除(10cm): 155元/M²")
        report.append(f"  瀝青刨除(20cm): 250元/M²")
        report.append(f"  瀝青舖面(10cm): 890元/M²")
        report.append(f"  瀝青舖面(20cm): 1,700元/M²")
        report.append("")
        report.append("=" * 60)
        
        return "\n".join(report)


# 便捷函數
def query_price(item_keyword: str = None) -> List[Dict]:
    """查詢單價便捷函數"""
    estimator = PipelineBudgetEstimator()
    return estimator.query_1000mm_price(item_keyword)

def estimate(
    length: float,
    diameter: int,
    geology: str = "軟質土壤",
    environment: str = "郊區",
    road_type: str = "一般道路"
) -> Dict:
    """預算推估便捷函數"""
    estimator = PipelineBudgetEstimator()
    return estimator.estimate_budget(length, diameter, geology, environment, road_type)

def calculate_clsm(length: float, diameter: int) -> Dict:
    """CLSM計算便捷函數"""
    estimator = PipelineBudgetEstimator()
    return estimator.calculate_clsm_volume(length, diameter)


if __name__ == "__main__":
    # 示範使用
    estimator = PipelineBudgetEstimator()
    
    print(estimator.get_price_summary())
    print("\n")
    
    # 推估範例
    print("【預算推估範例】")
    print("800mm管線，500公尺，市區，一般土壤:")
    result = estimator.estimate_budget(500, 800, "軟質土壤", "市區", "一般道路")
    print(f"  總預算(未稅): {result['費用明細(元)']['總計(未稅)']:,}元")
    print(f"  總預算(含稅): {result['費用明細(元)']['總計(含稅5%)']:,}元")
    print(f"  每公尺單價: {result['單位長度單價']['每公尺單價(含稅)']:,}元/M")
