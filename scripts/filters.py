import streamlit as st
import pandas as pd
import plotly.express as px


# ======================================================
# PAGE CONFIG
# ======================================================

st.set_page_config(
    page_title="Remote Work Blocker Dashboard",
    layout="wide"
)


st.title("Remote Work Blocker Analytics Dashboard")


# ======================================================
# LOAD DATA WITH CACHE
# ======================================================

@st.cache_data
def load_data(file):

    df = pd.read_csv(file)

    return df



# ======================================================
# UPLOAD DATA
# ======================================================


uploaded_file = st.file_uploader(
    "Upload Blocker CSV Dataset",
    type=["csv"]
)


if uploaded_file is None:

    st.info(
        "Upload normalized_blocker.csv to continue"
    )

    st.stop()



df = load_data(uploaded_file)



# ======================================================
# DATA VALIDATION
# ======================================================


required_columns = [

    "blocker_id",
    "date_logged",
    "category",
    "resolution_time_days",
    "status",
    "team_id"

]


missing = [

    col for col in required_columns
    if col not in df.columns

]


if missing:

    st.error(
        f"Missing columns: {missing}"
    )

    st.stop()



# ======================================================
# DATA CLEANING
# ======================================================


df["date_logged"] = pd.to_datetime(
    df["date_logged"]
)


df["resolution_time_days"] = pd.to_numeric(
    df["resolution_time_days"],
    errors="coerce"
)



# Fill missing resolution times

df["resolution_time_days"] = (
    df["resolution_time_days"]
    .fillna(
        df["resolution_time_days"].median()
    )
)



# ======================================================
# SIDEBAR FILTERS
# ======================================================


st.sidebar.header(
    "Filters"
)



# ------------------------------------------------------
# RESET BUTTON
# ------------------------------------------------------


if st.sidebar.button(
    "Reset Filters"
):

    st.rerun()



# ======================================================
# WIDGET 1
# DATE RANGE PICKER
# ======================================================


date_range = st.sidebar.date_input(

    "Select Date Range",

    value=(

        df["date_logged"].min(),

        df["date_logged"].max()

    )

)



# ======================================================
# WIDGET 2
# MULTI SELECT
# ======================================================


categories = (

    df["category"]
    .dropna()
    .unique()
    .tolist()

)


selected_categories = st.sidebar.multiselect(

    "Select Blocker Categories",

    options=categories,

    default=categories

)



# ======================================================
# WIDGET 3
# SLIDER
# ======================================================


min_resolution = int(
    df["resolution_time_days"].min()
)


max_resolution = int(
    df["resolution_time_days"].max()
)



resolution_range = st.sidebar.slider(

    "Resolution Time (Days)",

    min_value=min_resolution,

    max_value=max_resolution,

    value=(

        min_resolution,

        max_resolution

    )

)



# ======================================================
# WIDGET 4
# RADIO BUTTON
# ======================================================


status_options = [

    "All"

] + df["status"].unique().tolist()



selected_status = st.sidebar.radio(

    "Ticket Status",

    status_options

)



# ======================================================
# APPLY FILTERS
# ======================================================


filtered_df = df.copy()



# Date filter

filtered_df = filtered_df[

    (filtered_df["date_logged"].dt.date >= date_range[0])

    &

    (filtered_df["date_logged"].dt.date <= date_range[1])

]



# Category filter

filtered_df = filtered_df[

    filtered_df["category"]
    .isin(selected_categories)

]



# Resolution filter

filtered_df = filtered_df[

    (filtered_df["resolution_time_days"]
     >= resolution_range[0])

    &

    (filtered_df["resolution_time_days"]
     <= resolution_range[1])

]



# Status filter

if selected_status != "All":

    filtered_df = filtered_df[

        filtered_df["status"]
        ==
        selected_status

    ]



# ======================================================
# EMPTY DATA HANDLING
# ======================================================


if len(filtered_df) == 0:

    st.warning(
        "No data matches the current filters. "
        "Try broadening your selection."
    )

    st.stop()



# ======================================================
# FILTER SUMMARY
# ======================================================


st.write(

    f"Showing **{len(filtered_df):,}** "
    f"of **{len(df):,}** records"

)



st.dataframe(

    filtered_df.head(20),

    use_container_width=True

)



# ======================================================
# KPI METRICS
# ======================================================


total_blockers = len(filtered_df)


resolved = (

    filtered_df["status"]
    .str.lower()
    .eq("resolved")
    .sum()

)


resolution_rate = (

    resolved /
    total_blockers *
    100

)


avg_resolution = (

    filtered_df["resolution_time_days"]
    .mean()

)


teams = (

    filtered_df["team_id"]
    .nunique()

)



external_dependency = (

    filtered_df["is_external_dependency"]
    .astype(str)
    .eq("True")
    .mean()
    *
    100

)



c1,c2,c3,c4,c5 = st.columns(5)



c1.metric(
    "Total Blockers",
    total_blockers
)


c2.metric(
    "Resolved",
    resolved
)


c3.metric(
    "Resolution Rate",
    f"{resolution_rate:.1f}%"
)


c4.metric(
    "Avg Resolution Days",
    f"{avg_resolution:.2f}"
)


c5.metric(
    "Teams Impacted",
    teams
)



# ======================================================
# CHART 1
# LINE CHART
# ======================================================


st.subheader(
    "Blocker Trend"
)



trend = (

    filtered_df

    .groupby(
        filtered_df["date_logged"]
        .dt.date
    )

    ["blocker_id"]

    .count()

    .reset_index()

)



trend.columns = [

    "date",

    "count"

]



fig1 = px.line(

    trend,

    x="date",

    y="count",

    markers=True

)



st.plotly_chart(

    fig1,

    use_container_width=True

)



# ======================================================
# CHART 2
# BAR CHART
# ======================================================


st.subheader(
    "Blockers by Category"
)



category_chart = (

    filtered_df

    .groupby("category")

    ["blocker_id"]

    .count()

    .reset_index()

)



category_chart.columns = [

    "category",

    "count"

]



fig2 = px.bar(

    category_chart,

    x="category",

    y="count"

)



st.plotly_chart(

    fig2,

    use_container_width=True

)



# ======================================================
# CHART 3
# HISTOGRAM
# ======================================================


st.subheader(
    "Resolution Time Distribution"
)



fig3 = px.histogram(

    filtered_df,

    x="resolution_time_days",

    nbins=20

)



st.plotly_chart(

    fig3,

    use_container_width=True

)