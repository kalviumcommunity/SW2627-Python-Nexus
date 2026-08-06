import pandas as pd
import plotly.express as px

from export_functions import export_analysis



# Load data

df = pd.read_csv(
    "data/raw/normalized_blocker.csv"
)



# ===============================
# Analysis
# ===============================


category_summary = (
    df.groupby("category")
    .agg(
        blockers=("blocker_id","count"),
        avg_resolution_time=(
            "resolution_time_days",
            "mean"
        )
    )
    .reset_index()
)



team_summary = (
    df.groupby("team_id")
    .size()
    .reset_index(
        name="total_blockers"
    )
)



# ===============================
# Charts
# ===============================


fig_category = px.bar(
    category_summary,
    x="category",
    y="blockers",
    title="Blockers by Category"
)


fig_team = px.bar(
    team_summary,
    x="team_id",
    y="total_blockers",
    title="Blockers by Team"
)


fig_resolution = px.histogram(
    df,
    x="resolution_time_days",
    title="Resolution Time Distribution"
)



charts = {

    "Category Analysis":
        fig_category,

    "Team Analysis":
        fig_team,

    "Resolution Time":
        fig_resolution
}



# ===============================
# Summary
# ===============================


summary = f"""

# Remote Work Blocker Summary


## Key Findings


Total blockers:

**{len(df)}**



Highest blocker category:

**{category_summary.iloc[0]['category']}**



Average resolution time:

**{df['resolution_time_days'].mean():.2f} days**



## Recommendations


1. Reduce environment access issues.

2. Improve CI/CD automation.

3. Create team dependency alerts.


"""



# Export

folder = export_analysis(
    df,
    summary,
    charts,
    "output"
)



print(
    "Report generated:",
    folder
)