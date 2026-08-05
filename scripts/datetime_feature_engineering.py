import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os



# ==========================================================
# LOAD DATA
# ==========================================================

df = pd.read_csv(
    "data/raw/slack_queries.csv"
)


print("="*70)
print("DATETIME FEATURE ENGINEERING - SLACK QUERIES")
print("="*70)


print("\nInitial Data")
print(df.head())



# ==========================================================
# TASK 1
# PARSE TIMESTAMP STRINGS
# ==========================================================


print("\nTASK 1: DATETIME PARSING")
print("-"*70)


# Original format:
# DD-MM-YYYY HH:MM


# Convert to datetime
# Adding :00 seconds because source does not contain seconds


df["Created Time (Ticket)"] = (

    pd.to_datetime(

        df["Created Time (Ticket)"],

        format="%d-%m-%Y %H:%M"

    )

)



print(
    "Datetime datatype:"
)


print(
    df["Created Time (Ticket)"].dtype
)



# Expected:
# datetime64[ns]



# ==========================================================
# TASK 2
# EXTRACT DAY AND HOUR FEATURES
# ==========================================================


print("\nTASK 2: DAY AND HOUR FEATURES")
print("-"*70)



df["day_of_week"] = (

    df["Created Time (Ticket)"]
    .dt.day_name()

)



df["hour"] = (

    df["Created Time (Ticket)"]
    .dt.hour

)



df["day_number"] = (

    df["Created Time (Ticket)"]
    .dt.day

)



print(
    df[
        [
            "Created Time (Ticket)",
            "day_of_week",
            "hour"
        ]
    ].head()
)



# Hour distribution

hourly_volume = (

    df.groupby("hour")
    .size()

)


print("\nHourly Ticket Volume")

print(hourly_volume)



# Plot hour distribution

plt.figure(figsize=(8,5))

hourly_volume.plot(
    kind="bar"
)

plt.title(
    "Ticket Creation Hour Distribution"
)

plt.xlabel(
    "Hour"
)

plt.ylabel(
    "Number of Tickets"
)

plt.tight_layout()


os.makedirs(
    "output",
    exist_ok=True
)


plt.savefig(
    "output/hour_distribution.png"
)


plt.close()



# ==========================================================
# TASK 3
# WEEK NUMBER AND RESAMPLING
# ==========================================================


print("\nTASK 3: WEEKLY ANALYSIS")
print("-"*70)



df["week_num"] = (

    df["Created Time (Ticket)"]
    .dt.isocalendar()
    .week

)



df["month"] = (

    df["Created Time (Ticket)"]
    .dt.month

)



# Set datetime index


df_ts = (

    df.set_index(
        "Created Time (Ticket)"
    )

)



weekly_tickets = (

    df_ts["Ticket Id"]
    .resample("W")
    .count()

)



print("\nWeekly Ticket Trend")

print(
    weekly_tickets
)



weekly_tickets.to_csv(

    "output/weekly_ticket_trends.csv"

)



# ==========================================================
# TASK 4
# DAYS SINCE EVENT / RECENCY
# ==========================================================


print("\nTASK 4: TICKET RECENCY")
print("-"*70)



today = pd.Timestamp.now()



# Last ticket created by student/WP

customer_last_ticket = (

    df.groupby(
        "Student or WP"
    )
    ["Created Time (Ticket)"]
    .max()

)



recency = (

    today -
    customer_last_ticket

).dt.days



print(
    "\nDays since last ticket"
)


print(
    recency
)



df["days_since_last_ticket"] = (

    today -
    df["Created Time (Ticket)"]

).dt.days



print(
    "\nRecency Statistics"
)


print(
    df[
        "days_since_last_ticket"
    ]
    .describe()

)



# Customers inactive for > 7 days

inactive_users = (

    df[
        df["days_since_last_ticket"] > 7
    ]

)



print(
    "\nInactive Tickets:"
)


print(
    inactive_users[
        [
            "Ticket Id",
            "Student or WP",
            "days_since_last_ticket"
        ]
    ]
)



# ==========================================================
# TASK 5
# DAY + HOUR AGGREGATION
# ==========================================================


print("\nTASK 5: TIME INDEXED AGGREGATION")
print("-"*70)



hourly_daily = (

    df.groupby(
        [
            "day_of_week",
            "hour"
        ]
    )
    .agg(

        ticket_count=
        (
            "Ticket Id",
            "count"
        ),

        avg_response_hour=
        (
            "hour",
            "mean"
        ),

        avg_ticket_id=
        (
            "Ticket Id",
            "count"
        )

    )

)



print(
    hourly_daily
)



# Pivot table


heatmap = pd.pivot_table(

    df,

    values="Ticket Id",

    index="hour",

    columns="day_of_week",

    aggfunc="count"

)



print("\nActivity Heatmap")

print(
    heatmap
)



heatmap.to_csv(

    "output/hourly_day_heatmap.csv"

)



# Plot heatmap

plt.figure(
    figsize=(10,6)
)


plt.imshow(
    heatmap.fillna(0)
)


plt.colorbar()



plt.title(
    "Ticket Activity Heatmap (Hour x Day)"
)



plt.xlabel(
    "Day of Week"
)



plt.ylabel(
    "Hour"
)



plt.tight_layout()



plt.savefig(

    "output/ticket_activity_heatmap.png"

)



plt.close()



# ==========================================================
# VALIDATION TESTS
# ==========================================================


print("\nVALIDATION")
print("-"*70)



print(
    "Min Date:",
    df["Created Time (Ticket)"].min()
)



print(
    "Max Date:",
    df["Created Time (Ticket)"].max()
)



print(

    "Days in Dataset:",

    (

        df["Created Time (Ticket)"].max()

        -

        df["Created Time (Ticket)"].min()

    ).days

)



print(
    "Hours with Data:",
    df["hour"].unique()
)



print(
    "Weeks:",
    df["week_num"].nunique()
)



print(
    "Minimum Recency:",
    df["days_since_last_ticket"].min()
)



print(
    "Maximum Recency:",
    df["days_since_last_ticket"].max()
)




# ==========================================================
# SAVE FINAL DATASET
# ==========================================================


df.to_csv(

    "output/slack_queries_datetime_features.csv",

    index=False

)



print("\n✓ Final dataset saved")
