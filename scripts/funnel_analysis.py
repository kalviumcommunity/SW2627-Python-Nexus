# ==========================================================
# Funnel Analysis - Slack Query Dataset
# ==========================================================

import pandas as pd
import matplotlib.pyplot as plt
import json
from pathlib import Path


print("=" * 70)
print("CUSTOMER SUPPORT FUNNEL ANALYSIS")
print("=" * 70)


# ==========================================================
# Configuration
# ==========================================================

INPUT_FILE = "data/raw/slack_queries.csv"

OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)



# ==========================================================
# Load Dataset
# ==========================================================

df = pd.read_csv(INPUT_FILE)


print("\nDataset Shape:")
print(df.shape)



# ==========================================================
# Data Cleaning
# ==========================================================


# Replace missing response values

df["First Response Time"] = (
    df["First Response Time"]
    .replace(
        ["#N/A", ""],
        pd.NA
    )
)



# Convert dates

date_columns = [
    "Created Time (Ticket)",
    "Ticket Closed Time",
    "First Response Time"
]


for col in date_columns:

    df[col] = pd.to_datetime(
        df[col],
        format="%d-%m-%Y %H:%M",
        errors="coerce"
    )



# ==========================================================
# Task 1: Define Funnel Stages
# ==========================================================


# Stage 1
stage1_created = len(df)



# Stage 2
# Users receiving first response

stage2_response = (
    df["First Response Time"]
    .notna()
    .sum()
)



# Stage 3
# Tickets that were actively processed

stage3_processed = (
    df[
        df["Status (Ticket)"]
        .isin(
            [
                "Closed",
                "Duplicate",
                "Deleted"
            ]
        )
    ]
    .shape[0]
)



# Stage 4
# Closed tickets

stage4_closed = (
    df[
        df["Status (Ticket)"]=="Closed"
    ]
    .shape[0]
)



# Stage 5
# Successfully resolved tickets

stage5_resolved = (
    df[
        (df["Status (Ticket)"]=="Closed")
        &
        (df["Ticket Closed Time"].notna())
    ]
    .shape[0]
)



# Stage 6
# Customers with complete lifecycle

stage6_completed = (
    df[
        (df["Status (Ticket)"]=="Closed")
        &
        (df["First Response Time"].notna())
        &
        (df["Ticket Closed Time"].notna())
    ]
    .shape[0]
)



stages = {

    "Ticket Created":
        stage1_created,

    "First Response":
        stage2_response,

    "Ticket Processed":
        stage3_processed,

    "Ticket Closed":
        stage4_closed,

    "Successfully Resolved":
        stage5_resolved,

    "Complete Lifecycle":
        stage6_completed

}



print("\nFunnel Stages")

for k,v in stages.items():

    print(k,":",v)



# ==========================================================
# Task 2: Drop-off Calculation
# ==========================================================


stage_names = list(stages.keys())
stage_values = list(stages.values())


drop_analysis = []


for i in range(len(stage_values)-1):

    before = stage_values[i]
    after = stage_values[i+1]


    lost = before-after


    drop_rate = (
        lost/before
    )*100


    completion_rate = (
        after/before
    )*100



    drop_analysis.append({

        "from_stage":
        stage_names[i],


        "to_stage":
        stage_names[i+1],


        "users_before":
        before,


        "users_after":
        after,


        "users_lost":
        lost,


        "drop_rate":
        round(drop_rate,2),


        "completion_rate":
        round(completion_rate,2)

    })



funnel_df = pd.DataFrame(
    drop_analysis
)



print("\nDrop-off Analysis")

print(funnel_df)



funnel_df.to_csv(
    OUTPUT_DIR /
    "dropoff_metrics.csv",
    index=False
)



# ==========================================================
# Find Biggest Bottleneck
# ==========================================================


biggest_drop = (
    funnel_df
    .sort_values(
        "users_lost",
        ascending=False
    )
    .iloc[0]
)


print("\nBiggest Bottleneck")

print(biggest_drop)



# ==========================================================
# Task 3: Funnel Visualization
# ==========================================================


plt.figure(
    figsize=(12,6)
)



bars = plt.bar(
    stage_names,
    stage_values
)



plt.title(
    "Customer Support Funnel"
)


plt.xlabel(
    "Funnel Stage"
)


plt.ylabel(
    "Users"
)



plt.xticks(
    rotation=45,
    ha="right"
)



# Add labels

for bar,value in zip(
    bars,
    stage_values
):

    plt.text(
        bar.get_x()+bar.get_width()/2,
        value,
        str(value),
        ha="center",
        va="bottom"
    )



plt.tight_layout()


plt.savefig(
    OUTPUT_DIR /
    "funnel_chart.png",
    dpi=150
)



plt.close()



# ==========================================================
# Task 4: Business Impact Calculation
# ==========================================================


revenue_per_customer = 100


impact=[]



for _,row in funnel_df.iterrows():

    lost=row["users_lost"]


    impact.append({

        "drop_point":
        row["from_stage"]
        +" -> "
        +row["to_stage"],


        "users_lost":
        lost,


        "business_cost":
        lost*revenue_per_customer,


        "priority":
        (
            "HIGH"
            if lost*revenue_per_customer > 1000
            else "MEDIUM"
        )

    })



impact_df=pd.DataFrame(
    impact
)



impact_df.to_csv(
    OUTPUT_DIR /
    "business_impact.csv",
    index=False
)



print("\nBusiness Impact")

print(
    impact_df
    .sort_values(
        "business_cost",
        ascending=False
    )
)



# ==========================================================
# Task 5: Recommendation Report
# ==========================================================


lost_users = biggest_drop["users_lost"]


revenue_loss = (
    lost_users*
    revenue_per_customer
)



recommendation=f"""

FUNNEL OPTIMIZATION REPORT
==========================


Critical Bottleneck:

{biggest_drop['from_stage']}
to
{biggest_drop['to_stage']}


Users Lost:
{lost_users}


Drop Rate:
{biggest_drop['drop_rate']}%


Estimated Business Impact:
${revenue_loss}



Possible Root Causes:

1. Slow response time
2. Poor communication during support process
3. Ticket complexity
4. Customers abandoning before resolution



Recommended Actions:

1. Reduce first response SLA
2. Add automated acknowledgement messages
3. Improve support workflow
4. Monitor stage conversion weekly



Success Metrics:

- Increase stage completion by 10%
- Reduce response abandonment
- Improve resolution rate


Expected Impact:

Recovering 10% of lost users:

Additional Users:
{int(lost_users*0.1)}

Additional Revenue:
${int(lost_users*0.1*100)}

"""



print(recommendation)



with open(
    OUTPUT_DIR /
    "funnel_analysis.txt",
    "w"
) as file:

    file.write(
        recommendation
    )



# ==========================================================
# Save Final Report
# ==========================================================


report={

    "dataset":
    "slack_queries.csv",


    "total_records":
    len(df),


    "biggest_bottleneck":
    biggest_drop.to_dict(),


    "revenue_per_customer":
    revenue_per_customer

}



with open(
    OUTPUT_DIR /
    "funnel_report.json",
    "w"
) as f:

    json.dump(
        report,
        f,
        indent=4,
        default=str
    )



print("\nFunnel analysis completed successfully.")