# Migration Operational Guide

## Purpose

This guide defines the standard workflow for all migration sessions after bootstrap is complete.

Use this guide for every migration session until migration closure.

Do not use the Bootstrap Guide once migration tracking has been initialized.

---

# Session Startup

At the beginning of every session:

Read:

* docs/MIGRATION_STATUS.md
* docs/SESSION_HANDOFF.md

Determine:

* Current migration phase
* Completed migration units
* Remaining migration units
* Open risks
* Open blockers
* Recommended next action

Then read only the documents required for the current phase.

Rules:

* Do not repeat discovery.
* Do not repeat architecture analysis.
* Do not repeat readiness validation.
* Do not repeat completed migration units.
* Preserve backward compatibility.
* Favor small, testable, reversible changes.

Expected Result:

AI identifies exactly where migration currently stands.

---

# Phase 1 — Migration Phase Review

Review:

* docs/MIGRATION_STATUS.md
* docs/SESSION_HANDOFF.md
* docs/MIGRATION_EXECUTION_ROADMAP.md

Determine:

* Current migration unit
* Previous completed units
* Remaining units
* Dependencies
* Validation requirements

Produce:

# Migration Session Plan

Include:

* Current Unit
* Scope
* Risks
* Validation Plan
* Rollback Plan

Do not modify code.

Expected Result:

Implementation plan for the next migration unit.

---

# Phase 2 — Pre-Implementation Review

Read only documents relevant to the selected migration unit.

Examples:

* FILE_DEPENDENCIES.md
* CONFIG_INVENTORY.md
* SHARED_UTILITY_INVENTORY.md
* Architecture references related to the unit

Determine:

* Files affected
* Dependencies
* Runtime impact
* Validation requirements

Produce:

# Migration Unit Review

Include:

* Scope
* Files likely affected
* Risks
* Validation approach
* Rollback approach

Do not modify code.

Expected Result:

Migration unit is fully understood before implementation.

---

# Phase 3 — Migration Implementation

Implement only the selected migration unit.

Rules:

* Small change set
* Reversible change set
* Backward compatible
* No unrelated refactoring
* No optimization outside migration scope
* No feature additions

Expected Result:

Migration unit completed.

---

# Phase 4 — Validation

Perform:

## Static Validation

Verify:

* Imports
* Syntax
* Startup

---

## Dependency Validation

Verify:

* Dependency integrity
* Interface compatibility

---

## Functional Validation

Verify:

* Existing behavior preserved

---

## Regression Validation

Compare:

* Outputs
* Generated files
* Baseline artifacts

---

## End-to-End Validation

Execute representative workflow.

Expected Result:

Migration unit validated.

---

# Phase 5 — Status Update

Update:

* docs/MIGRATION_STATUS.md
* docs/SESSION_HANDOFF.md

Record:

* Migration unit completed
* Files modified
* Validation performed
* Regression results
* Open risks
* Open blockers
* Next recommended action

Expected Result:

Project state fully documented.

---

# Phase 6 — Commit

Verify:

* Validation passed
* Documentation updated

Commit:

* Migration unit changes
* Documentation updates

Expected Result:

Stable migration checkpoint.

---

# Phase 7 — Session Closure

Produce:

# Session Closure Report

Include:

* Current migration phase
* Current migration unit
* Completed work
* Validation summary
* Regression summary
* Open risks
* Open blockers
* Recommended next action

Update:

* docs/SESSION_HANDOFF.md

Expected Result:

Next session can resume immediately.

---

# Migration Execution Order

Follow:

docs/MIGRATION_EXECUTION_ROADMAP.md

Current approved order:

1. Path Management Foundation
2. Configuration Centralization
3. Excel Operations Consolidation
4. File Operations Consolidation
5. Progress Tracking Consolidation
6. Color Management Consolidation
7. Shared Utility Consolidation
8. Core Processing Logic Migration

Do not skip units unless explicitly documented.

---

# Mandatory Rules

Always:

* Preserve backward compatibility
* Validate after every migration unit
* Update status documents after every migration unit
* Keep commits small and reversible
* Maintain baseline parity

Never:

* Repeat completed analysis phases
* Migrate multiple units simultaneously
* Mix refactoring with migration
* Skip validation
* Skip documentation updates

---

# Recovery Procedure

If migration validation fails:

1. Stop implementation.
2. Identify failing migration unit.
3. Revert the migration unit.
4. Restore last validated state.
5. Re-run validation.
6. Document failure.
7. Update SESSION_HANDOFF.md.
8. Re-plan the migration unit before retrying.

Expected Result:

Repository returns to a known-good state.

---

# Migration Completion

Migration is complete when:

* All migration units are completed.
* All validations pass.
* No critical regressions remain.
* Baseline parity is maintained.
* Final migration validation succeeds.

Then update:

* MIGRATION_STATUS.md
* SESSION_HANDOFF.md

Mark project status as:

Migration Complete.
