import pandas as pd
import json
import os



# =====================================================
# LOAD DATASETS
# =====================================================


df_velocity = pd.read_csv(
    "data/raw/jira_velocity.csv"
)


df_blockers = pd.read_csv(
    "data/raw/normalized_blocker.csv"
)



print("="*70)
print("JOIN VALIDATION PIPELINE")
print("="*70)



# =====================================================
# TASK 1
# Explicit LEFT JOIN WITH ROW VALIDATION
# =====================================================


print("\nTASK 1: LEFT JOIN VALIDATION")
print("-"*70)



print(
    f"Velocity rows (Left): {len(df_velocity)}"
)


print(
    f"Blocker rows (Right): {len(df_blockers)}"
)



merged_df = pd.merge(

    df_velocity,

    df_blockers,

    on="team_id",

    how="left",

    suffixes=(
        "_velocity",
        "_blocker"
    )

)



print(
    f"Merged rows: {len(merged_df)}"
)


print(
    f"Row change: {len(merged_df)-len(df_velocity)}"
)



# =====================================================
# TASK 2
# DETECT UNMATCHED KEYS
# =====================================================


print("\nTASK 2: UNMATCHED KEY DETECTION")
print("-"*70)



# Teams without blockers

unmatched_teams = df_velocity[

    ~df_velocity["team_id"].isin(

        df_blockers["team_id"]

    )

]



# Blockers without velocity record

orphan_blockers = df_blockers[

    ~df_blockers["team_id"].isin(

        df_velocity["team_id"]

    )

]



print(
    "Teams without blockers:",
    len(unmatched_teams)
)



print(
    "Orphan blockers:",
    len(orphan_blockers)
)



os.makedirs(
    "output",
    exist_ok=True
)



unmatched_teams.to_csv(

    "output/unmatched_teams.csv",

    index=False

)



orphan_blockers.to_csv(

    "output/orphan_blockers.csv",

    index=False

)



# =====================================================
# TASK 3
# COMPARE JOIN TYPES
# =====================================================


print("\nTASK 3: JOIN TYPE COMPARISON")
print("-"*70)



inner_join = pd.merge(

    df_velocity,

    df_blockers,

    on="team_id",

    how="inner"

)



left_join = pd.merge(

    df_velocity,

    df_blockers,

    on="team_id",

    how="left"

)



outer_join = pd.merge(

    df_velocity,

    df_blockers,

    on="team_id",

    how="outer"

)



print(
    f"Inner Join Rows: {len(inner_join)}"
)


print(
    f"Left Join Rows: {len(left_join)}"
)


print(
    f"Outer Join Rows: {len(outer_join)}"
)




# =====================================================
# TASK 4
# DUPLICATION VALIDATION
# =====================================================


print("\nTASK 4: DUPLICATION CHECK")
print("-"*70)



print(
    "Merged Columns:"
)


print(
    merged_df.columns.tolist()
)



team_counts = merged_df[
    "team_id"
].value_counts()



print(
    "Maximum blockers per team:",
    team_counts.max()
)



print(
    "Average records per team:",
    team_counts.mean()
)




# =====================================================
# TASK 5
# JOIN DECISION REPORT
# =====================================================


print("\nTASK 5: JOIN DOCUMENTATION")
print("-"*70)



join_report = {


    "join_type":
    "left",


    "left_table":
    "jira_velocity",


    "right_table":
    "normalized_blocker",


    "join_key":
    "team_id",


    "left_rows":
    len(df_velocity),


    "right_rows":
    len(df_blockers),


    "result_rows":
    len(merged_df),


    "unmatched_left":
    len(unmatched_teams),


    "unmatched_right":
    len(orphan_blockers),


    "business_reason":

    """
    Left join selected because sprint velocity data
    is the primary business dataset.

    Every sprint/team performance record must be
    retained even if no blocker exists.

    Blocker information is optional enrichment data
    used for identifying delivery risks.
    """

}



print(
    json.dumps(
        join_report,
        indent=4
    )
)



with open(
    "output/join_report.json",
    "w"
) as file:

    json.dump(
        join_report,
        file,
        indent=4
    )




# =====================================================
# SAVE FINAL DATA
# =====================================================



merged_df.to_csv(

    "output/sprint_blocker_joined.csv",

    index=False

)



print("\nFINAL OUTPUT")
print("-"*70)

print(
    "Saved:"
)

print(
    "output/sprint_blocker_joined.csv"
)

print(
    "output/unmatched_teams.csv"
)

print(
    "output/orphan_blockers.csv"
)

print(
    "output/join_report.json"
)


print("="*70)