#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Scraper Helper Functions
"""

import re


def extract_product_code(text: str) -> str:
    """
    Extract product code from text
    
    Args:
        text: Text containing product code
    
    Returns:
        Product code or empty string
    
    Examples:
        >>> extract_product_code('کیف کد 8009')
        '8009'
        >>> extract_product_code('چمدان کد ۱۲۳۴ قرمز')
        '1234'
    """
    if not text:
        return ''
    
    # Search for "کد" followed by numbers (Persian or English)
    pattern = r'کد\s*([۰-۹0-9]+)'
    match = re.search(pattern, text)
    
    if match:
        code = match.group(1)
        # Convert Persian numbers to English
        persian_to_english = str.maketrans('۰۱۲۳۴۵۶۷۸۹', '0123456789')
        code = code.translate(persian_to_english)
        return code
    
    return ''


def clean_product_name(text: str) -> str:
    """
    Clean product name by removing prices and extra whitespace
    
    Args:
        text: Raw product name
    
    Returns:
        Cleaned product name
    
    Examples:
        >>> clean_product_name('کیف کد 123 ۲٬۵۰۰٬۰۰۰ تومان')
        'کیف کد 123'
        >>> clean_product_name('چمدان   با فاصله زیاد  ')
        'چمدان با فاصله زیاد'
    """
    if not text:
        return ''
    
    # Remove price patterns (Persian/English numbers with commas + تومان/ریال)
    text = re.sub(r'[۰-۹0-9,٬\s]+\s*(تومان|ریال)', '', text)
    
    # Remove multiple spaces
    text = re.sub(r'\s+', ' ', text)
    
    # Remove newlines and tabs
    text = text.replace('\n', ' ').replace('\t', ' ')
    
    # Strip leading/trailing whitespace
    text = text.strip()
    
    return text


def normalize_url(url: str) -> str:
    """
    Normalize URL by removing query parameters and fragments
    
    Args:
        url: Raw URL
    
    Returns:
        Normalized URL
    """
    if not url:
        return ''
    
    # Remove query parameters and fragments
    url = url.split('?')[0].split('#')[0]
    
    # Ensure https
    if url.startswith('http://'):
        url = url.replace('http://', 'https://')
    
    return url.strip()


def extract_domain(url: str) -> str:
    """
    Extract domain from URL
    
    Args:
        url: Full URL
    
    Returns:
        Domain name
    """
    if not url:
        return ''
    
    # Remove protocol
    url = url.replace('https://', '').replace('http://', '')
    
    # Get domain (first part before /)
    domain = url.split('/')[0]
    
    return domain


if __name__ == "__main__":
    # Quick tests
    print("Testing extract_product_code:")
    print(f"  'کیف کد 8009' -> '{extract_product_code('کیف کد 8009')}'")
    print(f"  'چمدان کد ۱۲۳۴' -> '{extract_product_code('چمدان کد ۱۲۳۴')}'")
    
    print("\nTesting clean_product_name:")
    print(f"  'کیف ۲٬۵۰۰٬۰۰۰ تومان' -> '{clean_product_name('کیف ۲٬۵۰۰٬۰۰۰ تومان')}'")
    print(f"  'چمدان   زیاد  ' -> '{clean_product_name('چمدان   زیاد  ')}'")
