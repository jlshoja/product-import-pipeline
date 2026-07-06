# Hardcoded Path Inventory

## Executive Summary

The repository contains a significant number of hardcoded:

* Filenames
* Folder names
* Report locations
* Upload locations
* Mapping file references
* Runtime path assumptions

Most issues are concentrated in:

* `product_extraction/`
* `import_builder/`
* `image_processing/`

Overall Migration Risk: **Medium–High**

---

# Critical Findings

## product_extraction/scrapers/link_scraper.py

### Line 23

**Current Value**

```text
link_scraper_progress.json
```

**Usage**

Persistent scraper state.

**Migration Risk**

High

**Recommended Replacement**

```python
config.files.PROGRESS_FILE
```

---

### Line 24

**Current Value**

```text
checkpoint.xlsx
```

**Usage**

Incremental checkpoint storage.

**Migration Risk**

High

**Recommended Replacement**

```python
config.files.CHECKPOINT_FILE
```

---

### Line 26

**Current Value**

```text
archive_urls.xlsx
```

**Usage**

Primary scraper input.

**Migration Risk**

High

**Recommended Replacement**

```python
config.files.ARCHIVE_URLS_FILE
```

---

### Line 27

**Current Value**

```text
extracted_products.xlsx
```

**Usage**

Primary scraper output.

**Migration Risk**

High

**Recommended Replacement**

```python
config.files.EXTRACTED_PRODUCTS_FILE
```

---

# product_extraction/scrapers/spec_scraper.py

### Line 1106

**Current Value**

```text
scraper_progress.json
```

**Usage**

Progress persistence.

**Migration Risk**

High

**Recommended Replacement**

```python
config.files.SCRAPER_PROGRESS_FILE
```

---

### Line 1253

**Current Value**

```text
extracted_products.xlsx
```

**Usage**

Specification scraper input.

**Migration Risk**

High

**Recommended Replacement**

```python
config.files.EXTRACTED_PRODUCTS_FILE
```

---

### Line 1254

**Current Value**

```text
product_details_complete.xlsx
```

**Usage**

Specification scraper output.

**Migration Risk**

High

**Recommended Replacement**

```python
config.files.PRODUCT_DETAILS_FILE
```

---

### Line 1249

**Current Value**

```text
reports
```

**Usage**

Report output directory.

**Migration Risk**

Medium

**Recommended Replacement**

```python
config.paths.REPORTS_DIR
```

---

### Line 1363

**Current Value**

```text
color_mapping.xlsx
```

**Usage**

Color normalization.

**Migration Risk**

High

**Recommended Replacement**

```python
config.files.COLOR_MAPPING_FILE
```

---

# product_extraction/main.py

### Line 55

**Current Value**

```text
archive_urls.xlsx
```

**Usage**

Default extraction input.

**Migration Risk**

High

**Recommended Replacement**

Central file registry.

---

### Line 75

**Current Value**

```text
extracted_products.xlsx
```

**Usage**

Spec scraper default input.

**Migration Risk**

High

**Recommended Replacement**

Central file registry.

---

### Line 95

**Current Value**

```text
extracted_products.xlsx
```

**Usage**

Price tracker default input.

**Migration Risk**

High

**Recommended Replacement**

Central file registry.

---

# product_extraction/config/settings.py

### Line 21

**Current Value**

```text
data
```

**Usage**

Data directory definition.

**Migration Risk**

Medium

**Recommended Replacement**

Central path registry.

---

### Line 22

**Current Value**

```text
reports/outputs
```

**Usage**

Report storage.

**Migration Risk**

Medium

**Recommended Replacement**

Central path registry.

---

### Line 23

**Current Value**

```text
reports/templates
```

**Usage**

Template location.

**Migration Risk**

Medium

**Recommended Replacement**

Central path registry.

---

### Line 24

**Current Value**

```text
logs
```

**Usage**

Application logging.

**Migration Risk**

Medium

**Recommended Replacement**

Central path registry.

---

### Lines 55–58

**Current Values**

```text
archive_urls.xlsx
extracted_products.xlsx
product_details_complete.xlsx
scraper_progress.json
```

**Usage**

Core pipeline filenames.

**Migration Risk**

High

**Recommended Replacement**

File registry.

---

### Line 95

**Current Value**

```text
color_mapping.xlsx
```

**Usage**

Color mapping source.

**Migration Risk**

High

**Recommended Replacement**

Shared configuration registry.

---

### Lines 115–116

**Current Values**

```text
extracted_products.xlsx
product_tracking_LATEST.xlsx
```

**Usage**

Tracking inputs and outputs.

**Migration Risk**

High

**Recommended Replacement**

File registry.

---

# product_extraction/config/history_config.py

### Line 21

**Current Value**

```text
price_history.xlsx
```

**Usage**

Historical pricing store.

**Migration Risk**

Medium

**Recommended Replacement**

File registry.

---

# product_extraction/reports/dashboard_generator.py

### Line 35

**Current Value**

```text
reports/templates
```

**Usage**

Dashboard template discovery.

**Migration Risk**

Medium

**Recommended Replacement**

Path registry.

---

### Line 36

**Current Value**

```text
reports/outputs
```

**Usage**

Dashboard output directory.

**Migration Risk**

Medium

**Recommended Replacement**

Path registry.

---

# product_extraction/trackers/compare_scans.py

### Line 573

**Current Value**

```text
../reports
```

**Usage**

Report lookup.

**Migration Risk**

Medium

**Recommended Replacement**

Path registry.

---

### Lines 575–577

**Current Values**

```text
../../4_Product_import/uploads
../4_Product_import/uploads
../uploads
```

**Usage**

Upload discovery.

**Migration Risk**

Very High

**Recommended Replacement**

```python
config.paths.UPLOADS_DIR
```

---

### Line 83

**Current Value**

```text
product_details_*.xlsx
```

**Usage**

Historical report discovery.

**Migration Risk**

Medium

**Recommended Replacement**

Report naming policy configuration.

---

### Line 102

**Current Value**

```text
extracted_products*.xlsx
```

**Usage**

Extraction output discovery.

**Migration Risk**

Medium

**Recommended Replacement**

File naming registry.

---

### Line 107

**Current Value**

```text
woocommerce_import_*.csv
```

**Usage**

WooCommerce import discovery.

**Migration Risk**

Medium

**Recommended Replacement**

Export naming policy configuration.

---

# import_builder/web_panel_v12.py

### Line 55

**Current Value**

```text
uploads
```

**Usage**

Flask upload directory.

**Migration Risk**

High

**Recommended Replacement**

```python
config.paths.UPLOADS_DIR
```

---

### Line 66

**Current Value**

```text
product-images
```

**Usage**

Image repository.

**Migration Risk**

High

**Recommended Replacement**

```python
config.paths.PRODUCT_IMAGES_DIR
```

---

### Line 79

**Current Value**

```text
color_mapping.xlsx
```

**Usage**

Color mapping.

**Migration Risk**

High

**Recommended Replacement**

Central mapping registry.

---

### Line 86

**Current Value**

```text
product_names.xlsx
```

**Usage**

Product naming.

**Migration Risk**

High

**Recommended Replacement**

Central mapping registry.

---

# import_builder/woocommerce_generator_v12.py

### Line 26

**Current Value**

```text
color_mapping.xlsx
```

**Usage**

Color normalization.

**Migration Risk**

High

**Recommended Replacement**

Shared mapping configuration.

---

### Line 27

**Current Value**

```text
product_names.xlsx
```

**Usage**

Product naming.

**Migration Risk**

High

**Recommended Replacement**

Shared mapping configuration.

---

### Line 71

**Current Value**

```text
product-images
```

**Usage**

Image source folder.

**Migration Risk**

High

**Recommended Replacement**

Path registry.

---

### Lines 463–465

**Current Values**

```text
../4_Product_import/uploads
uploads
```

**Usage**

Upload directory discovery.

**Migration Risk**

Very High

**Recommended Replacement**

Path registry.

---

# import_builder/paths.py

### Line 16

**Current Value**

```text
data
```

**Usage**

Data directory.

**Migration Risk**

Medium

**Recommended Replacement**

Central path registry.

---

### Line 19

**Current Value**

```text
logs
```

**Usage**

Logging directory.

**Migration Risk**

Medium

**Recommended Replacement**

Central path registry.

---

### Lines 22–23

**Current Values**

```text
color_mapping.xlsx
product_names.xlsx
```

**Usage**

Configuration files.

**Migration Risk**

High

**Recommended Replacement**

Central file registry.

---

# import_builder/color_manager.py

### Line 32

**Current Value**

```text
color_mapping.xlsx
```

**Usage**

Default configuration file.

**Migration Risk**

High

**Recommended Replacement**

Shared mapping registry.

---

### Line 302

**Current Value**

```text
color_mapping.xlsx
```

**Usage**

Runtime initialization.

**Migration Risk**

High

**Recommended Replacement**

Shared mapping registry.

---

# import_builder/product_name_manager.py

### Line 114

**Current Value**

```text
product_names.xlsx
```

**Usage**

Default naming configuration.

**Migration Risk**

High

**Recommended Replacement**

Shared mapping registry.

---

# image_processing/menu.py

### Line 15

**Current Value**

```text
extracted_products.xlsx
```

**Usage**

Image workflow input.

**Migration Risk**

High

**Recommended Replacement**

Central file registry.

---

### Lines 86–87

**Current Value**

```text
download_state.json
```

**Usage**

Download state persistence.

**Migration Risk**

Medium

**Recommended Replacement**

File registry.

---

# image_processing/Image_Downloader.py

### Line 30

**Current Value**

```text
download_state.json
```

**Usage**

Download recovery state.

**Migration Risk**

Medium

**Recommended Replacement**

File registry.

---

### Line 801

**Current Value**

```text
extracted_products.xlsx
```

**Usage**

Default environment fallback.

**Migration Risk**

Medium

**Recommended Replacement**

File registry.

---

# Environment Assumptions

## Flask Secret Key

### File

import_builder/web_panel_v12.py

### Assumption

Application expects:

```text
SECRET_KEY
```

to exist or fallback behavior is acceptable.

### Migration Risk

High

### Recommended Replacement

Central environment loader.

---

## Relative Repository Layout

### Files

* compare_scans.py
* woocommerce_generator_v12.py
* dashboard_generator.py
* settings.py

### Assumption

Repository folders always remain:

```text
reports/
uploads/
data/
logs/
product-images/
```

in expected relative positions.

### Migration Risk

Very High

### Recommended Replacement

Central path registry.

---

# Highest-Risk Findings

1. `../../4_Product_import/uploads`
2. `../4_Product_import/uploads`
3. `uploads`
4. `product-images`
5. `archive_urls.xlsx`
6. `extracted_products.xlsx`
7. `product_details_complete.xlsx`
8. `color_mapping.xlsx`
9. `product_names.xlsx`
10. `scraper_progress.json`

These should be prioritized during configuration centralization because they create the strongest coupling between modules and repository layout.

---

# SESSION_HANDOFF.md Update Recommendation

Add the following section:

## Phase 4 Completed — Hardcoded Path Inventory

Completed:

* Repository-wide scan for hardcoded paths
* Hardcoded folder inventory
* Hardcoded filename inventory
* Environment assumption inventory

Key Findings:

* Significant filename coupling remains
* Upload path assumptions exist in multiple modules
* Color mapping and naming files are duplicated across modules
* Repository structure assumptions are embedded in tracker and import-builder workflows

Recommended Next Phase:

Phase 5 — Configuration Abstraction Planning

Objective:

Replace direct path and filename usage with centralized configuration access while maintaining backward compatibility and rollback capability.
