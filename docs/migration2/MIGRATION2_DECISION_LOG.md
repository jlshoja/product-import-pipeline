# Migration 2 Decision Log

## Purpose

This document captures the architectural and migration decisions made during Migration 2, including the rationale for each decision and the alternatives that were rejected or deferred.

---

## New Decisions

### Canonical runtime layout is authoritative

- Decision: `runtime/logs/`, `runtime/reports/`, `runtime/state/`, and `runtime/cache/` are the canonical homes for runtime artifacts.
- Rationale: This separates generated runtime artifacts from source code and makes workflow outputs predictable.
- Impact: Runtime writers were updated to prefer these folders, and legacy copies were removed after verification.

### Canonical data layout is authoritative

- Decision: `data/inputs/`, `data/intermediate/`, `data/outputs/`, `data/mappings/`, `data/reference/`, and `data/archives/` are the canonical data homes.
- Rationale: The repository’s spreadsheets fall into distinct lifecycle buckets and should not be mixed in module trees.
- Impact: Pipeline spreadsheets were moved into the appropriate canonical folders.

### Shared mappings stay centralized

- Decision: Shared mapping spreadsheets live in `data/mappings/`, with `data/archives/` used only for archived fallback copies.
- Rationale: Shared mappings need one canonical source of truth, but some validation and compatibility use cases still require an archived fallback.
- Impact: `color_mapping.xlsx` and `product_names.xlsx` were centralized; the legacy `color_mapping.xlsx` fallback was archived.

### Reusable templates and help assets move into `assets/`

- Decision: Reusable HTML/UI templates belong in `assets/templates/`, and user-facing help material belongs in `assets/help/`.
- Rationale: These files have a different lifecycle than live pipeline data and should not live beside executable code.
- Impact: Dashboard templates, the interactive product-extraction template, import-builder UI templates, and import-builder help files were moved.

### Generated caches may be removed after verification

- Decision: Generated caches such as `__pycache__` directories and empty migration debris folders can be removed once canonical replacements are verified.
- Rationale: They are not source assets and create noise after migration.
- Impact: Generated caches and empty wrapper directories were removed.

---

## Modified Decisions

### Legacy compatibility copies are temporary only

- Previous position: Keep legacy source-tree copies in place until later cleanup.
- Updated position: Retain legacy paths only as compatibility readers or archived fallbacks, not as duplicate source-tree files.
- Rationale: The canonical locations are now verified, so duplicate files add maintenance risk without operational value.

### Legacy dashboard report mirroring is retired

- Decision: Stop writing dashboard HTML to the legacy `reports/outputs/` mirror.
- Rationale: Smoke tests and alternate-working-directory regression checks confirmed the canonical runtime report path is sufficient.
- Impact: The dashboard generator now writes only to `runtime/reports/`.

### Legacy dashboard template fallback is retired

- Decision: Stop reading dashboard templates from the old `reports/templates/` location in shared settings and the dashboard generator.
- Rationale: The canonical asset template exists and the legacy template copy has already been removed.
- Impact: Template lookup now resolves directly from `assets/templates/` in the active code path.

### Legacy source-tree color-mapping fallback is retired

- Decision: Stop reading `product_extraction/color_mapping.xlsx` as a live fallback in the active color readers.
- Rationale: The canonical mapping lives in `data/mappings/`, and `data/archives/` is sufficient for recovery.
- Impact: The active readers no longer search the retired source-tree color mapping file.

### `product_extraction/color_mapping.xlsx` is archived, not retained in the source tree

- Previous position: Keep `product_extraction/color_mapping.xlsx` as a legacy fallback copy.
- Updated position: Archive the fallback at `data/archives/color_mapping.xlsx` and remove the source-tree duplicate.
- Rationale: The canonical mapping file in `data/mappings/` is now authoritative and the duplicate was redundant.

---

## Rejected Approaches

### Keeping runtime artifacts beside code

- Rejected because it perpetuates the same fragmentation Migration 2 is meant to eliminate.

### Keeping duplicate templates and help files in module-local folders

- Rejected because the canonical `assets/` layout already exists and the duplicates no longer add value.

### Leaving empty migration wrapper directories in place

- Rejected because they create false signals about active content and complicate future cleanup.

---

## Deferred Decisions

### Compatibility readers

- Deferred decision: whether to remove the remaining fallback search paths after alternate-working-directory regression checks.
- Why deferred: the repository still benefits from compatibility adapters until regression checks confirm no hidden legacy consumer remains.

### `data_standardization/`

- Deferred decision: whether to fold `data_standardization/` into `data/reference/` or keep it separate.
- Why deferred: the repository still needs a deliberate classification of those reference assets.

### Legacy scripts under `scrapers/Old/`

- Deferred decision: whether to keep them as archive-only material or retire them.
- Why deferred: they may still serve as historical reference or compatibility anchors.

### Historical image download sessions

- Deferred decision: whether to preserve or archive historical folders under `image_processing/downloaded_images/`.
- Why deferred: the current migration only required runtime state and cache standardization, not preservation policy for historical sessions.

---

## Decision Summary

- Canonical runtime, data, and asset homes are now established.
- Duplicate source-tree artifacts were removed after the canonical copies were verified.
- Remaining decisions are focused on validation, compatibility retirement, and archival policy.
