#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
管線工程預算估算器 - MCP工具
提供預算查詢和推估的標準化工具接口
"""

from typing import Dict, List, Optional
import sys
import os

# 添加當前目錄到路徑
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from budget_calculator import PipelineBudgetEstimator

# 全局估算器實例
_estimator = None

def _get_estimator() -> PipelineBudgetEstimator:
    """取得估算器實例（單例模式）"""
    global _estimator
    if _estimator is None:
        _estimator = PipelineBudgetEstimator()
    return _estimator


class PipelineBudgetTools:
    """管線工程預算工具類別"""
    
    @staticmethod
    def query_1000mm_unit_price(item_keyword: Optional[str] = None) -> Dict:
        """
        查詢1000mm管線單位長度施工單價
        
        Args:
            item_keyword: 項目關鍵字（如"埋設"、"接頭"、"試壓"等），不指定則返回所有項目
            
        Returns:
            單價查詢結果
        """
        estimator = _get_estimator()
        results = estimator.query_1000mm_price(item_keyword)
        
        if not results:
            return {
                "status": "success",
                "message": f"未找到符合 '{item_keyword}' 的項目",
                "data": []
            }
        
        return {
            "status": "success",
            "message": f"找到 {len(results)} 個項目",
            "keyword": item_keyword,
            "data": results
        }
    
    @staticmethod
    def get_price_summary() -> Dict:
        """
        取得1000mm管線價格摘要
        
        Returns:
            價格摘要報告
        """
        estimator = _get_estimator()
        report = estimator.get_price_summary()
        
        return {
            "status": "success",
            "message": "價格摘要",
            "data": report
        }
    
    @staticmethod
    def calculate_unit_price_per_meter(diameter: int) -> Dict:
        """
        計算指定管徑的單位長度綜合單價
        
        Args:
            diameter: 管徑(mm)，支援150-1500mm
            
        Returns:
            單位長度各項費用明細
        """
        estimator = _get_estimator()
        result = estimator.calculate_unit_price_per_meter(diameter)
        
        return {
            "status": "success",
            "message": f"{diameter}mm管徑單位長度單價",
            "diameter": diameter,
            "data": result
        }
    
    @staticmethod
    def estimate_pipeline_budget(
        length: float,
        diameter: int,
        geology: str = "軟質土壤",
        environment: str = "郊區",
        road_type: str = "一般道路"
    ) -> Dict:
        """
        推估管線工程預算
        
        Args:
            length: 管線長度(M)
            diameter: 管徑(mm)
            geology: 地質條件（軟質土壤/礫石層/岩盤）
            environment: 施工環境（郊區/市區/高鐵敏感區/捷運敏感區）
            road_type: 路面類型（一般道路/高速公路/鐵路穿越）
            
        Returns:
            預算明細
        """
        estimator = _get_estimator()
        result = estimator.estimate_budget(length, diameter, geology, environment, road_type)
        
        return {
            "status": "success",
            "message": f"{diameter}mm管線 {length}M 預算推估",
            "data": result
        }
    
    @staticmethod
    def calculate_clsm_backfill(
        length: float,
        diameter: int,
        trench_width: float = 2.25
    ) -> Dict:
        """
        計算CLSM控制性低強度回填材料數量
        
        Args:
            length: 管線長度(M)
            diameter: 管徑(mm)
            trench_width: 開挖寬度(M)，預設2.25M
            
        Returns:
            CLSM數量計算結果
        """
        estimator = _get_estimator()
        result = estimator.calculate_clsm_volume(length, diameter, trench_width)
        
        return {
            "status": "success",
            "message": f"CLSM回填數量計算",
            "data": result
        }
    
    @staticmethod
    def compare_diameter_prices(diameters: List[int]) -> Dict:
        """
        比較不同管徑的單價
        
        Args:
            diameters: 管徑列表(mm)
            
        Returns:
            各管徑單價比較表
        """
        estimator = _get_estimator()
        
        comparison = []
        for d in diameters:
            result = estimator.calculate_unit_price_per_meter(d)
            comparison.append({
                "管徑": d,
                "管徑係數": result["管徑係數"],
                "綜合單價": result["綜合單價(基本項目)"]
            })
        
        return {
            "status": "success",
            "message": f"比較 {len(diameters)} 種管徑",
            "data": comparison
        }


# 工具註冊表（供MCP使用）
TOOLS_REGISTRY = {
    "query_1000mm_unit_price": {
        "function": PipelineBudgetTools.query_1000mm_unit_price,
        "description": "查詢1000mm管線單位長度施工單價",
        "parameters": {
            "item_keyword": {
                "type": "string",
                "description": "項目關鍵字（如埋設、接頭、試壓等）",
                "required": False
            }
        }
    },
    "get_price_summary": {
        "function": PipelineBudgetTools.get_price_summary,
        "description": "取得1000mm管線價格摘要報告",
        "parameters": {}
    },
    "calculate_unit_price_per_meter": {
        "function": PipelineBudgetTools.calculate_unit_price_per_meter,
        "description": "計算指定管徑的單位長度綜合單價",
        "parameters": {
            "diameter": {
                "type": "integer",
                "description": "管徑(mm)，支援150-1500mm",
                "required": True
            }
        }
    },
    "estimate_pipeline_budget": {
        "function": PipelineBudgetTools.estimate_pipeline_budget,
        "description": "推估管線工程總預算",
        "parameters": {
            "length": {
                "type": "number",
                "description": "管線長度(M)",
                "required": True
            },
            "diameter": {
                "type": "integer",
                "description": "管徑(mm)",
                "required": True
            },
            "geology": {
                "type": "string",
                "description": "地質條件（軟質土壤/礫石層/岩盤）",
                "required": False,
                "default": "軟質土壤"
            },
            "environment": {
                "type": "string",
                "description": "施工環境（郊區/市區/高鐵敏感區/捷運敏感區）",
                "required": False,
                "default": "郊區"
            },
            "road_type": {
                "type": "string",
                "description": "路面類型（一般道路/高速公路/鐵路穿越）",
                "required": False,
                "default": "一般道路"
            }
        }
    },
    "calculate_clsm_backfill": {
        "function": PipelineBudgetTools.calculate_clsm_backfill,
        "description": "計算CLSM控制性低強度回填材料數量",
        "parameters": {
            "length": {
                "type": "number",
                "description": "管線長度(M)",
                "required": True
            },
            "diameter": {
                "type": "integer",
                "description": "管徑(mm)",
                "required": True
            },
            "trench_width": {
                "type": "number",
                "description": "開挖寬度(M)，預設2.25M",
                "required": False,
                "default": 2.25
            }
        }
    },
    "compare_diameter_prices": {
        "function": PipelineBudgetTools.compare_diameter_prices,
        "description": "比較不同管徑的單價",
        "parameters": {
            "diameters": {
                "type": "array",
                "description": "管徑列表(mm)",
                "required": True,
                "items": {"type": "integer"}
            }
        }
    }
}


def execute_tool(tool_name: str, **kwargs) -> Dict:
    """
    執行指定工具
    
    Args:
        tool_name: 工具名稱
        **kwargs: 工具參數
        
    Returns:
        工具執行結果
    """
    if tool_name not in TOOLS_REGISTRY:
        return {
            "status": "error",
            "message": f"未知的工具: {tool_name}",
            "available_tools": list(TOOLS_REGISTRY.keys())
        }
    
    tool = TOOLS_REGISTRY[tool_name]
    try:
        result = tool["function"](**kwargs)
        return result
    except Exception as e:
        return {
            "status": "error",
            "message": f"執行工具失敗: {str(e)}"
        }


if __name__ == "__main__":
    # 示範使用
    print("=" * 60)
    print("管線工程預算估算器 - 工具示範")
    print("=" * 60)
    
    # 1. 查詢單價
    print("\n1. 查詢1000mm管線單價:")
    result = execute_tool("query_1000mm_unit_price", item_keyword="埋設")
    print(f"   找到 {len(result['data'])} 個項目")
    
    # 2. 計算單位長度單價
    print("\n2. 計算800mm管徑單位長度單價:")
    result = execute_tool("calculate_unit_price_per_meter", diameter=800)
    print(f"   管徑係數: {result['data']['管徑係數']}")
    print(f"   綜合單價: {result['data']['綜合單價(基本項目)']}元/M")
    
    # 3. 預算推估
    print("\n3. 推估600mm管線1000M預算:")
    result = execute_tool("estimate_pipeline_budget", 
                         length=1000, 
                         diameter=600,
                         geology="軟質土壤",
                         environment="市區",
                         road_type="一般道路")
    budget = result['data']['費用明細(元)']
    print(f"   總預算(未稅): {budget['總計(未稅)']:,}元")
    print(f"   總預算(含稅): {budget['總計(含稅5%)']:,}元")
    
    # 4. CLSM計算
    print("\n4. 計算1000mm管線2000M的CLSM數量:")
    result = execute_tool("calculate_clsm_backfill", length=2000, diameter=1000)
    print(f"   CLSM體積: {result['data']['計算結果']['CLSM回填體積(M³)']}M³")
    print(f"   總價: {result['data']['計算結果']['總價(元)']:,}元")
    
    print("\n" + "=" * 60)
