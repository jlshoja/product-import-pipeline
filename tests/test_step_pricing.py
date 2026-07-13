import pytest
try:
    from product_extraction.standardizer.step_pricing import round_price
except ImportError:
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "product_extraction"))
    from standardizer.step_pricing import round_price

def test_round_price_nearest_1000():
    assert round_price(80400) == 80000
    assert round_price(80500) == 81000
    assert round_price(0) == 0
