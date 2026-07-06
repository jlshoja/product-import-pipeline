# Legacy Project Migration Guide

## Purpose

This repository contains a legacy project that must be understood and documented before any refactoring or migration takes place.

---

## Core Principle

Never refactor before understanding the system.

Follow this order:

Understand
↓
Document
↓
Analyze
↓
Plan
↓
Migrate

---

## Discovery Phase Rules

During the Discovery Phase:

Do NOT:

* Rename files
* Move folders
* Rewrite code
* Delete scripts
* Change architecture

Focus on:

* Understanding the system
* Discovering inputs and outputs
* Mapping dependencies
* Documenting findings

---

## Discovery Goals

Identify:

* Modules
* Responsibilities
* Input files
* Output files
* Shared resources
* Configuration files
* Hardcoded paths
* External dependencies

---

## Documentation Requirements

Keep documentation updated in:

* PROJECT_DISCOVERY.md
* ARCHITECTURE.md
* DATA_FLOW.md
* FILE_DEPENDENCIES.md
* TECHNICAL_DEBT.md
* MIGRATION_PLAN.md

Do not create duplicate reports.

Always update existing documents.

---

## Migration Rules

Migration must be:

* Incremental
* Testable
* Reversible
* Low Risk

Every migration step should be committed separately.

---

## Success Criteria

Before migration begins:

* All modules documented
* Data flow documented
* Dependencies documented
* Technical debt identified
* Future architecture designed
* Migration plan approved
