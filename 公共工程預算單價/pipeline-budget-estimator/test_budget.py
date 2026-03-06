#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
管線工程預算估算器測試腳本
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from budget_calculator import PipelineBudgetEstimator, query_price, estimate, calculate_clsm

def test_basic_functions():
    """測試基本功能"""
    print("="*70)
    print("管線工程預算估算器 - 功能測試")
    print("="*70)
    
    estimator = PipelineBudgetEstimator()
    
    # 測試1: 查詢單價
    print("\n【測試1】查詢1000mm管線單價")
    print("-"*70)
    results = estimator.query_1000mm_price("埋設")
    print(f"找到 {len(results)} 個項目:")
    for item in results[:3]:  # 只顯示前3個
        print(f"  - {item['項目名稱']}: {item.get('單價', 'N/A')} 元/{item.get('單位', '')}")
    
    # 測試2: 計算單位長度單價
    print("\n【測試2】計算不同管徑單位長度單價")
    print("-"*70)
    for diameter in [600, 800, 1000, 1200]:
        result = estimator.calculate_unit_price_per_meter(diameter)
        print(f"  {diameter}mm: 係數={result['管徑係數']}, 綜合單價={result['綜合單價(基本項目)']:.0f}元/M")
    
    # 測試3: 預算推估
    print("\n【測試3】預算推估範例")
    print("-"*70)
    
    # 範例1: 600mm管線
    result1 = estimator.estimate_budget(1000, 600, "軟質土壤", "郊區", "一般道路")
    print(f"\n範例1: 600mm管線 1000M (郊區/一般土壤)")
    print(f"  總預算(未稅): {result1['費用明細(元)']['總計(未稅)']:,} 元")
    print(f"  總預算(含稅): {result1['費用明細(元)']['總計(含稅5%)']:,} 元")
    print(f"  每公尺單價: {result1['單位長度單價']['每公尺單價(含稅)']:,} 元/M")
    
    # 範例2: 800mm管線（市區）
    result2 = estimator.estimate_budget(500, 800, "軟質土壤", "市區", "一般道路")
    print(f"\n範例2: 800mm管線 500M (市區/一般土壤)")
    print(f"  總預算(未稅): {result2['費用明細(元)']['總計(未稅)']:,} 元")
    print(f"  總預算(含稅): {result2['費用明細(元)']['總計(含稅5%)']:,} 元")
    print(f"  每公尺單價: {result2['單位長度單價']['每公尺單價(含稅)']:,} 元/M")
    
    # 範例3: 1000mm管線（高鐵敏感區）
    result3 = estimator.estimate_budget(300, 1000, "軟質土壤", "高鐵敏感區", "一般道路")
    print(f"\n範例3: 1000mm管線 300M (高鐵敏感區/一般土壤)")
    print(f"  總預算(未稅): {result3['費用明細(元)']['總計(未稅)']:,} 元")
    print(f"  總預算(含稅): {result3['費用明細(元)']['總計(含稅5%)']:,} 元")
    print(f"  每公尺單價: {result3['單位長度單價']['每公尺單價(含稅)']:,} 元/M")
    
    # 測試4: CLSM計算
    print("\n【測試4】CLSM回填計算")
    print("-"*70)
    clsm_result = estimator.calculate_clsm_volume(2000, 1000)
    print(f"1000mm管線 2000M:")
    print(f"  CLSM體積: {clsm_result['計算結果']['CLSM回填體積(M³)']:.2f} M³")
    print(f"  總價: {clsm_result['計算結果']['總價(元)']:,} 元")
    
    print("\n" + "="*70)
    print("測試完成!")
    print("="*70)

def test_convenience_functions():
    """測試便捷函數"""
    print("\n【便捷函數測試】")
    print("-"*70)
    
    # 測試 query_price
    print("\n1. query_price() - 查詢單價")
    results = query_price("接頭")
    print(f"   找到 {len(results)} 個接頭相關項目")
    
    # 測試 estimate
    print("\n2. estimate() - 預算推估")
    result = estimate(500, 600)
    print(f"   600mm管線 500M 預算: {result['費用明細(元)']['總計(含稅5%)']:,} 元")
    
    # 測試 calculate_clsm
    print("\n3. calculate_clsm() - CLSM計算")
    result = calculate_clsm(1000, 800)
    print(f"   800mm管線 1000M CLSM: {result['計算結果']['CLSM回填體積(M³)']:.2f} M³")

def show_price_summary():
    """顯示價格摘要"""
    estimator = PipelineBudgetEstimator()
    print("\n")
    print(estimator.get_price_summary())

if __name__ == "__main__":
    # 執行所有測試
    show_price_summary()
    test_basic_functions()
    test_convenience_functions()
