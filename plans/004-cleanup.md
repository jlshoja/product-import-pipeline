# Plan 004: Delete dead code and reconcile documentation drift

> **Executor instructions**: Follow this plan step by step. Run every
> verification command and confirm the expected result before moving to the
> next step. If anything in the "STOP conditions" section occurs, stop and
> report — do not improvise. When done, update the status row for this plan
> in `plans/README.md`.
>
> **Drift check (run first)**: `git diff --stat c8d53b2..HEAD -- product_extraction/utils/color_manager.py product_extraction/scrapers/Old/ CLAUDE.md README.md docs/MIGRATION_STATUS.md`
> If any listed file changed since this plan was written, re-run the
> import-check greps in Step 1 before deleting anything.

## Status

- **Priority**: P2
- **Effort**: S
- **Risk**: LOW
- **Depends on**: none
- **Category**: tech-debt + docs
- **Planned at**: commit `c8d53b2`, 2026-07-13

## Why this matters

Two kinds of rot make the codebase harder to navigate safely:

1. **Dead code that greps as live.** `product_extraction/utils/color_manager.py`
   (392 lines) has zero importers — there are two *other* color managers that
   are actually used, so an editor can easily "fix" the wrong one.
   `product_extraction/scrapers/Old/spec_scraper-final.py` (1,375 lines) is an
   archived copy of the scraper, also with zero importers. Together ~1,770 dead
   lines that pollute search results and invite wrong-file edits.
2. **Contradictory docs.** The first files an agent or new contributor reads
   disagree about project state: `CLAUDE.md` and `README.md` say the migration
   is a *pending / preparation* phase, while `docs/MIGRATION_STATUS.md` says it
   is *complete* (all 8 units done). Whichever is right, the reader is misled by
   the other.

This plan deletes the confirmed-dead files and reconciles the status docs. It
changes no runtime behavior.

## Current state

**Confirmed-dead files (verified: zero Python importers at commit `c8d53b2`):**
- `product_extraction/utils/color_manager.py` — a `grep` for
  `utils.color_manager` / `utils/color_manager` across all `.py` returns matches
  only in `docs/SHARED_UTILITY_INVENTORY.md` (documentation, not code). The two
  live color managers are `product_extraction/color_manager.py` and
  `import_builder/color_manager.py`; shared color helpers now live in
  `product_extraction/common/color_utils.py`.
- `product_extraction/scrapers/Old/spec_scraper-final.py` — a `grep` for
  `spec_scraper-final`, `scrapers.Old`, `from Old`, `import Old` across all `.py`
  returns no matches. The live scraper is `product_extraction/scrapers/spec_scraper.py`.

**Note on `utils/`**: check whether `product_extraction/utils/` has an
`__init__.py` and other modules (it does — e.g. `logger.py`, another
`color_manager.py` sibling). Only `color_manager.py` inside it is dead; do NOT
delete the whole `utils/` package.

**Doc drift:**
- `CLAUDE.md` — "Current Phase: Migration Preparation Phase", lists
  "Configuration validation" and "Incremental migration execution" as *Pending*.
- `README.md:4-6` — "Current Status: Migration Preparation Phase / Phase 0
  (Migration Readiness) is complete."
- `docs/MIGRATION_STATUS.md:3-5` — "Current Phase: Migration Complete", with all
  8 units marked COMPLETE.

The `docs/MIGRATION_STATUS.md` "complete" state is corroborated by the codebase
(the `common/` shared utilities, the `standardizer/` module, and the git log
showing units 1-8 landed). So **`MIGRATION_STATUS.md` is authoritative**;
`CLAUDE.md` and `README.md` are stale.

## Commands you will need

| Purpose | Command | Expected on success |
|---------|---------|---------------------|
| Confirm no code imports the dead color manager | `grep -rn "utils.color_manager\|utils/color_manager" --include=*.py .` | no matches |
| Confirm no code imports the old scraper | `grep -rn "spec_scraper-final\|scrapers.Old\|import Old\|from Old" --include=*.py .` | no matches |
| Confirm pipeline still compiles | `python -m compileall product_extraction -q` | exit 0 |

Run from repo root.

## Scope

**In scope** (the only files you should modify/delete):
- Delete `product_extraction/utils/color_manager.py`
- Delete `product_extraction/scrapers/Old/spec_scraper-final.py` (and the now-empty `Old/` directory)
- Edit `CLAUDE.md` (status text)
- Edit `README.md` (status text)
- `plans/README.md` (status row only)

**Out of scope** (do NOT touch):
- `product_extraction/utils/__init__.py`, `product_extraction/utils/logger.py`,
  and any other file in `utils/` — only `color_manager.py` there is dead.
- `product_extraction/color_manager.py` and `import_builder/color_manager.py` —
  these are the LIVE color managers. Do not delete them.
- `product_extraction/scrapers/spec_scraper.py` — the live scraper.
- `docs/MIGRATION_STATUS.md` — it is already correct; leave it.
- `docs/SHARED_UTILITY_INVENTORY.md` — historical record; its mention of the
  deleted file is acceptable as history. Do not rewrite it.

## Git workflow

- Branch: `advisor/004-cleanup`
- Use `git rm` for deletions so they're staged correctly. Separate commit for
  deletions vs. doc edits. Short imperative messages (see `git log`).
- Do NOT push or open a PR unless the operator instructs it.

## Steps

### Step 1: Re-verify the files are dead before deleting

Run both import-check greps from the commands table. Both MUST return no matches
(the color-manager grep may match only `docs/…` markdown — that is fine, it is
not code). If either returns a `.py` match outside `scrapers/Old/` itself, STOP.

**Verify**: both greps return no `.py` matches (docs-only matches OK).

### Step 2: Delete the dead color manager

```
git rm product_extraction/utils/color_manager.py
```

**Verify**: `test ! -f product_extraction/utils/color_manager.py && echo gone` → prints `gone`.

### Step 3: Delete the archived scraper

```
git rm product_extraction/scrapers/Old/spec_scraper-final.py
```
If `product_extraction/scrapers/Old/` is now empty, remove it too (git drops
empty dirs automatically once tracked files are removed).

**Verify**: `test ! -f "product_extraction/scrapers/Old/spec_scraper-final.py" && echo gone` → prints `gone`.

### Step 4: Confirm nothing broke

```
python -m compileall product_extraction -q
```
Must exit 0 (no import errors introduced). If plan 001's tests exist, also run
`python -m pytest tests/ -v` and confirm still-green.

**Verify**: `python -m compileall product_extraction -q` → exit 0.

### Step 5: Reconcile the status docs

In `CLAUDE.md`, update the "Current Phase" section so it matches
`docs/MIGRATION_STATUS.md`. Change the phase from "Migration Preparation Phase"
to reflect completion, and move the "Pending" items to "Completed" (or remove
them if done). Keep the "Required reading" line intact. Example target for the
top of `CLAUDE.md`:
```markdown
## Current Phase
Migration Complete (all 8 shared-utility migration units landed — see docs/MIGRATION_STATUS.md)

Completed:
- Discovery
- Migration Readiness
- Configuration validation
- Incremental migration execution (Units 1–8)
```
Confirm against `docs/MIGRATION_STATUS.md` before writing — if that file lists a
different next-action, reflect it rather than declaring blanket completion.

In `README.md`, change "Current Status: Migration Preparation Phase" to
"Current Status: Migration Complete" (matching `MIGRATION_STATUS.md`), and update
the following sentence so it no longer implies work is pending.

**Verify**: `grep -in "preparation phase" CLAUDE.md README.md` → no matches.

### Step 6: Update the status row

In `plans/README.md`, change plan 004's status to `DONE`.

**Verify**: `grep "004" plans/README.md` shows `DONE`.

## Test plan

No new tests — this plan removes dead files and edits prose. Verification is:
- The two import-check greps (no live importers).
- `python -m compileall product_extraction -q` exits 0 (deletions broke nothing).
- If plan 001 exists, `python -m pytest tests/ -v` stays green.

## Done criteria

Machine-checkable. ALL must hold:

- [ ] `product_extraction/utils/color_manager.py` no longer exists
- [ ] `product_extraction/scrapers/Old/spec_scraper-final.py` no longer exists
- [ ] `product_extraction/color_manager.py` and `import_builder/color_manager.py` STILL exist (live ones untouched)
- [ ] `product_extraction/utils/logger.py` STILL exists (rest of utils/ untouched)
- [ ] `python -m compileall product_extraction -q` exits 0
- [ ] `grep -in "preparation phase" CLAUDE.md README.md` returns no matches
- [ ] No files outside the in-scope list are modified (`git status`)
- [ ] `plans/README.md` status row for 004 shows DONE

## STOP conditions

Stop and report back (do not improvise) if:

- Either import-check grep in Step 1 finds a real `.py` importer of the
  supposedly-dead files — they are not dead; do not delete.
- `python -m compileall product_extraction -q` fails after deletion (something
  imported a file you removed) — restore it and report.
- `docs/MIGRATION_STATUS.md` turns out to describe the project as NOT complete,
  or names a pending next action — then the "authoritative" doc is ambiguous;
  report the contradiction instead of guessing which to trust.

## Maintenance notes

- After this, `product_extraction/utils/` holds only live modules; if a future
  reader wonders why there were three color managers, the git history and
  `docs/SHARED_UTILITY_INVENTORY.md` explain it.
- Keep `CLAUDE.md` and `README.md` status in sync with `docs/MIGRATION_STATUS.md`
  going forward — they are the entry-point docs and drift here misleads every
  new session.
- A reviewer should confirm no `.bat` runner referenced the deleted scraper by
  path (the greps covered `.py`; a quick `grep -rn "spec_scraper-final" .` over
  all files confirms `.bat`/docs too).
