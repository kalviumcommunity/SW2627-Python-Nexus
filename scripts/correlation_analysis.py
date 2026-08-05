# ==========================================================
# Correlation Analysis - Jira Velocity Dataset
# ==========================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import json
from pathlib import Path


print("=" * 70)
print("CORRELATION ANALYSIS")
print("=" * 70)


# ==========================================================
# Configuration
# ==========================================================

INPUT_FILE = "data/raw/jira_velocity.csv"

OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)


# ==========================================================
# Load Dataset
# ==========================================================

df = pd.read_csv(INPUT_FILE)

print("\nDataset Shape:")
print(df.shape)

print("\nColumns:")
print(df.columns.tolist())


# ==========================================================
# Select Numerical Features
# ==========================================================

numeric_features = [
    "committed_points",
    "completed_points",
    "velocity_completion_pct",
    "avg_cycle_time_days",
    "bugs_logged"
]


df_numeric = df[numeric_features]


print("\nNumerical Data:")
print(df_numeric.head())


# ==========================================================
# Task 1: Pearson and Spearman Correlation
# ==========================================================

print("\n" + "=" * 50)
print("TASK 1: CORRELATION MATRICES")
print("=" * 50)


# Pearson correlation
# Measures linear relationship

pearson_corr = df_numeric.corr(
    method="pearson"
)


# Spearman correlation
# Measures monotonic relationship

spearman_corr = df_numeric.corr(
    method="spearman"
)


print("\nPearson Correlation:")
print(pearson_corr)


print("\nSpearman Correlation:")
print(spearman_corr)



# Compare correlations

comparison = pd.DataFrame({
    "pearson": pearson_corr["velocity_completion_pct"],
    "spearman": spearman_corr["velocity_completion_pct"]
})


comparison.to_csv(
    OUTPUT_DIR / "correlation_comparison.csv"
)


print("\nCorrelation with velocity completion:")
print(comparison)



# ==========================================================
# Task 2: Correlation Heatmap
# ==========================================================


print("\nGenerating Heatmap...")


plt.figure(
    figsize=(10,8)
)


sns.heatmap(
    pearson_corr,
    annot=True,
    cmap="coolwarm",
    center=0
)


plt.title(
    "Jira Velocity Feature Correlation Matrix"
)


plt.tight_layout()


plt.savefig(
    OUTPUT_DIR / "correlation_heatmap.png"
)


plt.close()



# ==========================================================
# Task 3: Identify Strong Correlation Pairs
# ==========================================================


print("\n" + "=" * 50)
print("TASK 3: STRONG CORRELATIONS")
print("=" * 50)



# Convert matrix into single series

corr_flat = pearson_corr.unstack()


# Remove self correlation

strong = corr_flat[
    (corr_flat.abs() > 0.7) &
    (corr_flat != 1)
]


strong = strong.sort_values(
    ascending=False
)


print(
    strong
)



strong.to_csv(
    OUTPUT_DIR / "strong_correlations.csv"
)



# ==========================================================
# Task 4: Business Interpretation
# ==========================================================


analysis = {

    "completed_points_vs_velocity_completion_pct": {

        "correlation_meaning":
        "Higher completed points generally improve sprint completion percentage",

        "possible_reason":
        "Teams finishing committed work achieve better velocity",

        "business_action":
        "Monitor estimation accuracy and delivery capacity"

    },


    "bugs_logged_vs_avg_cycle_time_days": {

        "correlation_meaning":
        "More bugs may increase cycle time",

        "possible_reason":
        "Teams spend additional effort debugging",

        "business_action":
        "Improve testing automation and code quality"

    },


    "committed_points_vs_completed_points": {

        "correlation_meaning":
        "Strong positive relationship expected",

        "possible_reason":
        "Teams completing planned work show predictable delivery",

        "business_action":
        "Use historical velocity for sprint planning"

    }

}



with open(
    OUTPUT_DIR / "business_interpretation.json",
    "w"
) as f:

    json.dump(
        analysis,
        f,
        indent=4
    )


print(
    "\nBusiness interpretation saved."
)



# ==========================================================
# Task 5: Feature Selection Based on Correlation
# ==========================================================


print("\n" + "=" * 50)
print("TASK 5: FEATURE SELECTION")
print("=" * 50)



# Example:
# committed_points and completed_points
# may be highly correlated.

selected_features = [
    "completed_points",
    "velocity_completion_pct",
    "avg_cycle_time_days",
    "bugs_logged"
]


df_features = df_numeric[
    selected_features
]


print(
    "\nSelected Features:"
)

print(
    df_features.corr()
)



df_features.to_csv(
    OUTPUT_DIR / "selected_features.csv",
    index=False
)



# ==========================================================
# Generate Report
# ==========================================================


report = {

    "dataset":
    "jira_velocity.csv",

    "rows":
    len(df),

    "features_used":
    numeric_features,

    "correlation_method":
    [
        "Pearson",
        "Spearman"
    ],

    "strong_correlation_threshold":
    0.7,

    "feature_selection_reason":
    "Removed redundant highly correlated metrics while keeping interpretable delivery indicators"

}



with open(
    OUTPUT_DIR / "correlation_report.json",
    "w"
) as f:

    json.dump(
        report,
        f,
        indent=4
    )


print("\nCorrelation analysis completed successfully.")