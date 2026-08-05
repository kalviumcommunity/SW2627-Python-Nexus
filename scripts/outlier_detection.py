import pandas as pd
import numpy as np
from scipy import stats
import os


# ======================================================
# LOAD DATA
# ======================================================

df = pd.read_csv(
    "data/raw/slack_queries.csv"
)


print("=" * 70)
print("OUTLIER DETECTION AND HANDLING PIPELINE")
print("=" * 70)


print("\nInitial Dataset")
print(df.head())



# ======================================================
# CREATE NUMERICAL METRIC
# Ticket Resolution Time
# ======================================================

print("\nCreating Resolution Time Feature")
print("-" * 70)


# ======================================================
# DATETIME CONVERSION
# Handles invalid values like "-"
# ======================================================


df["Created Time (Ticket)"] = pd.to_datetime(
    df["Created Time (Ticket)"],
    format="%d-%m-%Y %H:%M",
    errors="coerce"
)


df["Ticket Closed Time"] = pd.to_datetime(
    df["Ticket Closed Time"],
    format="%d-%m-%Y %H:%M",
    errors="coerce"
)



print("\nInvalid datetime values")

print(
    df[
        [
            "Created Time (Ticket)",
            "Ticket Closed Time"
        ]
    ]
    .isnull()
    .sum()
)



# Remove records where duration cannot be calculated

before_drop = len(df)


df = df.dropna(
    subset=[
        "Created Time (Ticket)",
        "Ticket Closed Time"
    ]
)


after_drop = len(df)


print(
    "\nRows removed due to invalid dates:",
    before_drop - after_drop
)



# ======================================================
# Calculate Resolution Time
# ======================================================


df["resolution_time_hours"] = (

    (
        df["Ticket Closed Time"]
        -
        df["Created Time (Ticket)"]
    )
    .dt.total_seconds()

    /

    3600

)



print(
    "\nResolution Time Sample"
)


print(
    df[
        [
            "Ticket Id",
            "resolution_time_hours"
        ]
    ].head()
)



# ======================================================
# TASK 1
# Z-SCORE OUTLIER DETECTION
# ======================================================


print("\nTASK 1: Z-SCORE OUTLIER DETECTION")
print("-" * 70)



df["resolution_zscore"] = (

    np.abs(
        stats.zscore(
            df["resolution_time_hours"]
        )
    )

)



z_outliers = df[
    df["resolution_zscore"] > 3
]



print(
    f"Z-score outliers: {len(z_outliers)}"
)



if len(z_outliers) > 0:

    print(
        z_outliers[
            [
                "Ticket Id",
                "resolution_time_hours",
                "resolution_zscore"
            ]
        ]
    )



# ======================================================
# TASK 2
# IQR OUTLIER DETECTION
# ======================================================


print("\nTASK 2: IQR OUTLIER DETECTION")
print("-" * 70)



Q1 = df[
    "resolution_time_hours"
].quantile(
    0.25
)



Q3 = df[
    "resolution_time_hours"
].quantile(
    0.75
)



IQR = Q3 - Q1



lower_limit = Q1 - (1.5 * IQR)

upper_limit = Q3 + (1.5 * IQR)



print(
    "Q1:",
    Q1
)


print(
    "Q3:",
    Q3
)


print(
    "IQR:",
    IQR
)


print(
    "Lower boundary:",
    lower_limit
)


print(
    "Upper boundary:",
    upper_limit
)



df["is_outlier_iqr"] = (

    (df["resolution_time_hours"] < lower_limit)

    |

    (df["resolution_time_hours"] > upper_limit)

)



print(
    "IQR Outliers:",
    df["is_outlier_iqr"].sum()
)




# ======================================================
# TASK 3
# CAP OUTLIERS
# ======================================================


print("\nTASK 3: OUTLIER CAPPING")
print("-" * 70)



df["resolution_time_capped"] = (

    df["resolution_time_hours"]

    .clip(
        lower=lower_limit,
        upper=upper_limit
    )

)



print("Before Capping")

print(
    "Min:",
    df["resolution_time_hours"].min()
)


print(
    "Max:",
    df["resolution_time_hours"].max()
)



print("\nAfter Capping")

print(
    "Min:",
    df["resolution_time_capped"].min()
)


print(
    "Max:",
    df["resolution_time_capped"].max()
)




# ======================================================
# TASK 4
# FLAG OUTLIERS
# ======================================================


print("\nTASK 4: FLAG OUTLIERS")
print("-" * 70)



df["is_outlier"] = (

    df["is_outlier_iqr"]

    |

    (df["resolution_zscore"] > 3)

)



normal_records = df[
    ~df["is_outlier"]
]


anomalies = df[
    df["is_outlier"]
]



print(
    "Normal records:",
    len(normal_records)
)


print(
    "Anomalies:",
    len(anomalies)
)




# ======================================================
# TASK 5
# CLEANING LOG
# ======================================================


print("\nTASK 5: CLEANING LOG")
print("-" * 70)



cleaning_log = [

    {

        "column":
        "resolution_time_hours",


        "method":
        "IQR + Z-score",


        "action":
        "Cap extreme values and flag anomalies",


        "zscore_threshold":
        3,


        "iqr_multiplier":
        1.5,


        "threshold_lower":
        float(lower_limit),


        "threshold_upper":
        float(upper_limit),


        "affected_rows":
        int(df["is_outlier"].sum()),


        "date":
        pd.Timestamp.now()

    }

]



os.makedirs(
    "output",
    exist_ok=True
)



log_df = pd.DataFrame(
    cleaning_log
)



log_df.to_csv(
    "output/cleaning_log.csv",
    index=False
)



print(
    "Cleaning log saved:"
    " output/cleaning_log.csv"
)




# ======================================================
# SAVE FINAL DATASET
# ======================================================


df.to_csv(
    "output/outlier_cleaned_data.csv",
    index=False
)



print(
    "\nFinal cleaned dataset saved:"
    " output/outlier_cleaned_data.csv"
)



# ======================================================
# SUMMARY
# ======================================================


print("\nFINAL SUMMARY")
print("=" * 70)


print(
    "Total records processed:",
    len(df)
)


print(
    "Total anomalies detected:",
    df["is_outlier"].sum()
)


print(
    "Total normal records:",
    len(normal_records)
)
