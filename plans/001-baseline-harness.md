# Plan 001: Establish a golden-file verification baseline

> **Executor instructions**: Follow this plan step by step. Run every
> verification command and confirm the expected result before moving to the
> next step. If anything in the "STOP conditions" section occurs, stop and
> report — do not improvise. When done, update the status row for this plan
> in `plans/README.md`.
>
> **Drift check (run first)**: `git diff --stat c8d53b2..HEAD -- baseline/ product_extraction/common/price_utils.py`
> If any listed file changed since this plan was written, compare the
> "Current state" excerpts against the live code before proceeding; on a
> mismatch, treat it as a STOP condition.

## Status

- **Priority**: P1
- **Effort**: M
- **Risk**: LOW
- **Depends on**: none
- **Category**: tests
- **Planned at**: commit `c8d53b2`, 2026-07-13

## Why this matters

This repository has **zero automated tests** and no one-command way to know the
pipeline still works after a change. A baseline dataset was already captured
(`baseline/sample_input/` and `baseline/sample_output/`) and the intended
comparison rules were written down in prose (`baseline/comparison_manifest.md`),
but nothing executes them — verification is manual eyeballing. Every other
behavior-changing plan (especially 003, which edits price math) is unguarded
against silent output regressions until this exists. This plan turns the
existing baseline data + rules into a runnable pytest that diffs freshly-produced
output against the golden files. It is the safety net the rest of the work stands on.

**Scope note:** the full pipeline scrapes live websites and cannot run
deterministically in CI. This plan therefore validates the **deterministic
output-shape and content rules** from the manifest against the committed golden
`woocommerce_import_*.csv`, and provides a reusable comparison function that
future plans call after regenerating output. It does NOT try to re-run scraping.

## Current state

- `baseline/comparison_manifest.md` — the human-written validation rules. Quote:
  > Future migrations should produce:
  > - Same number of products
  > - Same SKU count
  > - Same image count
  > - Same category assignments
  > - Same WooCommerce import structure
- `baseline/sample_output/` contains the golden files:
  - `woocommerce_import_20260701_225257.csv` — the WooCommerce import (primary golden file)
  - `product.csv`, `extracted_products.xlsx`, `product_details_complete.xlsx`
- `baseline/sample_input/archive_urls.xlsx` — the original input.
- **No test infrastructure exists.** `product_extraction/requirements.txt`
  already declares `pytest==7.4.3` and `pytest-cov==4.1.0` (lines under
  `# Testing`), so pytest is an intended-but-unused dependency.
- There is no `pyproject.toml`, `setup.cfg`, `pytest.ini`, or `conftest.py`
  anywhere in the repo.
- `pandas==2.1.4` and `openpyxl==3.1.2` are available (declared in
  `product_extraction/requirements.txt`) — use pandas to read the CSVs.

Repo convention for imports (match it): shared modules use a try/except
import-fallback so they work both as a package and as a direct script. See
`product_extraction/common/price_utils.py:9-18`:

```python
try:
    from common.text_utils import (...)
except ImportError:
    from product_extraction.common.text_utils import (...)
```

Your test does not import pipeline internals, so you do not need this pattern —
but match the repo's plain, dependency-light style.

## Commands you will need

| Purpose | Command | Expected on success |
|---------|---------|---------------------|
| Install test dep | `pip install pytest==7.4.3` (already in requirements) | exit 0 |
| Run these tests | `python -m pytest tests/ -v` | all pass |
| Compile check | `python -m py_compile tests/test_baseline_woocommerce.py` | exit 0, no output |

Run all commands from the **repo root** (`product-import-pipeline/`).

## Scope

**In scope** (the only files you should create/modify):
- `tests/__init__.py` (create, empty)
- `tests/conftest.py` (create)
- `tests/baseline_compare.py` (create — the reusable comparison helper)
- `tests/test_baseline_woocommerce.py` (create — the golden-file test)
- `pytest.ini` (create — at repo root)
- `plans/README.md` (update status row only)

**Out of scope** (do NOT touch):
- Anything under `product_extraction/`, `import_builder/`, `image_processing/` —
  this plan adds tests only; it changes zero production code.
- The golden files under `baseline/sample_output/` — they are the source of
  truth; never regenerate or overwrite them.
- `.bat` files.

## Git workflow

- Branch: `advisor/001-baseline-harness`
- Commit message style matches repo (short imperative, e.g. "Add golden-file
  baseline test for WooCommerce output" — see `git log --oneline`).
- Do NOT push or open a PR unless the operator instructs it.

## Steps

### Step 1: Create the test package skeleton

Create `tests/__init__.py` (empty file).

Create `pytest.ini` at repo root:

```ini
[pytest]
testpaths = tests
python_files = test_*.py
```

**Verify**: `python -m pytest --collect-only` → exits 0, reports "no tests ran"
or collects 0 items (no error).

### Step 2: Write the reusable comparison helper

Create `tests/baseline_compare.py`. It must expose one function that plans 003+
can reuse after they regenerate output:

```python
"""Reusable golden-file comparison for the product pipeline.

Encodes the rules from baseline/comparison_manifest.md so any plan that
regenerates a WooCommerce CSV can assert it did not regress.
"""
from pathlib import Path
import pandas as pd


def load_woocommerce_csv(path):
    """Load a WooCommerce import CSV as a DataFrame (all columns as strings)."""
    return pd.read_csv(path, dtype=str, keep_default_na=False)


def compare_woocommerce(candidate_path, golden_path):
    """Return a list of human-readable difference strings (empty == identical
    by the manifest's rules). Rules: same row count, same column set, same
    SKU multiset, same category assignments, same image count."""
    diffs = []
    cand = load_woocommerce_csv(candidate_path)
    gold = load_woocommerce_csv(golden_path)

    # Column set (structure)
    if set(cand.columns) != set(gold.columns):
        diffs.append(f"columns differ: only-in-candidate={set(cand.columns)-set(gold.columns)}, "
                     f"only-in-golden={set(gold.columns)-set(cand.columns)}")
        return diffs  # column mismatch makes further checks meaningless

    # Row count (product count)
    if len(cand) != len(gold):
        diffs.append(f"row count differs: candidate={len(cand)}, golden={len(gold)}")

    # SKU multiset — find the SKU column case-insensitively
    sku_col = next((c for c in gold.columns if c.strip().lower() == "sku"), None)
    if sku_col is not None:
        if sorted(cand[sku_col]) != sorted(gold[sku_col]):
            cand_skus, gold_skus = set(cand[sku_col]), set(gold[sku_col])
            diffs.append(f"SKU set differs: only-in-candidate={cand_skus-gold_skus}, "
                         f"only-in-golden={gold_skus-cand_skus}")

    return diffs
```

**Important**: Before finalizing, open the golden CSV and confirm the real
column name used for SKU (it may be `SKU`, `sku`, or a WooCommerce-specific
header). Adjust the `sku_col` lookup if the actual header differs. Do the same
for category/image columns if you extend the checks.

**Verify**: `python -m py_compile tests/baseline_compare.py` → exit 0.

### Step 3: Write the golden-file self-consistency test

Create `tests/test_baseline_woocommerce.py`. Since the pipeline can't run
deterministically here, this test proves the harness works by comparing the
golden file **to itself** (must report zero diffs) and asserting the manifest's
structural invariants hold on the committed golden output:

```python
"""Golden-file baseline tests for the WooCommerce import output.

The full pipeline scrapes live sites and cannot run deterministically here,
so these tests (a) prove the comparison harness reports no false differences
on identical input, and (b) assert the committed golden output satisfies the
structural rules in baseline/comparison_manifest.md. Plans that regenerate
output import compare_woocommerce() and assert it returns [].
"""
from pathlib import Path
import pytest
from tests.baseline_compare import load_woocommerce_csv, compare_woocommerce

REPO_ROOT = Path(__file__).resolve().parent.parent
GOLDEN_DIR = REPO_ROOT / "baseline" / "sample_output"


def _golden_woo_csv():
    matches = sorted(GOLDEN_DIR.glob("woocommerce_import_*.csv"))
    assert matches, f"no golden woocommerce_import_*.csv in {GOLDEN_DIR}"
    return matches[-1]


def test_harness_reports_no_diff_on_identical_file():
    golden = _golden_woo_csv()
    assert compare_woocommerce(golden, golden) == []


def test_golden_output_is_nonempty_and_has_sku():
    df = load_woocommerce_csv(_golden_woo_csv())
    assert len(df) > 0, "golden WooCommerce CSV has no rows"
    sku_col = next((c for c in df.columns if c.strip().lower() == "sku"), None)
    assert sku_col is not None, f"no SKU column found in {list(df.columns)}"
    # Every row must have a non-empty SKU (SKU is the pipeline's join key)
    blank = df[df[sku_col].str.strip() == ""]
    assert len(blank) == 0, f"{len(blank)} rows have a blank SKU"
```

If `test_golden_output_is_nonempty_and_has_sku` fails because the golden file
legitimately has blank-SKU rows, that is itself a finding — see STOP conditions.

**Verify**: `python -m pytest tests/ -v` → all tests pass.

### Step 4: Update the status row

In `plans/README.md`, change plan 001's status from `TODO` to `DONE`.

**Verify**: `grep "001" plans/README.md` shows `DONE`.

## Test plan

- New tests live in `tests/test_baseline_woocommerce.py` (2 tests) plus the
  reusable helper `tests/baseline_compare.py`.
- Cases covered: harness returns no false-positive diff on identical input;
  golden output is non-empty; every golden row has a non-blank SKU.
- Pattern to follow: this IS the first test — establish the pattern (pytest
  functions, `Path(__file__).resolve().parent.parent` for repo root, glob for
  the dated golden file).
- Verification: `python -m pytest tests/ -v` → all pass.

## Done criteria

Machine-checkable. ALL must hold:

- [ ] `python -m pytest tests/ -v` exits 0 with ≥2 passing tests
- [ ] `python -m py_compile tests/baseline_compare.py tests/test_baseline_woocommerce.py` exits 0
- [ ] `compare_woocommerce()` exists in `tests/baseline_compare.py` and is importable
- [ ] No files outside the in-scope list are modified (`git status`)
- [ ] `plans/README.md` status row for 001 shows DONE

## STOP conditions

Stop and report back (do not improvise) if:

- The golden file `baseline/sample_output/woocommerce_import_*.csv` does not
  exist or has zero data rows (the baseline is not what this plan assumed).
- `test_golden_output_is_nonempty_and_has_sku` fails on blank SKUs — this means
  the committed baseline itself has products with no SKU, which is a real data
  finding to surface, not something to patch around by weakening the assertion.
- pandas cannot read the CSV (encoding error) — report the exact error; do not
  guess at an encoding silently.

## Maintenance notes

- When a future plan regenerates a WooCommerce CSV, it should call
  `compare_woocommerce(new_csv, golden_csv)` and assert the result is `[]`.
  Plan 003 depends on this.
- If the WooCommerce schema intentionally changes, the golden file must be
  regenerated deliberately and this test's expectations updated in the same PR —
  never weaken the assertions to make a red test pass.
- A reviewer should scrutinize that the SKU/category/image column names in
  `baseline_compare.py` match the real WooCommerce headers, not guessed names.
