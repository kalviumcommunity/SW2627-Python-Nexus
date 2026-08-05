import pandas as pd
import numpy as np
import time
import os


# =====================================================
# LOAD JIRA VELOCITY DATA
# =====================================================

df = pd.read_csv(
    "data/raw/jira_velocity.csv"
)


print("="*70)
print("JIRA VELOCITY NUMPY VECTORIZATION")
print("="*70)


print("\nInitial Dataset")
print(df.head())



# =====================================================
# TASK 1
# MIN-MAX NORMALIZATION
# Normalize completed points
# =====================================================


print("\nTASK 1: COMPLETED POINTS NORMALIZATION")
print("-"*70)



# -------- Loop Version --------


start = time.time()


normalized_loop = []


for value in df["completed_points"]:

    normalized_loop.append(

        (
            value - df["completed_points"].min()
        )
        /
        (
            df["completed_points"].max()
            -
            df["completed_points"].min()
        )

    )


loop_time = time.time() - start




# -------- NumPy Version --------


start = time.time()


completed_array = (
    df["completed_points"].values
)



completed_normalized = (

    completed_array - completed_array.min()

) / (

    completed_array.max()
    -
    completed_array.min()

)



np_time = time.time() - start



df["completed_points_normalized"] = (
    completed_normalized
)



print(
    f"Loop Time: {loop_time:.6f}s"
)


print(
    f"NumPy Time: {np_time:.6f}s"
)


print(
    f"Speedup: {loop_time/np_time:.2f}x"
)



# =====================================================
# TASK 2
# Z-SCORE NORMALIZATION
# Average Cycle Time
# =====================================================


print("\nTASK 2: CYCLE TIME Z-SCORE")
print("-"*70)



cycle_array = (

    df["avg_cycle_time_days"]
    .values

)



cycle_zscore = (

    cycle_array - cycle_array.mean()

) / (

    cycle_array.std()

)



df["cycle_time_zscore"] = (
    cycle_zscore
)



print(
    df[
        [
            "team_name",
            "avg_cycle_time_days",
            "cycle_time_zscore"
        ]
    ].head()
)



# =====================================================
# TASK 3
# TEAM VELOCITY RANKING
# =====================================================


print("\nTASK 3: TEAM PERFORMANCE RANKING")
print("-"*70)



velocity_array = (

    df["velocity_completion_pct"]
    .values

)



# Highest velocity gets rank 1

sorted_indexes = np.argsort(
    -velocity_array
)



velocity_rank = np.empty_like(
    sorted_indexes
)



velocity_rank[
    sorted_indexes
] = np.arange(
    1,
    len(sorted_indexes)+1
)



df["velocity_rank"] = (
    velocity_rank
)



print(

    df[
        [
            "team_name",
            "sprint_name",
            "velocity_completion_pct",
            "velocity_rank"
        ]
    ]
    .sort_values(
        "velocity_rank"
    )
    .head(10)

)



# =====================================================
# TASK 4
# PERFORMANCE COMPARISON
# =====================================================


print("\nTASK 4: LOOP VS NUMPY PERFORMANCE")
print("-"*70)



# Generate million rows

large_completed_points = np.random.randint(
    10,
    100,
    size=1000000
)



large_df = pd.DataFrame(

    {
        "completed_points":
        large_completed_points
    }

)



# -------- Loop --------


start = time.time()



loop_result = []

for value in large_df["completed_points"]:

    loop_result.append(
        value * 1.1
    )



loop_time = time.time() - start




# -------- NumPy --------


start = time.time()



numpy_result = (

    large_df["completed_points"]
    .values
    *
    1.1

)



numpy_time = time.time() - start



print(
    f"Loop: {loop_time:.6f}s"
)


print(
    f"NumPy: {numpy_time:.6f}s"
)


print(
    f"Speedup: {loop_time/numpy_time:.0f}x"
)




# =====================================================
# TASK 5
# FINAL DATAFRAME VALIDATION
# =====================================================


print("\nTASK 5: FINAL DATAFRAME")
print("-"*70)



print(
    df.head()
)



print(
    "\nShape:",
    df.shape
)



print(
    "\nColumn Types:"
)


print(
    df.dtypes
)




# =====================================================
# SAVE RESULT
# =====================================================


os.makedirs(
    "output",
    exist_ok=True
)



df.to_csv(

    "output/jira_velocity_processed.csv",

    index=False

)



print(
    "\n✓ Saved:"
    " output/jira_velocity_processed.csv"
)