import pytest
try:
    from product_extraction.common.price_utils import select_effective_price
except ImportError:
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "product_extraction"))
    from common.price_utils import select_effective_price


def test_sale_price_used_when_present():
    assert select_effective_price("100000", "80000") == 80000

def test_regular_used_when_sale_missing():
    assert select_effective_price("100000", None) == 100000
    assert select_effective_price("100000", "nan") == 100000
    assert select_effective_price("100000", "") == 100000

def test_zero_sale_price_falls_through_to_regular():
    assert select_effective_price("100000", "0") == 100000
    assert select_effective_price("100000", "0.0") == 100000

def test_both_missing_returns_none():
    assert select_effective_price(None, None) is None

def test_zero_regular_and_zero_sale_returns_none():
    assert select_effective_price("0", "0") is None
