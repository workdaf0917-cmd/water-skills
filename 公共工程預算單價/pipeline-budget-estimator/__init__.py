# -*- coding: utf-8 -*-
"""
管線工程預算估算器 (Pipeline Budget Estimator)

基於台灣自來水公司管線工程預算書資料，提供1000mm管線單位長度施工單價查詢，
以及各管徑預算推估功能。

使用方法:
    from pipeline_budget_estimator import PipelineBudgetEstimator

    estimator = PipelineBudgetEstimator()
    result = estimator.estimate_budget(
        length=500,
        diameter=800,
        geology="軟質土壤",
        environment="市區",
        road_type="一般道路"
    )
"""

from .budget_calculator import (
    PipelineBudgetEstimator,
    BudgetItem,
    query_price,
    estimate,
    calculate_clsm
)

from .mcp_tools import (
    PipelineBudgetTools,
    execute_tool,
    TOOLS_REGISTRY
)

__version__ = "1.0.0"
__author__ = "Claude Skill Developer"

__all__ = [
    "PipelineBudgetEstimator",
    "BudgetItem",
    "query_price",
    "estimate",
    "calculate_clsm",
    "PipelineBudgetTools",
    "execute_tool",
    "TOOLS_REGISTRY"
]
