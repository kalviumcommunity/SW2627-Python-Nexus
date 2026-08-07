import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ==========================================================
# Remote Work Blocker Analytics Dashboard
# Assignment 35 - Visualizations
# ==========================================================

OUTPUT_DIR = "output"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ==========================================================
# Company Color Palette
# ==========================================================

PALETTE = {
    "primary": "#1f77b4",      # Blue
    "secondary": "#ff7f0e",    # Orange
    "success": "#2ca02c",      # Green
    "warning": "#ffbb00",      # Yellow
    "danger": "#d62728",       # Red
    "neutral": "#7f7f7f"       # Gray
}

# ==========================================================
# Load Dataset
# ==========================================================

df = pd.read_csv("data/raw/normalized_blocker.csv")

print("=" * 70)
print("REMOTE WORK BLOCKER ANALYTICS")
print("=" * 70)

print("\nDataset Shape")
print(df.shape)

print("\nColumns")
print(df.columns.tolist())

# ==========================================================
# Data Preparation
# ==========================================================

df["date_logged"] = pd.to_datetime(
    df["date_logged"],
    errors="coerce"
)

df["resolution_time_days"] = pd.to_numeric(
    df["resolution_time_days"],
    errors="coerce"
)

df["is_external_dependency"] = (
    df["is_external_dependency"]
    .astype(bool)
)

print("\nMissing Values")
print(df.isnull().sum())

# ==========================================================
# CHART 1
# Horizontal Bar Chart
# Number of Blockers by Category
# ==========================================================

category_counts = (
    df.groupby("category")
    .size()
    .sort_values(ascending=True)
)

fig, ax = plt.subplots(figsize=(10, 6))

bars = ax.barh(
    category_counts.index,
    category_counts.values,
    color=PALETTE["primary"]
)

ax.set_title(
    "Blockers by Category",
    fontsize=15,
    fontweight="bold"
)

ax.set_xlabel(
    "Number of Blockers"
)

ax.set_ylabel(
    "Category"
)

for bar in bars:

    width = bar.get_width()

    ax.text(
        width + 0.3,
        bar.get_y() + bar.get_height() / 2,
        str(int(width)),
        va="center"
    )

highest_category = category_counts.idxmax()

highest_value = category_counts.max()

ax.annotate(
    "Highest Frequency",
    xy=(highest_value, highest_category),
    xytext=(highest_value + 3, highest_category),
    arrowprops=dict(
        arrowstyle="->",
        color="red"
    ),
    fontsize=10
)

plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "chart1_blockers_by_category.png"
    ),
    dpi=300
)

plt.close()

print("Chart 1 Generated")

# ==========================================================
# CHART 2
# Line Chart
# Daily Blockers Logged
# ==========================================================

daily_blockers = (
    df.groupby(
        df["date_logged"].dt.date
    )
    .size()
)

fig, ax = plt.subplots(figsize=(11,6))

ax.plot(
    daily_blockers.index,
    daily_blockers.values,
    marker="o",
    linewidth=2,
    color=PALETTE["secondary"],
    label="Daily Blockers"
)

ax.set_title(
    "Daily Blockers Logged",
    fontsize=15,
    fontweight="bold"
)

ax.set_xlabel("Date")

ax.set_ylabel("Number of Blockers")

ax.grid(alpha=0.3)

ax.legend()

peak_day = daily_blockers.idxmax()

peak_value = daily_blockers.max()

ax.annotate(
    "Peak Activity",
    xy=(peak_day, peak_value),
    xytext=(peak_day, peak_value + 2),
    arrowprops=dict(
        arrowstyle="->",
        color="red"
    ),
    fontsize=10
)

plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "chart2_daily_trend.png"
    ),
    dpi=300
)

plt.close()

print("Chart 2 Generated")

# ==========================================================
# CHART 3 - Resolution Time Distribution (Histogram)
# ==========================================================

plt.figure(figsize=(10, 6))

plt.hist(
    df["resolution_time_days"],
    bins=10,
    edgecolor="black",
    color=PALETTE["warning"]
)

plt.title(
    "Distribution of Resolution Time",
    fontsize=14,
    fontweight="bold"
)

plt.xlabel("Resolution Time (Days)")
plt.ylabel("Number of Blockers")
plt.grid(alpha=0.3)

avg_resolution = df["resolution_time_days"].mean()

plt.axvline(
    avg_resolution,
    color="red",
    linestyle="--",
    linewidth=2,
    label=f"Average = {avg_resolution:.2f} days"
)

plt.annotate(
    "Average Resolution Time",
    xy=(avg_resolution, plt.ylim()[1] * 0.8),
    xytext=(avg_resolution + 0.5, plt.ylim()[1] * 0.9),
    arrowprops=dict(arrowstyle="->", color="red"),
    fontsize=10
)

plt.legend()

plt.tight_layout()

plt.savefig(
    "output/chart3_resolution_distribution.png",
    dpi=300
)

plt.close()

print("Chart 3 Saved")


# ==========================================================
# CHART 4 - Blocker Composition by Source (Stacked Bar)
# ==========================================================

source_status = (
    df.groupby(["source_type", "status"])
      .size()
      .unstack(fill_value=0)
)

ax = source_status.plot(
    kind="bar",
    stacked=True,
    figsize=(10, 6),
    color=[
        PALETTE["primary"],
        PALETTE["success"],
        PALETTE["warning"],
        PALETTE["danger"]
    ][:len(source_status.columns)]
)

plt.title(
    "Blockers by Source Type and Status",
    fontsize=14,
    fontweight="bold"
)

plt.xlabel("Source Type")
plt.ylabel("Number of Blockers")

plt.legend(title="Status")

plt.grid(axis="y", alpha=0.3)

highest_source = source_status.sum(axis=1).idxmax()
highest_value = source_status.sum(axis=1).max()

plt.annotate(
    "Highest Blocker Volume",
    xy=(list(source_status.index).index(highest_source), highest_value),
    xytext=(
        list(source_status.index).index(highest_source),
        highest_value + highest_value * 0.15
    ),
    arrowprops=dict(
        arrowstyle="->",
        color="red"
    ),
    ha="center",
    fontsize=10
)

plt.tight_layout()

plt.savefig(
    "output/chart4_source_composition.png",
    dpi=300
)

plt.close()

print("Chart 4 Saved")

# ==========================================================
# CHART 5 - Scatter Plot
# Correlation: Resolution Time vs External Dependency
# ==========================================================

plt.figure(figsize=(10, 6))

# Convert boolean to numeric for plotting
df["external_numeric"] = df["is_external_dependency"].astype(int)

plt.scatter(
    df["resolution_time_days"],
    df["external_numeric"],
    color=PALETTE["secondary"],
    alpha=0.7
)

plt.title(
    "Resolution Time vs External Dependency",
    fontsize=14,
    fontweight="bold"
)

plt.xlabel("Resolution Time (Days)")
plt.ylabel("External Dependency (0 = No, 1 = Yes)")

plt.grid(alpha=0.3)

# Trend line
z = np.polyfit(
    df["resolution_time_days"],
    df["external_numeric"],
    1
)

p = np.poly1d(z)

plt.plot(
    df["resolution_time_days"],
    p(df["resolution_time_days"]),
    color="red",
    linewidth=2,
    label="Trend Line"
)

# Highlight longest blocker
longest_idx = df["resolution_time_days"].idxmax()

plt.annotate(
    "Longest Resolution",
    xy=(
        df.loc[longest_idx, "resolution_time_days"],
        df.loc[longest_idx, "external_numeric"]
    ),
    xytext=(
        df.loc[longest_idx, "resolution_time_days"] + 1,
        df.loc[longest_idx, "external_numeric"] + 0.15
    ),
    arrowprops=dict(
        arrowstyle="->",
        color="black"
    ),
    fontsize=10
)

plt.legend()

plt.tight_layout()

plt.savefig(
    "output/chart5_resolution_vs_dependency.png",
    dpi=300
)

plt.close()

print("Chart 5 Saved")


# ==========================================================
# CREATE CHARTS README
# ==========================================================

readme_text = """
# Analysis Visualizations

## Chart 1: Blockers by Category

- Type: Bar Chart
- Business Question:
  Which blocker category occurs most frequently?
- Insight:
  Categories with the highest blocker counts require immediate attention.
- Annotation:
  Highest blocker category highlighted.

------------------------------------------------------------

## Chart 2: Daily Blocker Trend

- Type: Line Chart
- Business Question:
  How are blockers changing over time?
- Insight:
  Peaks indicate days with unusually high blocker creation.
- Annotation:
  Highest daily blocker count marked.

------------------------------------------------------------

## Chart 3: Resolution Time Distribution

- Type: Histogram
- Business Question:
  How long do blockers usually take to resolve?
- Insight:
  Most blockers are resolved within the average resolution window.
- Annotation:
  Average resolution time shown with dashed line.

------------------------------------------------------------

## Chart 4: Blockers by Source and Status

- Type: Stacked Bar Chart
- Business Question:
  Which source contributes the most blockers and what is their status?
- Insight:
  Helps compare resolved vs unresolved blockers across Jira, Slack and CSV.
- Annotation:
  Source with highest blocker volume highlighted.

------------------------------------------------------------

## Chart 5: Resolution Time vs External Dependency

- Type: Scatter Plot
- Business Question:
  Do external dependencies increase blocker resolution time?
- Insight:
  Trend line shows the relationship between dependency and resolution.
- Annotation:
  Longest resolution case highlighted.

------------------------------------------------------------

All charts were generated using:

- Matplotlib
- Pandas
- NumPy

Image Format:
PNG (300 DPI)

Output Folder:
output/
"""

with open(
    "output/CHARTS_README.md",
    "w",
    encoding="utf-8"
) as f:
    f.write(readme_text)

print("CHARTS_README.md Created")


# ==========================================================
# SUMMARY
# ==========================================================

print("\n" + "=" * 60)
print("VISUALIZATION ASSIGNMENT COMPLETED")
print("=" * 60)

print("""
Generated Files

✓ chart1_category_bar.png
✓ chart2_daily_trend.png
✓ chart3_resolution_distribution.png
✓ chart4_source_composition.png
✓ chart5_resolution_vs_dependency.png
✓ CHARTS_README.md

All charts:
✓ Proper titles
✓ Axis labels
✓ Consistent colour palette
✓ Annotations
✓ Saved as PNG (300 DPI)

Output Location:
output/
""")