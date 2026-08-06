import pandas as pd
import sys
import os

def validate(path: str):
    """
    Validates a processed CSV dataset against schema standards:
    1. Checks for required columns.
    2. Validates numerical data types.
    3. Enforces a minimum row count threshold.
    4. Ensures no columns are entirely null.
    """
    print(f"🔍 Starting Data Validation on: {path}\n")

    # Ensure file exists before reading
    if not os.path.exists(path):
        print(f"❌ ERROR: File not found at path: '{path}'")
        sys.exit(1)

    try:
        df = pd.read_csv(path)
    except Exception as e:
        print(f"❌ ERROR: Failed to parse CSV file: {str(e)}")
        sys.exit(1)

    errors = []

    # -------------------------------------------------
    # Check 1: Required Columns
    # -------------------------------------------------
    required = ["customer_id", "order_id", "amount", "date", "segment"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        errors.append(f"Missing required column(s): {missing}")
    else:
        print("PASS: Required columns present (" + ", ".join(required) + ")")

    # -------------------------------------------------
    # Check 2: Data Types (Numeric Check)
    # -------------------------------------------------
    if "amount" in df.columns:
        if not pd.api.types.is_numeric_dtype(df["amount"]):
            errors.append("'amount' column is not numeric")
        else:
            print("PASS: 'amount' column is numeric")

    # -------------------------------------------------
    # Check 3: Minimum Row Count
    # -------------------------------------------------
    min_rows = 100
    if len(df) < min_rows:
        errors.append(f"Row count ({len(df):,}) is below required minimum threshold ({min_rows:,})")
    else:
        print(f"PASS: Row count ({len(df):,}) meets minimum threshold (>= {min_rows:,})")

    # -------------------------------------------------
    # Check 4: Fully Null Columns
    # -------------------------------------------------
    null_cols = [c for c in df.columns if df[c].isnull().all()]
    if null_cols:
        errors.append(f"Fully null column(s) detected: {null_cols}")
    else:
        print("PASS: No fully null columns found")

    # -------------------------------------------------
    # Exit Status Evaluation
    # -------------------------------------------------
    print("\n" + "=" * 50)
    if errors:
        print("🚨 VALIDATION FAILED WITH THE FOLLOWING ERROR(S):")
        for err in errors:
            print(f"  • ERROR: {err}")
        print("=" * 50 + "\n")
        # Non-zero exit code stops CI/CD pipeline step and fails the job
        sys.exit(1)
    else:
        print("✅ ALL CHECKS PASSED SUCCESSFULLY")
        print("=" * 50 + "\n")
        sys.exit(0)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python validate_data.py <path_to_csv>")
        sys.exit(1)

    validate(sys.argv[1])