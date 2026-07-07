# Next Session Prompt

You are continuing Migration 2 in the repository at:
`E:\Luxbaz\All Codes\Projects\product-import-pipeline`

## Project Context

Migration 2 standardizes repository structure and asset organization without changing business logic. The canonical data, runtime, and asset layout is now established, the shared registry layer is active, and the project is in cleanup and validation prep.

## Migration Objectives

- Keep source code separate from runtime artifacts.
- Keep data in canonical `data/` subfolders.
- Keep runtime output in canonical `runtime/` subfolders.
- Keep reusable templates and help assets in `assets/`.
- Preserve compatibility until validation proves legacy paths are safe to retire.

## Current Phase

Phase 6 - Legacy Cleanup and Consolidation in progress.

## Current Status

- Phase 0 complete.
- Phase 1 complete.
- Phase 2 complete.
- Phase 3 complete.
- Phase 4 complete.
- Phase 5 complete.
- Phase 6 in progress.
- Phase 7 pending.
- Phase 8 pending.

## Completed Work

- Shared registries implemented and wired into the main consumers.
- Shared mappings moved to `data/mappings/`.
- Pipeline spreadsheets moved to `data/inputs/`, `data/intermediate/`, and `data/outputs/`.
- Legacy color mapping archived in `data/archives/`.
- Runtime artifacts moved to `runtime/state/`, `runtime/cache/`, `runtime/logs/`, and `runtime/reports/`.
- Reusable templates moved to `assets/templates/`.
- Help assets moved to `assets/help/import_builder/`.
- Source-tree duplicates retired after verification.
- Generated caches and empty migration debris directories removed.
- Smoke tests for the migrated entry points passed.
- The dashboard generator regression that blocked default output generation was fixed.
- Alternate-working-directory regression checks passed.

## Pending Work

- Sweep stale docs and scripts for retired path references.
- Review whether remaining compatibility readers can be retired after validation.
- Review `data_standardization/` for final placement.
- Decide whether `scrapers/Old/` should remain as an archive.
- Decide whether historical `image_processing/downloaded_images/` sessions need archiving.

## Open Decisions

- Whether to keep compatibility readers after the final compatibility sweep.
- Whether to fold `data_standardization/` into `data/reference/`.
- Whether to keep `scrapers/Old/` as archive-only code.
- Whether to preserve or relocate historical image download sessions.
- Which stale docs should be rewritten versus left historical.

## Known Risks

- Stale documentation can still reference retired paths.
- Legacy scripts may still assume module-local locations.
- Compatibility fallbacks may hide missed migration coverage.
- Historical sessions under `image_processing/downloaded_images/` may be mistaken for canonical data.
- Future runs can recreate caches unless ignored.

## Mandatory Documents To Review

- `docs/migration2/MIGRATION2_STATUS.md`
- `docs/migration2/MIGRATION2_ROADMAP.md`
- `docs/migration2/MIGRATION2_PHASE2_LAYOUT_MAP.md`
- `docs/migration2/MIGRATION2_DECISION_LOG.md`
- `docs/migration2/MIGRATION2_CONTINUATION_HANDOFF.md`
- `docs/migration2/SESSION_HANDOFF.md`

## Files Modified During Previous Session

- `docs/migration2/MIGRATION2_STATUS.md`
- `docs/migration2/MIGRATION2_ROADMAP.md`
- `docs/migration2/MIGRATION2_PHASE2_LAYOUT_MAP.md`
- `docs/migration2/MIGRATION2_CONTINUATION_HANDOFF.md`
- `docs/migration2/MIGRATION2_DECISION_LOG.md`
- `docs/migration2/SESSION_HANDOFF.md`
- `docs/migration2/NEXT_SESSION_PROMPT.md`

## Validation Status

- Passed: syntax parsing of the edited Python files.
- Passed: filesystem verification for canonical `data/`, `runtime/`, `assets/`, and `data/archives/` locations.
- Passed: removal verification for retired source-tree duplicates and empty migration debris directories.
- Passed: smoke tests for `product_extraction.main`, `DashboardGenerator`, `product_extraction.web_panel_interactive`, `import_builder.web_panel_v12`, and `image_processing.menu`.
- Passed: regression checks from an alternate working directory.

## Next Recommended Task

Sweep stale docs and scripts for retired path references, then review whether any remaining compatibility readers can be retired.

## Stop Conditions

- Stop if a smoke test fails and a path regression must be diagnosed.
- Stop if a hidden consumer is found that still depends on a retired path and the minimal safe fallback is unclear.
- Stop if a doc claim cannot be reconciled with the actual repository state.
- Stop if the next move would change business logic instead of repository layout.

## Migration Rules

- Do not change business logic.
- Do not change algorithm behavior.
- Do not delete legacy files unless the new location is verified.
- Prefer small, reviewable moves.
- Keep the repository functional after every step.
- Preserve compatibility until validation is complete.

## Short Prompt For The Next Model

Continue Migration 2 from the current repository state. Review the mandatory docs above, then sweep stale docs for retired path references and review whether any remaining compatibility readers can be retired. If a hidden legacy consumer still depends on a retired path, preserve the smallest safe fallback needed to keep the repository working.
