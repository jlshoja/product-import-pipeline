#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Centralized path management
همه مسیرهای فایل‌های داده اینجا تعریف شده‌اند
"""

import os
from pathlib import Path

# ریشه پروژه (پوشه‌ای که web_panel_v12.py در آن است)
ROOT_DIR = Path(__file__).parent.parent

# پوشه داده‌ها
DATA_DIR = ROOT_DIR / "data"

# پوشه لاگ‌ها
LOGS_DIR = ROOT_DIR / "logs"

# فایل‌های داده
COLOR_MAPPING_FILE  = str(DATA_DIR / "color_mapping.xlsx")
PRODUCT_NAMES_FILE  = str(DATA_DIR / "product_names.xlsx")
MISSING_PRODUCTS_LOG = str(LOGS_DIR / "missing_products.log")

# اطمینان از وجود پوشه‌ها
DATA_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)
