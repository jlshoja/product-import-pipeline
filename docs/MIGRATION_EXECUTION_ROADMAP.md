# Migration Execution Roadmap

## Purpose

This document defines the execution sequence for the migration phase.

It bridges the gap between migration planning and migration implementation.

The roadmap defines:

* Migration units
* Execution order
* Dependencies
* Validation requirements
* Rollback requirements
* Unit boundaries

---

# Migration Principles

All migration work must follow these rules:

* Preserve backward compatibility.
* Prefer small, reversible changes.
* Validate after every migration unit.
* Do not mix unrelated changes.
* Do not perform opportunistic refactoring.
* Maintain output parity with the baseline.
* Maintain existing external interfaces.

---

# Migration Unit 1 — Path Management Foundation

## Objective

Centralize path handling and eliminate scattered path construction logic.

## Scope

* Path construction
* Repository-relative paths
* Output directories
* Temporary directories

## Excluded

* Business logic
* Excel processing
* Scraping logic

## Dependencies

* CONFIG_INVENTORY.md
* FILE_DEPENDENCIES.md

## Risk

Low

## Validation

* Import validation
* Path resolution validation
* Startup validation

## Rollback

Revert only Unit 1 changes.

---

# Migration Unit 2 — Configuration Centralization

## Objective

Centralize configuration access.

## Scope

* Configuration loading
* Environment settings
* Runtime settings

## Dependencies

* Unit 1

## Risk

Low-Medium

## Validation

* Configuration loading
* Environment validation
* Runtime startup validation

## Rollback

Revert only Unit 2 changes.

---

# Migration Unit 3 — Excel Operations Consolidation

## Objective

Consolidate repeated Excel operations into shared utilities.

## Scope

* Excel readers
* Excel writers
* Workbook creation
* Report exports

## Dependencies

* Unit 1
* Unit 2

## Risk

Medium

## Validation

* Input validation
* Output parity validation
* Regression comparison

## Rollback

Revert only Unit 3 changes.

---

# Migration Unit 4 — File Operations Consolidation

## Objective

Consolidate repeated filesystem operations.

## Scope

* File creation
* File movement
* Directory management
* Validation helpers

## Dependencies

* Unit 1

## Risk

Medium

## Validation

* File lifecycle validation
* Output validation

## Rollback

Revert only Unit 4 changes.

---

# Migration Unit 5 — Progress Tracking Consolidation

## Objective

Standardize progress persistence and recovery.

## Scope

* Progress files
* State recovery
* Resume functionality

## Dependencies

* Unit 4

## Risk

Medium

## Validation

* Resume validation
* Progress recovery testing

## Rollback

Revert only Unit 5 changes.

---

# Migration Unit 6 — Color Management Consolidation

## Objective

Centralize color translation and validation logic.

## Scope

* Color mapping
* Color validation
* Translation helpers

## Dependencies

* Unit 3

## Risk

Medium-High

## Validation

* Color mapping validation
* Product generation validation

## Rollback

Revert only Unit 6 changes.

---

# Migration Unit 7 — Shared Utility Consolidation

## Objective

Move reusable helpers into shared utility modules.

## Scope

* Common helpers
* Shared utility functions

## Dependencies

* Units 1-6

## Risk

High

## Validation

* Dependency validation
* Full regression testing

## Rollback

Revert only Unit 7 changes.

---

# Migration Unit 8 — Core Processing Logic Migration

## Objective

Migrate remaining high-dependency processing components.

## Scope

* Pipeline orchestration
* Core processing logic

## Dependencies

* All previous units

## Risk

Very High

## Validation

* End-to-end execution
* Baseline comparison
* Output parity verification

## Rollback

Revert only Unit 8 changes.

---

# Validation Standard

Every migration unit must complete:

1. Static validation
2. Import validation
3. Dependency validation
4. Functional validation
5. Regression validation
6. Representative end-to-end validation

---

# Execution Order

1. Path Management Foundation
2. Configuration Centralization
3. Excel Operations Consolidation
4. File Operations Consolidation
5. Progress Tracking Consolidation
6. Color Management Consolidation
7. Shared Utility Consolidation
8. Core Processing Logic Migration

---

# Completion Criteria

Migration execution is complete when:

* All migration units are complete.
* All validations pass.
* Baseline parity is maintained.
* No critical regressions remain open.
* Final migration validation succeeds.
