#!/usr/bin/env python3
"""
工程参数提取脚本
从PDF或Markdown文件中提取水利环境工程及土木工程的关键参数和规定
"""

import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple
import json

def extract_from_markdown(file_path: str) -> Dict[str, List[str]]:
    """从Markdown文件中提取工程参数和规定"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    results = {
        'design_standards': [],
        'material_specs': [],
        'dimensions': [],
        'regulations': [],
        'safety_requirements': [],
        'environmental_standards': [],
        'hydraulic_params': [],
        'structural_params': [],
        'all_numbers_with_units': []
    }
    
    # 提取设计标准
    design_patterns = [
        r'设计标准[：:]\s*([^\n]+)',
        r'设计规范[：:]\s*([^\n]+)',
        r'依据[：:]?\s*(GB[/\s\d\-\.]+)',
        r'依据[：:]?\s*(CNS[/\s\d\-\.]+)',
        r'标准[：:]\s*([^\n]+)',
    ]
    for pattern in design_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        results['design_standards'].extend(matches)
    
    # 提取材料规格
    material_patterns = [
        r'材料[：:]\s*([^\n]+)',
        r'混凝土强度[：:]?\s*(fc\'?\s*[>=≥]\s*[\d\.]+\s*(?:MPa|kgf/cm²|N/mm²)?)',
        r'鋼筋[：:]?\s*([^\n]+)',
        r'砂石料[：:]\s*([^\n]+)',
    ]
    for pattern in material_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        results['material_specs'].extend(matches)
    
    # 提取尺寸参数
    dimension_patterns = [
        r'(?:寬度|宽度|深度|高度|厚度|直径|半径)[：:]?\s*([\d\.]+\s*(?:mm|cm|m|km|公尺|公分|公厘))',
        r'(?:長度|长度|跨度)[：:]?\s*([\d\.]+\s*(?:mm|cm|m|km|公尺|公分|公厘))',
        r'尺寸[：:]\s*([^\n]+)',
    ]
    for pattern in dimension_patterns:
        matches = re.findall(pattern, content)
        results['dimensions'].extend(matches)
    
    # 提取規定
    regulation_patterns = [
        r'(?:規定|规定|要求)[：:]\s*([^\n]+)',
        r'(?:應|应当|必须)[^\n]{10,100}',
        r'(?:不得|禁止)[^\n]{10,100}',
    ]
    for pattern in regulation_patterns:
        matches = re.findall(pattern, content)
        results['regulations'].extend(matches)
    
    # 提取安全要求
    safety_patterns = [
        r'安全[係系]?数[：:]?\s*([\d\.]+)',
        r'安全要求[：:]\s*([^\n]+)',
        r'安全[標标]准[：:]\s*([^\n]+)',
    ]
    for pattern in safety_patterns:
        matches = re.findall(pattern, content)
        results['safety_requirements'].extend(matches)
    
    # 提取環境標準
    env_patterns = [
        r'環境[標标]准[：:]\s*([^\n]+)',
        r'排放[標标]准[：:]\s*([^\n]+)',
        r'水質[標标]准[：:]\s*([^\n]+)',
    ]
    for pattern in env_patterns:
        matches = re.findall(pattern, content)
        results['environmental_standards'].extend(matches)
    
    # 提取水利參數
    hydraulic_patterns = [
        r'流量[：:]?\s*([\d\.]+\s*(?:m³/s|cms|立方公尺/秒|CMD))',
        r'水位[：:]?\s*([\d\.]+\s*(?:m|公尺|EL\.))',
        r'水深[：:]?\s*([\d\.]+\s*(?:m|cm|公尺|公分))',
        r'流速[：:]?\s*([\d\.]+\s*(?:m/s|公尺/秒))',
        r'揚程[：:]?\s*([\d\.]+\s*(?:m|公尺))',
        r'水力坡降[：:]?\s*([\d\.]+)',
    ]
    for pattern in hydraulic_patterns:
        matches = re.findall(pattern, content)
        results['hydraulic_params'].extend(matches)
    
    # 提取結構參數
    structural_patterns = [
        r'載重[：:]?\s*([\d\.]+\s*(?:kN|tf|ton|噸))',
        r'彎矩[：:]?\s*([\d\.]+\s*(?:kN-m|tf-m))',
        r'應力[：:]?\s*([\d\.]+\s*(?:MPa|kgf/cm²|N/mm²))',
        r'撓度[：:]?\s*([\d\.]+\s*(?:mm|cm))',
    ]
    for pattern in structural_patterns:
        matches = re.findall(pattern, content)
        results['structural_params'].extend(matches)
    
    # 提取所有數值及單位（通用）
    general_number_pattern = r'([\d\.]+\s*(?:mm|cm|m|km|MPa|kN|tf|ton|m³/s|°C|%|kgf/cm²|N/mm²))'
    results['all_numbers_with_units'] = re.findall(general_number_pattern, content)
    
    # 去除重複項
    for key in results:
        results[key] = list(set(results[key]))
    
    return results

def extract_from_pdf_text(pdf_text: str) -> Dict[str, List[str]]:
    """從PDF文本中提取參數（與markdown類似）"""
    # 將PDF文本保存為臨時變量並使用相同的提取邏輯
    temp_file = '/tmp/temp_extracted.txt'
    with open(temp_file, 'w', encoding='utf-8') as f:
        f.write(pdf_text)
    
    results = extract_from_markdown(temp_file)
    Path(temp_file).unlink(missing_ok=True)
    return results

def format_output(results: Dict[str, List[str]], format_type: str = 'text') -> str:
    """格式化輸出結果"""
    if format_type == 'json':
        return json.dumps(results, ensure_ascii=False, indent=2)
    
    # 文本格式
    output = []
    output.append("=" * 60)
    output.append("工程參數提取結果")
    output.append("=" * 60)
    
    sections = {
        'design_standards': '設計標準',
        'material_specs': '材料規格',
        'dimensions': '尺寸參數',
        'regulations': '規定要求',
        'safety_requirements': '安全要求',
        'environmental_standards': '環境標準',
        'hydraulic_params': '水利參數',
        'structural_params': '結構參數',
        'all_numbers_with_units': '所有數值參數'
    }
    
    for key, title in sections.items():
        if results.get(key):
            output.append(f"\n【{title}】")
            for i, item in enumerate(results[key], 1):
                output.append(f"  {i}. {item}")
    
    output.append("\n" + "=" * 60)
    return "\n".join(output)

def main():
    if len(sys.argv) < 2:
        print("使用方法: python extract_params.py <文件路徑> [--format json|text]")
        print("示例: python extract_params.py document.md")
        print("示例: python extract_params.py document.md --format json")
        sys.exit(1)
    
    file_path = sys.argv[1]
    output_format = 'text'
    
    if '--format' in sys.argv:
        idx = sys.argv.index('--format')
        if idx + 1 < len(sys.argv):
            output_format = sys.argv[idx + 1]
    
    if not Path(file_path).exists():
        print(f"錯誤: 文件不存在 - {file_path}")
        sys.exit(1)
    
    # 判斷文件類型
    if file_path.lower().endswith('.md'):
        results = extract_from_markdown(file_path)
    elif file_path.lower().endswith('.pdf'):
        print("注意: PDF提取需要PDF處理庫。請先使用PDF工具將PDF轉換為文本。")
        print("或者使用: pdfplumber, PyPDF2 等庫來讀取PDF")
        sys.exit(1)
    else:
        # 嘗試作為文本文件讀取
        try:
            results = extract_from_markdown(file_path)
        except Exception as e:
            print(f"錯誤: 無法讀取文件 - {e}")
            sys.exit(1)
    
    print(format_output(results, output_format))

if __name__ == "__main__":
    main()
