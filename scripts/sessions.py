import streamlit as st
import pandas as pd
import os


# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Remote Work Blocker Analytics",
    layout="wide"
)


st.title("Remote Work Blocker Analytics Dashboard")


# ==========================================================
# SESSION STATE INITIALIZATION
# ==========================================================

# Stores selected team from Step 1.
# This survives Streamlit reruns.
if "selected_team" not in st.session_state:
    st.session_state["selected_team"] = "All"


# Tracks workflow progress.
# Step 1 -> selection
# Step 2 -> analysis
if "workflow_step" not in st.session_state:
    st.session_state["workflow_step"] = 1


# Stores calculated analysis result.
# Prevents unnecessary recalculation.
if "analysis_result" not in st.session_state:
    st.session_state["analysis_result"] = None


# Stores selected start date filter.
if "filter_start_date" not in st.session_state:
    st.session_state["filter_start_date"] = None


# Stores whether export is ready.
if "export_ready" not in st.session_state:
    st.session_state["export_ready"] = False



# ==========================================================
# LOAD DATA
# ==========================================================


@st.cache_data
def load_data():

    file_path = "data/raw/normalized_blocker.csv"

    df = pd.read_csv(file_path)

    df["date_logged"] = pd.to_datetime(
        df["date_logged"]
    )

    return df



df = load_data()



# ==========================================================
# SIDEBAR FILTERS
# ==========================================================


st.sidebar.header("Filters")


# Date Filter

min_date = df["date_logged"].min()
max_date = df["date_logged"].max()


selected_date = st.sidebar.date_input(
    "Start Date",
    value=min_date
)


st.session_state["filter_start_date"] = selected_date



# Category Filter

categories = df["category"].unique().tolist()


selected_categories = st.sidebar.multiselect(
    "Blocker Category",
    categories,
    default=categories
)



# Status Filter

statuses = df["status"].unique().tolist()


selected_status = st.sidebar.radio(
    "Ticket Status",
    statuses
)



# ==========================================================
# FILTER DATA
# ==========================================================


filtered_df = df[
    (df["date_logged"] >= pd.Timestamp(selected_date))
    &
    (df["category"].isin(selected_categories))
    &
    (df["status"] == selected_status)
]



if len(filtered_df) == 0:

    st.warning(
        "No blockers match the selected filters."
    )

    st.stop()



st.success(
    f"Showing {len(filtered_df)} blockers"
)



# ==========================================================
# STEP 1
# ==========================================================


st.header(
    "Step 1: Select Team"
)



teams = [
    "All"
] + sorted(
    df["team_id"].unique().tolist()
)



team_choice = st.selectbox(
    "Choose Team",
    teams
)



if st.button(
    "Confirm Team"
):

    st.session_state["selected_team"] = team_choice

    st.session_state["workflow_step"] = 2

    st.success(
        "Team selection saved"
    )



# ==========================================================
# STEP 2
# ==========================================================


if st.session_state["workflow_step"] >= 2:


    st.header(
        "Step 2: Blocker Analysis"
    )


    chosen_team = st.session_state["selected_team"]


    st.write(
        f"Analysing Team: **{chosen_team}**"
    )


    # Apply team filter

    if chosen_team != "All":

        analysis_df = filtered_df[
            filtered_df["team_id"]
            ==
            chosen_team
        ]

    else:

        analysis_df = filtered_df



    # Calculate metrics

    result = {

        "Total Blockers":
            len(analysis_df),


        "Resolved":
            (
                analysis_df["status"]
                ==
                "Resolved"
            )
            .sum(),


        "Average Resolution Days":
            round(
                analysis_df[
                    "resolution_time_days"
                ]
                .mean(),
                2
            ),


        "External Dependencies":
            analysis_df[
                "is_external_dependency"
            ]
            .sum()

    }



    # Save result in session state

    st.session_state[
        "analysis_result"
    ] = result



    st.session_state[
        "export_ready"
    ] = True




# ==========================================================
# DISPLAY RESULT
# ==========================================================


if st.session_state["analysis_result"]:


    st.subheader(
        "Analysis Result"
    )


    result_df = pd.DataFrame(
        [
            st.session_state[
                "analysis_result"
            ]
        ]
    )


    st.dataframe(
        result_df,
        use_container_width=True
    )



# ==========================================================
# CHARTS
# ==========================================================


st.subheader(
    "Blocker Distribution"
)



category_count = (
    filtered_df
    .groupby("category")
    .size()
)



st.bar_chart(
    category_count
)



st.subheader(
    "Resolution Time Trend"
)



trend = (
    filtered_df
    .groupby("date_logged")
    [
        "resolution_time_days"
    ]
    .mean()
)



st.line_chart(
    trend
)



# ==========================================================
# RESET WORKFLOW
# ==========================================================


st.sidebar.divider()


if st.sidebar.button(
    "Reset Workflow"
):


    keys = [

        "selected_team",
        "workflow_step",
        "analysis_result",
        "filter_start_date",
        "export_ready"

    ]


    for key in keys:

        if key in st.session_state:

            del st.session_state[key]


    st.rerun()



# ==========================================================
# EXPORT STATUS
# ==========================================================


if st.session_state["export_ready"]:

    st.sidebar.success(
        "Analysis ready for export"
    )
