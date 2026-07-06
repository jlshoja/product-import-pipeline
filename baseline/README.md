# Baseline Dataset

## Purpose

This folder contains the baseline data used for migration validation.

Before any refactoring or migration work is performed, a representative pipeline execution is captured here.

Future migration phases must be validated against this baseline to ensure that behavior has not changed unexpectedly.

---

## Structure

baseline/

├── sample_input/
├── sample_output/
├── execution_notes.md
├── comparison_manifest.md
└── README.md

---

## sample_input

Contains representative input files used to execute the pipeline.

Example:

* archive_urls.xlsx

---

## sample_output

Contains outputs generated from the baseline execution.

Examples:

* extracted_products.xlsx
* product_details_complete.xlsx
* product.csv
* WooCommerce import CSV

---

## execution_notes.md

Documents:

* Environment
* Execution method
* Commands used
* Warnings
* Errors
* Runtime observations

---

## comparison_manifest.md

Defines validation criteria for future migrations.

Future executions should be compared against the baseline outputs documented here.

---

## Usage During Migration

Whenever a migration phase is completed:

1. Execute the pipeline.
2. Compare outputs against baseline.
3. Investigate unexpected differences.
4. Update documentation only when changes are intentional.

The baseline should remain unchanged unless a new official baseline is approved.
