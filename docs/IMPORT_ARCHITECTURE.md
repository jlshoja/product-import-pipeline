# Import Architecture

## Purpose

This document describes the current import architecture of the project.

It exists to prevent runtime regressions during migration work.

Any migration that introduces shared modules must follow the rules defined here.

---

# Current Execution Modes

The project currently supports multiple execution modes.

Understanding these execution modes is required before modifying imports.

## Mode 1 — Main Entry Point

Example:

```bash
python main.py scrape-links
```

In this mode:

* main.py becomes the execution root.
* Imports are resolved relative to the product_extraction directory.
* Some modules are imported indirectly through main.py.

Examples:

```python
import scrapers.link_scraper
import trackers.price_tracker
```

---

## Mode 2 — Direct Script Execution

Example:

```bash
python trackers/compare_scans.py
```

In this mode:

* The executed file becomes the entry point.
* Python import resolution differs from main.py execution.
* Modules available in Mode 1 may not be available in Mode 2.

Examples:

```bash
python trackers/compare_scans.py
python reports/dashboard_generator.py
```

---

# Existing Import Patterns

The codebase currently contains multiple import styles.

## Pattern A

```python
from common.path_registry import REPORTS_DIR
```

Common in older modules.

---

## Pattern B

```python
from product_extraction.common.file_registry import FILES
```

Introduced during migration work.

---

## Pattern C

```python
from color_manager import ColorManager
```

Local module import.

Common in directly executed scripts.

---

# Compatibility Risk

A module that works correctly when executed through:

```bash
python main.py
```

may fail when executed directly:

```bash
python trackers/script.py
```

Typical error:

```text
ModuleNotFoundError
```

---

# Migration Rule

Before replacing imports with shared utilities:

Validate both:

## Validation A

Execution through main.py.

Example:

```bash
python main.py scrape-links
```

## Validation B

Direct script execution.

Example:

```bash
python trackers/compare_scans.py
```

Migration is not considered complete until both execution modes pass.

---

# Shared Utility Rule

When introducing a new shared utility:

Example:

```python
excel_utils.py
```

Do not assume a single import path will work everywhere.

Validate:

* Import resolution
* Runtime execution
* Script execution
* Main entry execution

before applying changes broadly.

---

# Unit 3 Lessons Learned

Excel Operations Consolidation initially failed because import compatibility was not evaluated before consumer migration.

The migration was rolled back.

Future migrations must:

1. Audit import architecture first.
2. Validate execution modes.
3. Define compatibility strategy.
4. Then migrate consumers.

---

# Approved Workflow

For every migration unit:

1. Create foundation.
2. Validate runtime compatibility.
3. Migrate one consumer.
4. Validate.
5. Commit.
6. Continue incrementally.

Never migrate multiple consumers before runtime validation.
