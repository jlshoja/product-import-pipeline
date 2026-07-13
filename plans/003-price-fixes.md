# Plan 003: Fix price bugs and add price characterization tests

> **Executor instructions**: Follow this plan step by step. Run every
> verification command and confirm the expected result before moving to the
> next step. If anything in the "STOP conditions" section occurs, stop and
> report — do not improvise. When done, update the status row for this plan
> in `plans/README.md`.
>
> **Drift check (run first)**: `git diff --stat c8d53b2..HEAD -- product_extraction/standardizer/step_pricing.py product_extraction/common/price_utils.py`
> If either file changed since this plan was written, compare the "Current
> state" excerpts against the live code before proceeding; on a mismatch, treat
> it as a STOP condition.

## Status

- **Priority**: P1
- **Effort**: M
- **Risk**: MED (changes money-calculation behavior)
- **Depends on**: 001 recommended (golden-file harness) — see note below
- **Category**: bug + tests
- **Planned at**: commit `c8d53b2`, 2026-07-13

**Dependency note**: The *unit tests* in this plan (Step 1) are standalone and
should be written first regardless. The *behavior change* in Step 3
(`step_pricing.py`) affects the WooCommerce price output; ideally plan 001's
golden harness exists so you can confirm no unintended output drift. If 001 is
not done, you may still complete this plan, but flag in your status update that
the `step_pricing` change was merged without golden-file coverage.

## Why this matters

Two price bugs feed a live WooCommerce store:

1. **`step_pricing.py:105`** divides by `(1 - total_discount/100)`. When a
   configured range discount plus `extra_discount_percent` sums to exactly 100,
   this raises `ZeroDivisionError` and aborts the entire standardization run;
   when it exceeds 100, it silently produces a **negative** display price that
   ships to the store as a valid-looking number.
2. **`price_utils.py:112` (`select_effective_price`)** treats a sale price of
   `"0"` / `"0.0"` as a real sale. WooCommerce exports commonly emit
   `sale_price="0"` for non-sale items, so those products get an effective price
   of 0 — which makes `compare_scans` report spurious ~100% price drops and
   floods the change report with false positives.

Price code is exactly the kind of pure, high-consequence logic that must be
pinned by tests before and after a change. This plan characterizes current
behavior, then fixes both bugs.

## Current state

**File A — `product_extraction/common/price_utils.py`**

Import-fallback convention at the top (lines 9-18) — your test must import the
module the same dual way:
```python
try:
    from common.text_utils import (THOUSANDS_SEPARATORS, normalize_digits)
except ImportError:
    from product_extraction.common.text_utils import (THOUSANDS_SEPARATORS, normalize_digits)
```

The function to fix (lines 112-123):
```python
def select_effective_price(regular_price, sale_price):
    """Return the sale price when present, otherwise the regular price."""
    for value in (sale_price, regular_price):
        if value is None:
            continue
        text = str(value).strip()
        if text and text.lower() not in {"nan", "none"}:
            try:
                return int(float(text))
            except ValueError:
                continue
    return None
```

Consumed at `product_extraction/trackers/compare_scans.py:465-466`
(`effective_price(regular, sale)`), which is why a wrong 0 pollutes the change report.

**File B — `product_extraction/standardizer/step_pricing.py`**

`round_price` helper (lines 7-9):
```python
def round_price(price):
    """Round to nearest 1000 (matches JS Math.round behavior)."""
    return int(price / 1000 + 0.5) * 1000
```

The buggy block (lines 101-110):
```python
        total_discount = price_range['discount_percent'] + extra_discount_percent

        if total_discount > 0:
            final_sale_price = new_price
            display_price = final_sale_price / (1 - total_discount / 100)
            df.at[idx, base_price_col] = round_price(display_price)
            df.at[idx, sale_price_col] = final_sale_price
            discounts_applied += 1
        else:
            df.at[idx, base_price_col] = new_price
```

## Commands you will need

| Purpose | Command | Expected on success |
|---------|---------|---------------------|
| Compile A | `python -m py_compile product_extraction/common/price_utils.py` | exit 0 |
| Compile B | `python -m py_compile product_extraction/standardizer/step_pricing.py` | exit 0 |
| Run new tests | `python -m pytest tests/test_price_utils.py tests/test_step_pricing.py -v` | all pass |
| Full test run | `python -m pytest tests/ -v` | all pass |

Run from repo root. `pytest==7.4.3` is already declared in
`product_extraction/requirements.txt`.

## Scope

**In scope** (the only files you should modify/create):
- `product_extraction/common/price_utils.py` (edit `select_effective_price` only)
- `product_extraction/standardizer/step_pricing.py` (edit the discount block only)
- `tests/test_price_utils.py` (create)
- `tests/test_step_pricing.py` (create)
- `plans/README.md` (status row only)

**Out of scope** (do NOT touch):
- `product_extraction/trackers/compare_scans.py` — it consumes the fixed
  function; its behavior improves automatically. Do not modify it.
- Any other function in `price_utils.py` (`parse_numeric_price`,
  `extract_price_from_text`, etc.) — leave them exactly as-is.
- The pricing config/Excel files.

## Git workflow

- Branch: `advisor/003-price-fixes`
- Commit the characterization tests first (Step 1), then each fix with its own
  commit. Short imperative messages (see `git log`).
- Do NOT push or open a PR unless the operator instructs it.

## Steps

### Step 1: Characterize current behavior FIRST (tests before fixes)

Create `tests/test_price_utils.py`. Import using the same dual-fallback the
module uses:
```python
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
    # After the fix, a "0" sale price must NOT be treated as a real sale.
    assert select_effective_price("100000", "0") == 100000
    assert select_effective_price("100000", "0.0") == 100000

def test_both_missing_returns_none():
    assert select_effective_price(None, None) is None

def test_zero_regular_and_zero_sale_returns_none():
    # No usable positive price anywhere.
    assert select_effective_price("0", "0") is None
```

Create `tests/test_step_pricing.py`:
```python
import pytest
try:
    from product_extraction.standardizer.step_pricing import round_price
except ImportError:
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "product_extraction"))
    from standardizer.step_pricing import round_price

# round_price is unchanged — pin it so a refactor can't silently alter rounding.
def test_round_price_nearest_1000():
    assert round_price(80400) == 80000
    assert round_price(80500) == 81000
    assert round_price(0) == 0
```
(The discount-block behavior is tested indirectly; if `process` can be called
with a small synthetic DataFrame without heavy setup, add a direct test in
Step 3. If it requires large fixtures, the `round_price` pin plus the guard
assertion in Step 3 is sufficient — do not build elaborate fixtures.)

Run: `python -m pytest tests/test_price_utils.py tests/test_step_pricing.py -v`.
**Expected NOW**: `test_zero_sale_price_falls_through_to_regular` and
`test_zero_regular_and_zero_sale_returns_none` **FAIL** (current code returns 0),
the rest pass. This red state confirms the tests capture the bug. Do not proceed
until you see exactly those failures.

### Step 2: Fix `select_effective_price` to reject non-positive values

In `product_extraction/common/price_utils.py`, change the function so a parsed
value `<= 0` falls through instead of being returned:
```python
def select_effective_price(regular_price, sale_price):
    """Return the sale price when it is a real (positive) sale, otherwise the
    regular price. A value of 0 / 0.0 is treated as 'no sale', not a free item,
    because WooCommerce exports emit sale_price=0 for non-sale products."""
    for value in (sale_price, regular_price):
        if value is None:
            continue
        text = str(value).strip()
        if text and text.lower() not in {"nan", "none"}:
            try:
                parsed = int(float(text))
            except ValueError:
                continue
            if parsed > 0:
                return parsed
    return None
```

Run the tests again. **Expected**: all `test_price_utils.py` tests pass.

**Verify**: `python -m pytest tests/test_price_utils.py -v` → all pass.

### Step 3: Guard `step_pricing` against total_discount >= 100

In `product_extraction/standardizer/step_pricing.py`, replace the discount block
(lines 101-110) with a clamped/guarded version:
```python
        total_discount = price_range['discount_percent'] + extra_discount_percent

        if total_discount >= 100:
            # A discount of 100%+ would divide by zero or produce a negative
            # display price. Clamp and warn rather than shipping a bad price.
            print(f"[step_pricing] WARNING: total_discount={total_discount} >= 100 "
                  f"at row {idx}; clamping to 99 to avoid invalid price.")
            total_discount = 99

        if total_discount > 0:
            final_sale_price = new_price
            display_price = final_sale_price / (1 - total_discount / 100)
            df.at[idx, base_price_col] = round_price(display_price)
            df.at[idx, sale_price_col] = final_sale_price
            discounts_applied += 1
        else:
            df.at[idx, base_price_col] = new_price
```
Keep the module's existing logging style — it uses `print(...)` elsewhere, so a
`print` warning matches convention. If the file already imports a logger, use
that instead.

Add a direct test to `tests/test_step_pricing.py` ONLY if `process` is callable
with a light synthetic DataFrame (inspect `process`'s signature at
`step_pricing.py:50` and the columns it reads). A minimal case:
```python
def test_discount_at_100_does_not_crash_or_go_negative():
    import pandas as pd
    from standardizer.step_pricing import process  # adjust import to match Step 1 style
    # Build the smallest df/pricing_data that reaches the discount branch.
    # If setup is heavy, SKIP this test and rely on the guard + code review.
    ...
```
If the setup is non-trivial, do not force it — note in your status that the
guard is covered by inspection + the `round_price` pin, not a direct unit test.

**Verify**: `python -m py_compile product_extraction/standardizer/step_pricing.py` → exit 0;
`python -m pytest tests/ -v` → all pass.

### Step 4: Confirm no output regression (if plan 001 is done)

If `tests/baseline_compare.py` exists (from plan 001), and you can regenerate a
WooCommerce CSV from the baseline input without live scraping, call
`compare_woocommerce(regenerated, golden)` and confirm it returns `[]`. If
regeneration requires scraping (it does for the full pipeline), skip this step
and record that the change is covered by unit tests only.

**Verify**: `python -m pytest tests/ -v` → all pass.

### Step 5: Update the status row

In `plans/README.md`, change plan 003's status to `DONE`.

## Test plan

- `tests/test_price_utils.py`: sale-used, regular-fallback, **zero-sale
  fall-through** (the bug), both-missing, zero/zero → None.
- `tests/test_step_pricing.py`: `round_price` pin; optionally the 100%-discount
  guard if `process` is lightly callable.
- Pattern to follow: plan 001's `tests/` files if present; otherwise these
  establish the pattern (dual-import fallback, plain pytest functions).
- Verification: `python -m pytest tests/ -v` → all pass, including the new cases.

## Done criteria

Machine-checkable. ALL must hold:

- [ ] `python -m pytest tests/test_price_utils.py -v` — all pass, including the two zero-value cases
- [ ] `python -m py_compile product_extraction/common/price_utils.py product_extraction/standardizer/step_pricing.py` exits 0
- [ ] `grep -n "parsed > 0" product_extraction/common/price_utils.py` returns a match
- [ ] `grep -n "total_discount >= 100" product_extraction/standardizer/step_pricing.py` returns a match
- [ ] `python -m pytest tests/ -v` exits 0 (whole suite green)
- [ ] No files outside the in-scope list are modified (`git status`)
- [ ] `plans/README.md` status row for 003 shows DONE

## STOP conditions

Stop and report back (do not improvise) if:

- The live code at the cited lines does not match the "Current state" excerpts.
- After Step 1, the tests do NOT fail on the two zero-value cases — that means
  the bug is not what this plan assumed (maybe already fixed); report before changing code.
- Treating `sale_price=0` as "no sale" turns out to hide a legitimately free/promotional
  product in this business (ask the operator) — the domain assumption is that 0 means "no sale".
- The `step_pricing` guard changes a large number of baseline prices when you
  run plan 001's comparison — that suggests real data currently hits the >=100
  path and someone must decide the intended behavior.

## Maintenance notes

- The "0 means no sale" rule is a domain assumption encoded in
  `select_effective_price`. If the store ever sells genuinely free items, this
  needs a different sentinel (e.g. distinguish empty from "0").
- The `total_discount` clamp to 99 is a safety floor, not a business rule — if
  the pricing config legitimately needs ≥100% behavior, revisit with the operator.
- A reviewer should confirm `compare_scans.py`'s false-positive change reports
  actually decrease after this fix (the downstream payoff).
