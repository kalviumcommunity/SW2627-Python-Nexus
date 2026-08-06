import pandas as pd
import logging
import argparse
import os
from datetime import datetime


# ----------------------------------------------------
# Logging Configuration
# ----------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

logger = logging.getLogger(__name__)


# ----------------------------------------------------
# Step 1: Data Ingestion
# ----------------------------------------------------

def ingest(file_path):

    logger.info(f"Starting ingestion: {file_path}")

    df = pd.read_csv(file_path)

    logger.info(f"Rows ingested: {len(df)}")

    return df



# ----------------------------------------------------
# Step 2: Data Cleaning
# ----------------------------------------------------

def clean(df):

    logger.info("Starting cleaning process")

    initial_rows = len(df)


    # Remove missing important values
    df = df.dropna(
        subset=[
            "customer_id",
            "amount",
            "segment"
        ]
    )


    # Convert amount to numeric
    df["amount"] = pd.to_numeric(
        df["amount"],
        errors="coerce"
    )


    # Remove invalid amounts
    df = df[df["amount"] > 0]


    logger.info(
        f"Cleaning completed: {initial_rows} -> {len(df)} rows"
    )


    return df



# ----------------------------------------------------
# Step 3: Aggregation
# ----------------------------------------------------

def aggregate(df):

    logger.info("Starting aggregation")


    aggregated = (
        df
        .groupby("segment")
        .agg(
            total_revenue=("amount","sum"),
            total_orders=("order_id","count"),
            avg_order_value=("amount","mean")
        )
        .reset_index()
    )


    logger.info(
        f"Aggregation completed for {len(aggregated)} segments"
    )


    return aggregated



# ----------------------------------------------------
# Step 4: Output
# ----------------------------------------------------

def save_output(cleaned, aggregated, output_dir):


    logger.info("Saving output files")


    os.makedirs(
        output_dir,
        exist_ok=True
    )


    cleaned_path = os.path.join(
        output_dir,
        "cleaned.csv"
    )


    aggregated_path = os.path.join(
        output_dir,
        "aggregated.csv"
    )


    cleaned.to_csv(
        cleaned_path,
        index=False
    )


    aggregated.to_csv(
        aggregated_path,
        index=False
    )


    logger.info(
        f"Cleaned data saved: {cleaned_path}"
    )

    logger.info(
        f"Aggregated data saved: {aggregated_path}"
    )



# ----------------------------------------------------
# Main Pipeline Runner
# ----------------------------------------------------

def run_pipeline(input_file, output_dir):

    logger.info("========== PIPELINE START ==========")


    raw_data = ingest(input_file)


    cleaned_data = clean(raw_data)


    aggregated_data = aggregate(cleaned_data)


    save_output(
        cleaned_data,
        aggregated_data,
        output_dir
    )


    logger.info(
        "Pipeline complete successfully"
    )



# ----------------------------------------------------
# CLI Arguments
# ----------------------------------------------------

if __name__ == "__main__":


    parser = argparse.ArgumentParser(
        description="Analytics Data Pipeline"
    )


    parser.add_argument(
        "--input",
        required=True,
        help="Input CSV file path"
    )


    parser.add_argument(
        "--output",
        default="output",
        help="Output directory"
    )


    args = parser.parse_args()


    run_pipeline(
        args.input,
        args.output
    )