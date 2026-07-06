# Central Configuration Design

## Executive Summary

The current repository uses a mixture of:

* Excel configuration files
* Python settings modules
* Environment variables
* Hardcoded filenames
* Hardcoded directory paths

The objective is to create a centralized configuration architecture that:

* Preserves existing behavior
* Allows gradual adoption
* Minimizes migration risk
* Supports rollback at every stage
* Avoids large-scale refactoring

This design intentionally favors compatibility over architectural purity.

---

# Design Principles

## 1. Backward Compatibility First

Existing modules must continue functioning without modification during early migration phases.

No existing configuration source should be removed until migration is complete.

---

## 2. Single Source of Truth

Configuration definitions should eventually exist in one centralized location.

Consumers should read configuration through a shared configuration API rather than directly reading files.

---

## 3. Incremental Adoption

Migration should occur module-by-module.

No repository-wide configuration rewrite.

---

## 4. Reversible Changes

Every migration step must be independently reversible.

Rollback must not require code reconstruction.

---

# Proposed Structure

## Future Configuration Layers

### Layer 1 — Environment Configuration

Contains:

* Secrets
* Environment-specific settings
* Runtime options

Examples:

* SECRET_KEY
* DEBUG
* LOG_LEVEL

---

### Layer 2 — Application Configuration

Contains:

* Application behavior
* Feature settings
* Processing limits
* Timeouts

Examples:

* Retry counts
* Batch sizes
* History retention settings

---

### Layer 3 — File Configuration

Contains:

* Input filenames
* Output filenames
* Folder locations
* Report locations

Examples:

* archive_urls.xlsx
* extracted_products.xlsx
* product_details_complete.xlsx

---

### Layer 4 — Business Configuration

Contains:

* Color mappings
* Category mappings
* Product naming rules
* Pricing rules

Examples:

* color_mapping.xlsx
* product_names.xlsx
* standard_categories.xlsx

---

# Proposed Directory Layout

```text
config/
│
├── __init__.py
│
├── environment.py
├── application.py
├── paths.py
├── files.py
│
├── loaders/
│   ├── excel_loader.py
│   ├── csv_loader.py
│   └── mapping_loader.py
│
├── mappings/
│   ├── color_mapping.xlsx
│   ├── product_names.xlsx
│   ├── standard_categories.xlsx
│   └── standard_colors.xlsx
│
└── schema/
    ├── file_registry.py
    └── config_registry.py
```

---

# Central Registry Concept

## File Registry

Purpose:

Maintain a single authoritative location for all repository file references.

Example:

```python
FILES = {
    "archive_urls": "archive_urls.xlsx",
    "extracted_products": "extracted_products.xlsx",
    "product_details": "product_details_complete.xlsx",
    "tracking": "product_tracking_LATEST.xlsx"
}
```

Benefits:

* Eliminates filename duplication.
* Simplifies future renames.
* Enables validation.

---

## Path Registry

Purpose:

Maintain all directory definitions.

Example:

```python
PATHS = {
    "uploads": "uploads",
    "reports": "reports",
    "logs": "logs",
    "images": "product-images"
}
```

Benefits:

* Removes path scattering.
* Supports environment portability.

---

# Configuration Access Model

## Current State

```text
Script
 └── Reads XLSX
 └── Reads Path
 └── Uses Hardcoded Filename
```

---

## Future State

```text
Script
    │
    ▼
Config API
    │
    ├── Registry
    ├── Environment
    ├── File Definitions
    └── Mapping Loader
```

Benefits:

* Centralized validation.
* Reduced duplication.
* Easier testing.

---

# Migration Sequence

## Phase A — Create Configuration Layer

Objective:

Add centralized configuration package.

Actions:

* Create config directory.
* Create registry files.
* Mirror existing settings.

Risk:

Very Low

Rollback:

Delete new config package.

---

## Phase B — Introduce Read-Only Adapters

Objective:

Expose existing settings through centralized API.

Actions:

* Registry references existing files.
* Existing modules remain unchanged.

Risk:

Very Low

Rollback:

Remove adapters.

---

## Phase C — Migrate File References

Objective:

Replace hardcoded filenames.

Actions:

Update modules gradually.

Example:

Before:

```python
"archive_urls.xlsx"
```

After:

```python
FILES["archive_urls"]
```

Risk:

Low

Rollback:

Restore previous literal values.

---

## Phase D — Migrate Path References

Objective:

Remove hardcoded directories.

Actions:

Replace literal folder names with registry values.

Risk:

Low

Rollback:

Revert modified modules.

---

## Phase E — Consolidate Mapping Files

Objective:

Create shared mapping repository.

Actions:

* Move color mappings.
* Move category mappings.
* Move naming mappings.

Risk:

Medium

Rollback:

Restore original file locations.

---

## Phase F — Remove Duplicate Configuration

Objective:

Retire obsolete settings.

Actions:

* Remove legacy path definitions.
* Remove duplicated mapping references.

Risk:

Medium

Rollback:

Restore archived configuration files.

---

# Rollback Strategy

## Rule 1

Never delete existing configuration during migration.

Only add new configuration.

---

## Rule 2

Maintain compatibility shims.

Example:

```python
from config.files import FILES
```

should coexist with:

```python
settings.INPUT_FILE
```

during migration.

---

## Rule 3

One Migration Unit Per Commit

Recommended units:

* File registry
* Path registry
* Module migration
* Mapping consolidation

This enables targeted rollback.

---

## Rule 4

Retain Legacy Files Until Validation Completes

Do not remove:

* settings.py
* config_v9.py
* paths.py

until migration verification passes.

---

# Risks

## Risk 1 — Hidden File Dependencies

Some scripts may rely on undocumented filenames.

Impact:

High

Mitigation:

Repository-wide filename inventory before migration.

---

## Risk 2 — Duplicate Mapping Divergence

Two mapping files may contain different values.

Impact:

High

Mitigation:

Compare contents before consolidation.

---

## Risk 3 — Legacy Module Assumptions

Older scripts may bypass settings modules.

Impact:

Medium

Mitigation:

Module-by-module migration.

---

## Risk 4 — Import Path Breakage

Centralization may alter import chains.

Impact:

Medium

Mitigation:

Introduce compatibility wrappers.

---

## Risk 5 — Environment Drift

Local environments may rely on undocumented settings.

Impact:

Medium

Mitigation:

Create environment inventory before migration.

---

# Required Code Changes

## New Files

Create:

```text
config/
    environment.py
    application.py
    files.py
    paths.py
```

---

## New Registries

Create:

```text
config/schema/file_registry.py
config/schema/config_registry.py
```

---

## New Loaders

Create:

```text
config/loaders/excel_loader.py
config/loaders/csv_loader.py
config/loaders/mapping_loader.py
```

---

## Module Updates

Future migrations will update:

### Product Extraction

* link_scraper.py
* spec_scraper.py
* price_tracker.py
* compare_scans.py

### Import Builder

* woocommerce_generator_v12.py
* web_panel_v12.py
* image_naming_v11_fixed.py

### Data Standardization

* category standardization modules
* pricing modules
* color standardization modules

---

# Recommended Migration Order

1. Configuration package creation
2. Registry creation
3. Read-only compatibility layer
4. Filename centralization
5. Path centralization
6. Mapping centralization
7. Legacy configuration retirement

This sequence minimizes operational risk while preserving complete rollback capability.

---

# Go / No-Go Assessment

Recommendation: GO

Conditions:

* No behavioral changes.
* Configuration package introduced as an additive layer.
* Existing settings retained during migration.
* Validation performed after each migration unit.

This design supports a safe, incremental transition toward centralized configuration management while maintaining compatibility with the current pipeline.
