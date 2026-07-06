# Legacy Project Workflow

## Phase 1 - Discovery

Goal:

Understand the current system.

Tasks:

1. Repository Discovery
2. Module Discovery
3. Input/Output Discovery
4. Dependency Discovery

Deliverables:

* PROJECT_DISCOVERY.md
* DATA_FLOW.md
* FILE_DEPENDENCIES.md

---

## Phase 2 - Analysis

Goal:

Understand weaknesses and risks.

Tasks:

1. Architecture Analysis
2. Technical Debt Analysis
3. Hardcoded Path Analysis

Deliverables:

* ARCHITECTURE.md
* TECHNICAL_DEBT.md

---

## Phase 3 - Design

Goal:

Design future architecture.

Tasks:

1. Future Architecture Design
2. Migration Strategy Design

Deliverables:

* ARCHITECTURE.md
* MIGRATION_PLAN.md

---

## Phase 4 - Migration

Goal:

Move from legacy structure to new structure.

Rules:

* Small changes
* Frequent commits
* Frequent testing

Workflow:

Change
↓
Test
↓
Commit
↓
Push

---

## Git Workflow

Start:

```bash
git pull
```

After every completed task:

```bash
git add .
git commit -m "Describe changes"
git push
```

---

## Discovery Exit Criteria

The Discovery Phase is complete when:

* All modules are documented
* All inputs are documented
* All outputs are documented
* Data flow is documented
* File dependencies are documented
* Technical debt is documented

Only then move to Design and Migration phases.
