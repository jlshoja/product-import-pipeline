#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Scraper helper compatibility wrappers.

Implementations live in product_extraction.common after shared utility
consolidation.
"""

import sys
from pathlib import Path

# Enable direct-script execution
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

try:
    from common.text_utils import clean_product_name as _clean_product_name
    from common.text_utils import extract_domain as _extract_domain
    from common.text_utils import extract_product_code as _extract_product_code
    from common.text_utils import normalize_url as _normalize_url
except ImportError:
    from product_extraction.common.text_utils import clean_product_name as _clean_product_name
    from product_extraction.common.text_utils import extract_domain as _extract_domain
    from product_extraction.common.text_utils import extract_product_code as _extract_product_code
    from product_extraction.common.text_utils import normalize_url as _normalize_url


def extract_product_code(text: str) -> str:
    """Extract product code from text."""
    return _extract_product_code(text)


def clean_product_name(text: str) -> str:
    """Clean product name by removing prices and extra whitespace."""
    return _clean_product_name(text, normalize_digit_characters=False)


def normalize_url(url: str) -> str:
    """Normalize URL by removing query parameters and fragments."""
    return _normalize_url(url)


def extract_domain(url: str) -> str:
    """Extract domain from URL."""
    return _extract_domain(url)


if __name__ == "__main__":
    print("Testing scraper helper wrappers...")
    print(f"  code -> {extract_product_code('کیف کد 8009')}")
    print(f"  name -> {clean_product_name('کیف کد 123 ۲٬۵۰۰٬۰۰۰ تومان')}")
    print(f"  url -> {normalize_url('http://example.com/a?x=1#b')}")
    print(f"  domain -> {extract_domain('https://example.com/a')}")
