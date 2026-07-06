
# Migration Bootstrap Guide

## Purpose

This guide is used exactly once.

Use this guide when:

- Starting migration execution for the first time.
- Opening the project in a completely new AI.
- MIGRATION\_STATUS.md does not yet exist.
- Project status is not yet centralized.

After this guide is completed, switch permanently to:

docs/MIGRATION\_OPERATIONAL\_GUIDE.md

---

# Step 0 — Create Migration Branch

Perform manually:

```
git checkout -b migration-phase-1

```

Verify:

```
git status

```

Expected:

```
nothing to commit, working tree clean

```

---

# Step 1 — Bootstrap Analysis

Provide the following prompt to the AI:

```
# Migration Bootstrap

This repository has already completed:

- Discovery
- Architecture Analysis
- Data Flow Analysis
- Dependency Analysis
- Technical Debt Analysis
- Migration Planning
- Migration Readiness
- Final Audit
- Baseline Creation

Read:

Core Documents

- README.md
- CLAUDE.md
- docs/DOCUMENTATION_MAP.md
- docs/SESSION_HANDOFF.md

Analysis Documents

- docs/PROJECT_DISCOVERY.md
- docs/ARCHITECTURE.md
- docs/PIPELINE_INTEGRATION.md
- docs/DATA_FLOW.md
- docs/FILE_DEPENDENCIES.md
- docs/TECHNICAL_DEBT.md

Migration Documents

- docs/MIGRATION_PLAN.md
- docs/MIGRATION_READINESS.md
- docs/FINAL_AUDIT.md
- docs/CONFIG_INVENTORY.md

Analyze the repository status.

Create:

docs/MIGRATION_STATUS.md

The document must become the authoritative source of truth for migration progress.

Produce:

1. Current migration phase
2. Completed work
3. Remaining work
4. Baseline status
5. Validation status
6. Open risks
7. Open blockers
8. Next recommended action

Do not modify code.

```

---

# Step 2 — Create MIGRATION\_STATUS.md

Perform manually.

Create:

```
docs/MIGRATION_STATUS.md

```

Paste the generated contents.

---

# Step 3 — Review Generated Status

Verify:

- Current phase is correct.
- Completed work is correct.
- Remaining work is correct.
- Baseline information exists.
- Risks are realistic.

If incorrect, fix before continuing.

---

# Step 4 — Commit Bootstrap Artifacts

Perform manually:

```
git add docs/MIGRATION_STATUS.md
git add docs/MIGRATION_BOOTSTRAP_GUIDE.md

```

Commit:

```
git commit -m "Add migration status tracking"

```

---

# Step 5 — Switch To Operational Mode

Bootstrap is now complete.

Never run Bootstrap again unless:

- MIGRATION\_STATUS.md is lost.
- Project history is corrupted.
- Migration tracking must be rebuilt.

From now on use:

docs/MIGRATION\_OPERATIONAL\_GUIDE.md