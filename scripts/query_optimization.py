"""
Remote Work Blocker SQL Query Optimization

Optimization techniques demonstrated:

1. Replace SELECT *
   with explicit columns

2. Apply filtering before JOIN operations

3. Replace nested queries with CTEs

Dataset:
normalized_blockers.csv

Business Goal:
Optimize analytical queries used for
remote work blocker dashboards.
"""


import pandas as pd
import sqlite3
import time
import os


# ==========================================================
# Setup
# ==========================================================

os.makedirs("output", exist_ok=True)


# ==========================================================
# Load Dataset
# ==========================================================

blockers = pd.read_csv(
    "data/raw/normalized_blocker.csv"
)


# Create team table
teams = pd.DataFrame({
    "team_id": [
        "TEAM-ALPHA",
        "TEAM-BETA",
        "TEAM-GAMMA"
    ],
    "team_name":[
        "Backend Core",
        "Frontend Web",
        "DevOps Infra"
    ],
    "team_type":[
        "Engineering",
        "Engineering",
        "Infrastructure"
    ]
})


# Create category table

categories = pd.DataFrame({
    "category":[
        "Environment & Access",
        "CI/CD & Pipeline",
        "Cross-Team Dependency",
        "PTO / Outage",
        "Process & Approval"
    ],

    "severity":[
        "High",
        "Medium",
        "High",
        "Low",
        "Medium"
    ]
})


# ==========================================================
# SQLite Database
# ==========================================================


conn = sqlite3.connect(":memory:")


blockers.to_sql(
    "blockers",
    conn,
    index=False
)


teams.to_sql(
    "teams",
    conn,
    index=False
)


categories.to_sql(
    "blocker_categories",
    conn,
    index=False
)



# ==========================================================
# TASK 1
# SELECT * Optimization
# ==========================================================


print("\nTASK 1")
print("="*60)



original_query = """

SELECT *
FROM blockers b
JOIN teams t
ON b.team_id = t.team_id

LIMIT 1000;

"""


optimized_query = """

SELECT

b.blocker_id,
b.team_id,
b.category,
b.resolution_time_days,
b.status,

t.team_name,
t.team_type


FROM blockers b

JOIN teams t

ON b.team_id=t.team_id

LIMIT 1000;

"""


start=time.time()

original_result=pd.read_sql(
    original_query,
    conn
)

original_time=time.time()-start



start=time.time()

optimized_result=pd.read_sql(
    optimized_query,
    conn
)

optimized_time=time.time()-start



print(
f"Original columns : {original_result.shape[1]}"
)


print(
f"Optimized columns : {optimized_result.shape[1]}"
)


print(
f"Column reduction : "
f"{((original_result.shape[1]-optimized_result.shape[1])/
original_result.shape[1])*100:.1f}%"
)


print(
f"Original time : {original_time:.6f}"
)


print(
f"Optimized time : {optimized_time:.6f}"
)



# ==========================================================
# TASK 2
# Filtering Before JOIN
# ==========================================================


print("\nTASK 2")
print("="*60)



original_join = """

SELECT

b.blocker_id,
b.category,
t.team_name

FROM blockers b

JOIN teams t

ON b.team_id=t.team_id

WHERE

b.resolution_time_days > 5

AND t.team_type='Engineering';

"""


optimized_join = """

WITH filtered_blockers AS

(

SELECT

blocker_id,
team_id,
category,
resolution_time_days

FROM blockers

WHERE resolution_time_days > 5

)


SELECT

fb.blocker_id,
fb.category,
t.team_name


FROM filtered_blockers fb


JOIN teams t

ON fb.team_id=t.team_id


WHERE t.team_type='Engineering';


"""


original_result=pd.read_sql(
    original_join,
    conn
)


optimized_result=pd.read_sql(
    optimized_join,
    conn
)


print(
"Original rows:",
len(original_result)
)


print(
"Optimized rows:",
len(optimized_result)
)


total_rows=pd.read_sql(
"SELECT COUNT(*) count FROM blockers",
conn
).iloc[0,0]


filtered_rows=pd.read_sql(
"""

SELECT COUNT(*)

FROM blockers

WHERE resolution_time_days>5

""",
conn
).iloc[0,0]


print(
f"""
Before filtering:
{total_rows} rows

After filtering:
{filtered_rows} rows

Reduction:
{(1-filtered_rows/total_rows)*100:.2f}%
"""
)




# ==========================================================
# TASK 3
# CTE Optimization
# ==========================================================


print("\nTASK 3")
print("="*60)



cte_query="""


WITH recent_blockers AS

(

-- Step 1:
-- Select only required blocker records

SELECT

blocker_id,
team_id,
category,
resolution_time_days

FROM blockers

WHERE status='Resolved'

),



team_blockers AS

(

-- Step 2:
-- Add team information


SELECT

rb.blocker_id,
rb.category,
rb.resolution_time_days,
t.team_name


FROM recent_blockers rb


JOIN teams t

ON rb.team_id=t.team_id


),



category_metrics AS

(

-- Step 3:
-- Generate dashboard metrics


SELECT


team_name,

category,

COUNT(*) AS blocker_count,

AVG(resolution_time_days)
AS avg_resolution_time


FROM team_blockers


GROUP BY

team_name,
category

)


SELECT *

FROM category_metrics

ORDER BY avg_resolution_time DESC;


"""



cte_result=pd.read_sql(
    cte_query,
    conn
)


print(cte_result)




# ==========================================================
# TASK 4
# Documentation
# ==========================================================


comparison="""


QUERY OPTIMIZATION REPORT
=========================


Technique 1:
SELECT * Removal

Before:

SELECT *

Problem:
Fetched unnecessary columns.

After:

Explicit column selection.

Benefit:

Less memory usage.
Less network transfer.



--------------------------------


Technique 2:
Filter Before JOIN


Before:

JOIN first
FILTER later


Problem:

Large intermediate datasets.


After:

CTE filters blockers first.


Benefit:

Smaller join workload.



--------------------------------


Technique 3:
CTE Structure


Before:

Nested subqueries


After:

Named CTE steps


Benefit:

Readable,
testable,
maintainable queries.



Optimization Patterns Applied:

1. Projection optimization
   -> Select required columns only


2. Predicate pushdown
   -> Apply filters early


3. Query decomposition
   -> Use CTEs


"""


print(comparison)



with open(
"output/query_comparison.txt",
"w"
) as f:

    f.write(comparison)



# ==========================================================
# TASK 5
# Follow-up Answers
# ==========================================================



answers="""


FOLLOW UP QUESTIONS
===================


1. Index Impact

An index on resolution_time_days or status
allows the database to locate matching rows
without scanning the complete table.

Tradeoff:

Indexes consume storage and slow INSERT/UPDATE
operations because the index must also be updated.



2. CTE Recalculation

Most modern databases optimize CTE execution.

Some databases inline CTEs.
Some materialize them.

Materialized CTEs avoid repeated calculations.



3. Large Dataset Optimization

Beyond query rewriting:

- Partition tables by date
- Create materialized views
- Precompute dashboard aggregates
- Use columnar storage
- Add appropriate indexes



"""


with open(
"output/follow_up_answers.txt",
"w"
) as f:

    f.write(answers)



print(
"\nQuery optimization completed successfully"
)