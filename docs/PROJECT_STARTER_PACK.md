# PROJECT STARTER PACK

## Project Structure

```text
product-import-pipeline/

├── README.md
├── CLAUDE.md
├── .gitignore
│
├── docs/
│   ├── DOCUMENTATION_MAP.md
│   ├── PROJECT_DISCOVERY.md
│   ├── ARCHITECTURE.md
│   ├── DATA_FLOW.md
│   ├── FILE_DEPENDENCIES.md
│   ├── TECHNICAL_DEBT.md
│   ├── MIGRATION_PLAN.md
│   ├── LEGACY_PROJECT_MIGRATION_GUIDE.md
│   ├── LEGACY_PROJECT_PROMPTS.md
│   └── LEGACY_PROJECT_WORKFLOW.md
```

## README.md
Purpose: Human entry point.

## CLAUDE.md
Purpose: AI entry point.
Read order:
1. README.md
2. docs/DOCUMENTATION_MAP.md
3. docs/LEGACY_PROJECT_MIGRATION_GUIDE.md
4. docs/LEGACY_PROJECT_WORKFLOW.md
5. docs/PROJECT_DISCOVERY.md
6. docs/ARCHITECTURE.md
7. docs/DATA_FLOW.md
8. docs/FILE_DEPENDENCIES.md
9. docs/TECHNICAL_DEBT.md
10. docs/MIGRATION_PLAN.md

Rules:
- Do not rename files during discovery.
- Do not move folders during discovery.
- Do not rewrite code during discovery.
- Update existing documentation.

## DOCUMENTATION_MAP.md
Maps information to documentation files.

## PROJECT_DISCOVERY.md
Modules, responsibilities, inputs, outputs, dependencies.

## ARCHITECTURE.md
Current and future architecture.

## DATA_FLOW.md
Data movement through the pipeline.

## FILE_DEPENDENCIES.md
Who creates, reads, modifies, and consumes files.

## TECHNICAL_DEBT.md
Dead code, duplicate code, hardcoded paths, risks.

## MIGRATION_PLAN.md
Future migration and refactoring roadmap.

## LEGACY_PROJECT_MIGRATION_GUIDE.md
Guide for analyzing and modernizing the legacy system.

## LEGACY_PROJECT_PROMPTS.md
Prompt library.

## LEGACY_PROJECT_WORKFLOW.md
Execution order.

# Discovery Workflow

1. Read documentation
2. Discover modules
3. Discover inputs/outputs
4. Discover file dependencies
5. Analyze hardcoded paths
6. Analyze architecture
7. Analyze data flow
8. Analyze technical debt
9. Design future architecture
10. Create migration plan

# Initial Claude Prompt

Analyze the repository.
Do not modify code.
Do not rename files.
Do not move folders.

Read all documentation files first.
Summarize your understanding.
Then update existing documentation only.

# Git Workflow

Daily:

```bash
git pull
```

After each task:

```bash
git add .
git commit -m "Describe changes"
git push
```

# Discovery Exit Criteria

- All modules identified
- Inputs/outputs documented
- File dependencies documented
- Data flow documented
- Technical debt documented
- Migration plan created
