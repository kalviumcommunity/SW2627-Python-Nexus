# Data Workflow

## Execute

python scripts/data_workflow.py

## Functions

### ingest_data()

Loads the Excel workbook into memory.

### process_data()

Performs validation, schema checks, statistics, and mandatory column checks.

### output_results()

Exports validation reports to Excel.

## Modifying for New Dataset

Replace the workbook inside data/raw and update EXPECTED_SHEETS if required.