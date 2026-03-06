---
name: engineering-params-extractor
description: Extract key engineering parameters and regulations from PDF or Markdown documents for hydraulic, environmental, and civil engineering projects. Use when analyzing technical specifications, design standards, material requirements, safety regulations, or extracting numerical parameters with units from engineering documentation (CNS, GB, ACI standards, etc.).
---

# Engineering Parameters Extractor

## Overview

Specialized skill for water resources, environmental, and civil engineering consultants to rapidly extract critical parameters and regulations from technical documents. Automatically identifies design standards, material specifications, dimensions, safety requirements, hydraulic parameters, structural values, and compliance regulations.

## Quick Start

### For Markdown Files

```python
python scripts/extract_params.py document.md
```

Output includes categorized parameters:
- Design standards (CNS, GB, ACI, ISO)
- Material specifications (concrete strength, rebar grades)
- Dimensions (width, depth, thickness with units)
- Regulations and requirements
- Safety factors and coefficients
- Environmental standards
- Hydraulic parameters (flow rate, water level, velocity)
- Structural parameters (load, moment, stress)

### For PDF Files

```python
python scripts/extract_pdf_params.py document.pdf
```

Requires: `pip install pdfplumber`

### JSON Output Format

For programmatic processing:

```python
python scripts/extract_params.py document.md --format json
```

## Core Capabilities

### 1. Design Standards Extraction

Automatically identifies:
- **Taiwan standards**: CNS specifications
- **Chinese standards**: GB codes
- **International standards**: ACI, ASCE, Eurocode, ISO
- Design codes and regulation references

Example patterns recognized:
- "設計標準: CNS 3090"
- "依據 GB 50009-2012"
- "符合 ACI 318"

### 2. Material Specifications

Extracts material properties:
- **Concrete strength**: fc' ≥ 280 kgf/cm², 28 MPa
- **Rebar grades**: SD280, SD420
- **Aggregate specifications**
- **Material requirements and tolerances**

### 3. Dimensional Parameters

Captures measurements with units:
- Length, width, depth, height, thickness
- Diameter, radius, span
- Automatic unit recognition: mm, cm, m, km, 公尺, 公分, 公厘

### 4. Hydraulic Engineering Parameters

Specialized extraction for:
- **Flow rate** (Q): m³/s, cms, CMD
- **Water level** (EL.): elevation in meters
- **Water depth**: m, cm
- **Flow velocity**: m/s
- **Pump head**: m
- **Hydraulic gradient**: slope ratio

### 5. Structural Engineering Parameters

Identifies structural values:
- **Loads**: kN, tf, ton (live/dead loads)
- **Moments**: kN-m, tf-m (bending moments)
- **Stress**: MPa, kgf/cm², N/mm²
- **Deflection**: mm, cm
- **Safety factors**

### 6. Regulations and Requirements

Extracts compliance items:
- Mandatory requirements ("應", "必須")
- Prohibitions ("不得", "禁止")
- Safety regulations
- Environmental compliance
- Quality control standards

### 7. Environmental Standards

Captures environmental parameters:
- Water quality standards (BOD, COD, SS, pH, DO)
- Emission standards
- Discharge limits
- Environmental impact criteria

## Workflow

### Step 1: Prepare Document

Ensure document is in:
- **Markdown format** (.md) - direct processing
- **PDF format** (.pdf) - requires pdfplumber installation

### Step 2: Run Extraction

Choose appropriate script:

**For text-based analysis:**
```bash
python scripts/extract_params.py <file_path>
```

**For PDF documents:**
```bash
python scripts/extract_pdf_params.py <file_path>
```

### Step 3: Review Results

Extraction organizes parameters into categories:

```
============================================================
工程參數提取結果
============================================================

【設計標準】
  1. CNS 3090
  2. GB 50009-2012

【材料規格】
  1. fc' ≥ 280 kgf/cm²
  2. SD420 鋼筋

【尺寸參數】
  1. 寬度 3.5 m
  2. 深度 2.0 m

【水利參數】
  1. 設計流量 15.5 m³/s
  2. 水位 EL. 125.00 m

【結構參數】
  1. 活載重 5.0 kN/m²
  2. 混凝土強度 fc' = 280 kgf/cm²

【規定要求】
  1. 安全係數不得小於 1.5
  2. 保護層厚度應符合規範
```

### Step 4: Post-Processing

For further analysis, use JSON output:

```bash
python scripts/extract_params.py document.md --format json > output.json
```

## Engineering Domain Reference

For detailed terminology and standards, see `references/engineering_terms.md`:
- Complete list of hydraulic parameters and units
- Structural engineering terminology
- Taiwan, Chinese, and international standards codes
- Material properties reference
- Safety factor guidelines
- Environmental standards reference

## Available Scripts

### extract_params.py
Main extraction script for Markdown and text files. Processes content and categorizes engineering parameters.

**Usage:**
```bash
python scripts/extract_params.py <file_path> [--format json|text]
```

### extract_pdf_params.py
PDF-specific extraction using pdfplumber library. Converts PDF to text then applies parameter extraction.

**Usage:**
```bash
python scripts/extract_pdf_params.py <file_path> [--format json|text]
```

**Dependencies:** Requires `pdfplumber` - install via `pip install pdfplumber`

## Customization

### Adding New Parameter Patterns

Edit `scripts/extract_params.py` to add domain-specific patterns:

```python
# Add custom patterns to relevant sections
custom_patterns = [
    r'your_pattern_here',
    r'another_pattern'
]
```

### Extending Engineering Terms

Add new terminology to `references/engineering_terms.md` for domain reference.
