#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tracker Helper Functions
"""

import re
from typing import Tuple, Optional
from datetime import datetime


def extract_price_from_text(text: str) -> Optional[int]:
    """
    Extract price from Persian/English text
    
    Args:
        text: Text containing price
    
    Returns:
        Price as integer or None
    
    Examples:
        >>> extract_price_from_text('کیف ۲٬۵۴۰٬۰۰۰ تومان')
        2540000
        >>> extract_price_from_text('1,500,000')
        1500000
    """
    if not text:
        return None
    
    # Convert Persian numbers to English
    persian_to_english = str.maketrans('۰۱۲۳۴۵۶۷۸۹٬', '0123456789,')
    text = text.translate(persian_to_english)
    
    # Find all number patterns (with commas)
    pattern = r'[\d,]+'
    matches = re.findall(pattern, text)
    
    if not matches:
        return None
    
    # Get the largest number (usually the price)
    numbers = []
    for match in matches:
        try:
            num = int(match.replace(',', ''))
            if num > 1000:  # Filter out small numbers (like codes)
                numbers.append(num)
        except ValueError:
            continue
    
    if numbers:
        return max(numbers)
    
    return None


def format_number(number: Optional[int]) -> str:
    """
    Format number with comma separators
    
    Args:
        number: Number to format
    
    Returns:
        Formatted string
    
    Examples:
        >>> format_number(1000000)
        '1,000,000'
        >>> format_number(None)
        ''
    """
    if number is None:
        return ''
    
    if number == 0:
        return '0'
    
    return f"{int(number):,}"


def calculate_price_change(old_price: float, new_price: float) -> Tuple[float, float]:
    """
    Calculate price change amount and percentage
    
    Args:
        old_price: Previous price
        new_price: Current price
    
    Returns:
        Tuple of (change_amount, change_percent)
    
    Examples:
        >>> calculate_price_change(100000, 120000)
        (20000, 20.0)
        >>> calculate_price_change(100000, 80000)
        (-20000, -20.0)
    """
    if old_price == 0:
        return (0, 0.0)
    
    change = new_price - old_price
    percent = (change / old_price) * 100
    
    return (change, percent)


def gregorian_to_jalali(g_y: int, g_m: int, g_d: int) -> Tuple[int, int, int]:
    """
    Convert Gregorian date to Jalali (Persian) date
    
    Args:
        g_y: Gregorian year
        g_m: Gregorian month
        g_d: Gregorian day
    
    Returns:
        Tuple of (jalali_year, jalali_month, jalali_day)
    
    Example:
        >>> gregorian_to_jalali(2024, 1, 1)
        (1402, 10, 11)
    """
    # Simplified conversion algorithm
    # For accurate conversion, use jdatetime library
    
    # This is a simplified approximation
    # Actual implementation should use proper algorithm
    
    gy = g_y - 1600
    gm = g_m - 1
    gd = g_d - 1
    
    g_day_no = 365 * gy + ((gy + 3) // 4) - ((gy + 99) // 100) + ((gy + 399) // 400)
    
    days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if (gy % 4 == 0 and gy % 100 != 0) or (gy % 400 == 0):
        days_in_month[1] = 29
    
    for i in range(gm):
        g_day_no += days_in_month[i]
    
    g_day_no += gd
    
    j_day_no = g_day_no - 79
    
    j_np = j_day_no // 12053
    j_day_no %= 12053
    
    jy = 979 + 33 * j_np + 4 * (j_day_no // 1461)
    j_day_no %= 1461
    
    if j_day_no >= 366:
        jy += (j_day_no - 1) // 365
        j_day_no = (j_day_no - 1) % 365
    
    if j_day_no < 186:
        jm = 1 + j_day_no // 31
        jd = 1 + (j_day_no % 31)
    else:
        jm = 7 + (j_day_no - 186) // 30
        jd = 1 + ((j_day_no - 186) % 30)
    
    return (jy, jm, jd)


def get_persian_date(date: Optional[datetime] = None) -> str:
    """
    Get current date in Persian format
    
    Args:
        date: Date to convert (default: now)
    
    Returns:
        Persian date string in YYYY/MM/DD format
    
    Example:
        >>> get_persian_date()
        '1403/10/12'
    """
    if date is None:
        date = datetime.now()
    
    j_y, j_m, j_d = gregorian_to_jalali(date.year, date.month, date.day)
    
    return f"{j_y:04d}/{j_m:02d}/{j_d:02d}"


def format_persian_price(price: Optional[int]) -> str:
    """
    Format price with Persian separators
    
    Args:
        price: Price to format
    
    Returns:
        Formatted price with Persian comma
    """
    if price is None:
        return ''
    
    formatted = format_number(price)
    # Replace English comma with Persian comma
    formatted = formatted.replace(',', '٬')
    
    return formatted


if __name__ == "__main__":
    # Quick tests
    print("Testing extract_price_from_text:")
    print(f"  'کیف ۲٬۵۴۰٬۰۰۰ تومان' -> {extract_price_from_text('کیف ۲٬۵۴۰٬۰۰۰ تومان')}")
    print(f"  '1,500,000' -> {extract_price_from_text('1,500,000')}")
    
    print("\nTesting format_number:")
    print(f"  1000000 -> '{format_number(1000000)}'")
    print(f"  None -> '{format_number(None)}'")
    
    print("\nTesting calculate_price_change:")
    print(f"  100000 -> 120000: {calculate_price_change(100000, 120000)}")
    print(f"  100000 -> 80000: {calculate_price_change(100000, 80000)}")
    
    print("\nTesting gregorian_to_jalali:")
    print(f"  2024-01-01 -> {gregorian_to_jalali(2024, 1, 1)}")
    
    print("\nTesting get_persian_date:")
    print(f"  Today: {get_persian_date()}")
