"""
==========================================================
Data Workflow Script
==========================================================

This script performs a complete data workflow:

1. Ingest data from an Excel workbook
2. Validate workbook structure
3. Generate statistics and schema reports
4. Save reports to the output folder

Run:
    python scripts/data_workflow.py
"""

from pathlib import Path
import pandas as pd
import numpy as np

# ==========================================================
# Configuration
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_FOLDER = BASE_DIR / "data" / "raw"
OUTPUT_FOLDER = BASE_DIR / "output"

FILE_NAME = "Combined_Data.xlsx"
FILE_PATH = DATA_FOLDER / FILE_NAME

OUTPUT_FOLDER.mkdir(exist_ok=True)

EXPECTED_SHEETS = [
    "Support Tickets",
    "Jira Issues",
    "Survey Responses"
]

MANDATORY_COLUMNS = {
    "Support Tickets": ["Ticket Id"],
    "Jira Issues": ["Key"],
    "Survey Responses": ["Response ID"]
}


# ==========================================================
# Function 1 : Ingest
# ==========================================================

def ingest_data(filepath):
    """
    Load the Excel workbook.

    Input:
        filepath : Path to Excel workbook

    Returns:
        Dictionary containing all worksheets as DataFrames.

    Raises:
        FileNotFoundError if workbook is missing.
    """

    print("=" * 70)
    print("DATA WORKFLOW")
    print("=" * 70)

    print("\nChecking dataset...")

    if not filepath.exists():
        raise FileNotFoundError(f"Dataset not found:\n{filepath}")

    print("✓ Dataset Found")

    file_size = round(filepath.stat().st_size / (1024 * 1024), 2)

    print(f"File Size : {file_size} MB")
    print(f"Extension : {filepath.suffix}")

    print("\nLoading workbook...")

    workbook = pd.read_excel(filepath, sheet_name=None)

    print("✓ Workbook Loaded Successfully")

    print("\nAvailable Sheets:")

    for sheet in workbook.keys():
        print(f" - {sheet}")

    return workbook


# ==========================================================
# Function 2 : Process
# ==========================================================

def process_data(workbook):
    """
    Process workbook and generate validation reports.

    Input:
        Dictionary of DataFrames.

    Returns:
        Dictionary containing report DataFrames.
    """

    # --------------------------------------------
    # Workbook Summary
    # --------------------------------------------

    summary = []

    for sheet, df in workbook.items():

        summary.append({

            "Sheet Name": sheet,
            "Rows": len(df),
            "Columns": len(df.columns),
            "Memory(MB)": round(
                df.memory_usage(deep=True).sum() / 1024 ** 2,
                2
            )

        })

    summary_df = pd.DataFrame(summary)

    print("\nWorkbook Summary")
    print(summary_df.to_string(index=False))

    # --------------------------------------------
    # Sheet Validation
    # --------------------------------------------

    validation = []

    for sheet in EXPECTED_SHEETS:

        validation.append({

            "Sheet": sheet,
            "Exists": sheet in workbook

        })

    sheet_validation = pd.DataFrame(validation)

    print("\nSheet Validation")
    print(sheet_validation.to_string(index=False))

    # --------------------------------------------
    # Schema Validation
    # --------------------------------------------

    schema = []

    for sheet, df in workbook.items():

        for col in df.columns:

            schema.append({

                "Sheet": sheet,
                "Column": col,
                "Data Type": str(df[col].dtype),
                "Null Count": int(df[col].isna().sum()),
                "Unique Values": int(df[col].nunique())

            })

    schema_df = pd.DataFrame(schema)

    print("\nSchema Sample")
    print(schema_df.head(20).to_string(index=False))

    # --------------------------------------------
    # Mandatory Columns
    # --------------------------------------------

    mandatory_report = []

    for sheet, columns in MANDATORY_COLUMNS.items():

        if sheet not in workbook:
            continue

        df = workbook[sheet]

        for col in columns:

            mandatory_report.append({

                "Sheet": sheet,
                "Column": col,
                "Exists": col in df.columns

            })

    mandatory_df = pd.DataFrame(mandatory_report)

    print("\nMandatory Column Validation")
    print(mandatory_df.to_string(index=False))

    # --------------------------------------------
    # Workbook Statistics
    # --------------------------------------------

    stats = []

    for sheet, df in workbook.items():

        stats.append({

            "Sheet": sheet,
            "Rows": len(df),
            "Columns": len(df.columns),
            "Missing Cells": int(df.isna().sum().sum()),
            "Duplicate Rows": int(df.duplicated().sum()),
            "Numeric Columns":
                len(df.select_dtypes(include=np.number).columns),
            "Categorical Columns":
                len(df.select_dtypes(include=["object", "string"]).columns),
            "Date Columns":
                len(df.select_dtypes(include=["datetime64[ns]"]).columns)

        })

    stats_df = pd.DataFrame(stats)

    print("\nWorkbook Statistics")
    print(stats_df.to_string(index=False))

    # --------------------------------------------
    # Overall Validation
    # --------------------------------------------

    issues = []

    for _, row in sheet_validation.iterrows():

        if not row["Exists"]:
            issues.append(f"Missing Sheet: {row['Sheet']}")

    for _, row in mandatory_df.iterrows():

        if not row["Exists"]:
            issues.append(
                f"Missing Column: {row['Column']} ({row['Sheet']})"
            )

    result = "PASS" if len(issues) == 0 else "FAIL"

    print("\nOverall Validation:", result)

    if issues:

        print("\nIssues Found:")

        for issue in issues:
            print("-", issue)

    else:

        print("No validation issues detected.")

    return {

        "summary": summary_df,
        "sheet_validation": sheet_validation,
        "schema": schema_df,
        "mandatory": mandatory_df,
        "stats": stats_df,
        "workbook": workbook

    }


# ==========================================================
# Function 3 : Output
# ==========================================================

def output_results(results, output_folder):
    """
    Save reports to Excel.

    Input:
        Dictionary returned by process_data()

    Output:
        Excel reports inside output folder.
    """

    validation_path = output_folder / "Validation_Report.xlsx"

    with pd.ExcelWriter(validation_path, engine="openpyxl") as writer:

        results["summary"].to_excel(
            writer,
            sheet_name="Workbook Summary",
            index=False
        )

        results["sheet_validation"].to_excel(
            writer,
            sheet_name="Sheet Validation",
            index=False
        )

        results["schema"].to_excel(
            writer,
            sheet_name="Schema Validation",
            index=False
        )

        results["mandatory"].to_excel(
            writer,
            sheet_name="Mandatory Columns",
            index=False
        )

        results["stats"].to_excel(
            writer,
            sheet_name="Statistics",
            index=False
        )

    results["summary"].to_excel(
        output_folder / "Workbook_Summary.xlsx",
        index=False
    )

    total_rows = results["summary"]["Rows"].sum()

    print("\n" + "=" * 70)
    print("✓ Data successfully processed")
    print(f"✓ Rows processed : {total_rows}")
    print(f"✓ Output saved to : {output_folder}")
    print("=" * 70)


# ==========================================================
# Main
# ==========================================================

if __name__ == "__main__":

    try:

        workbook = ingest_data(FILE_PATH)

        reports = process_data(workbook)

        output_results(reports, OUTPUT_FOLDER)

    except Exception as e:

        print("\nWorkflow Failed")
        print(f"Reason: {e}")