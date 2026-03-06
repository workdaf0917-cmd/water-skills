#!/usr/bin/env python3
"""
PDF工程參數提取腳本
使用pdfplumber提取PDF文件中的工程參數
"""

import sys
from pathlib import Path
import json

def extract_from_pdf(pdf_path: str, format_type: str = 'text') -> str:
    """從PDF提取參數並調用extract_params處理"""
    try:
        import pdfplumber
    except ImportError:
        return "錯誤: 需要安裝 pdfplumber。請執行: pip install pdfplumber"
    
    try:
        # 提取PDF文本
        text_content = []
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    text_content.append(text)
        
        full_text = "\n".join(text_content)
        
        # 保存到臨時文件
        temp_file = '/tmp/temp_pdf_extract.txt'
        with open(temp_file, 'w', encoding='utf-8') as f:
            f.write(full_text)
        
        # 調用extract_params處理
        import subprocess
        script_dir = Path(__file__).parent
        extract_script = script_dir / 'extract_params.py'
        
        result = subprocess.run(
            ['python', str(extract_script), temp_file, '--format', format_type],
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        
        # 清理臨時文件
        Path(temp_file).unlink(missing_ok=True)
        
        return result.stdout
        
    except Exception as e:
        return f"錯誤: {str(e)}"

def main():
    if len(sys.argv) < 2:
        print("使用方法: python extract_pdf_params.py <PDF文件路徑> [--format json|text]")
        print("示例: python extract_pdf_params.py document.pdf")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    output_format = 'text'
    
    if '--format' in sys.argv:
        idx = sys.argv.index('--format')
        if idx + 1 < len(sys.argv):
            output_format = sys.argv[idx + 1]
    
    if not Path(pdf_path).exists():
        print(f"錯誤: PDF文件不存在 - {pdf_path}")
        sys.exit(1)
    
    result = extract_from_pdf(pdf_path, output_format)
    print(result)

if __name__ == "__main__":
    main()
