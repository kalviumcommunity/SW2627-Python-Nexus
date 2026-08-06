import argparse
import logging
import os
from pathlib import Path
import pandas as pd

# Task 3: Configure Logging with Timestamps
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)


def ingest(path: str) -> pd.DataFrame:
    """Ingests raw dataset from specified file path."""
    logger.info(f"Ingesting file from: {path}")
    
    file_path = Path(path)
    if not file_path.exists():
        logger.error(f"Input file not found at path: {path}")
        raise FileNotFoundError(f"Input file not found at path: {path}")

    # Read CSV data
    df = pd.read_csv(file_path)
    logger.info(f"Ingested {len(df):,} rows and {len(df.columns)} columns.")
    return df


def clean(df: pd.DataFrame) -> pd.DataFrame:
    """Cleans dataset by dropping nulls and filtering invalid numeric records."""
    logger.info("Starting data cleaning stage...")
    initial_rows = len(df)

    # Drop rows missing key identifiers or amount
    cleaned_df = df.dropna(subset=["customer_id", "amount"]).copy()

    # Convert amount to numeric and keep positive values
    cleaned_df["amount"] = pd.to_numeric(cleaned_df["amount"], errors="coerce")
    cleaned_df = cleaned_df[cleaned_df["amount"] > 0]

    logger.info(f"Cleaned dataset: {initial_rows:,} rows -> {len(cleaned_df):,} rows.")
    return cleaned_df


def aggregate(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregates revenue and order counts by segment."""
    logger.info("Aggregating summary metrics by segment...")

    # Determine order count column dynamically if available
    order_col = "order_id" if "order_id" in df.columns else "customer_id"

    agg_df = df.groupby("segment").agg(
        revenue=("amount", "sum"),
        orders=(order_col, "count")
    ).reset_index()

    logger.info(f"Aggregation completed for {len(agg_df):,} segments.")
    return agg_df


def output(cleaned_df: pd.DataFrame, agg_df: pd.DataFrame, out_dir: str) -> None:
    """Writes cleaned and aggregated datasets to output directory."""
    logger.info(f"Writing outputs to target directory: {out_dir}")

    out_path = Path(out_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    cleaned_file = out_path / "cleaned.csv"
    agg_file = out_path / "aggregated.csv"

    cleaned_df.to_csv(cleaned_file, index=False)
    agg_df.to_csv(agg_file, index=False)

    logger.info(f"Saved cleaned data to: {cleaned_file}")
    logger.info(f"Saved aggregated data to: {agg_file}")


# Task 2: Parameter Handling via argparse
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Automated Ingest-Clean-Aggregate Data Pipeline")
    parser.add_argument("--input", required=True, help="Path to input dataset CSV file")
    parser.add_argument("--output", default="output", help="Directory path to write output CSV files")
    args = parser.parse_args()

    logger.info("==========================================")
    logger.info("STARTING DATA PIPELINE EXECUTION")
    logger.info("==========================================")

    try:
        # Task 1: Complete Execution Flow
        raw_data = ingest(args.input)
        cleaned_data = clean(raw_data)
        aggregated_data = aggregate(cleaned_data)
        output(cleaned_data, aggregated_data, args.output)

        # Task 5: Output Confirmation Log Entry
        logger.info("==========================================")
        logger.info("Pipeline completed successfully.")
        logger.info("==========================================")

    except Exception as e:
        logger.error(f"Pipeline execution failed: {str(e)}", exc_info=True)
        raise e