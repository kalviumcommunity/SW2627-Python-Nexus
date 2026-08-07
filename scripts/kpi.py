import streamlit as st
import pandas as pd
import plotly.express as px


# ======================================================
# PAGE CONFIGURATION
# ======================================================

st.set_page_config(
    page_title="Remote Work Blocker Dashboard",
    layout="wide"
)


st.title("Remote Work Blocker Analytics Dashboard")

st.write(
    """
    Interactive dashboard to analyze blockers,
    resolution performance, and operational issues.
    """
)


# ======================================================
# DATA LOADING WITH CACHE
# ======================================================

@st.cache_data
def load_data(uploaded_file):

    df = pd.read_csv(uploaded_file)

    return df



# ======================================================
# FILE UPLOAD
# ======================================================

uploaded_file = st.file_uploader(
    "Upload Blocker Dataset CSV",
    type=["csv"]
)


if uploaded_file is None:

    st.info(
        "Please upload normalized_blocker.csv file"
    )

    st.stop()



df = load_data(uploaded_file)



# ======================================================
# VALIDATE COLUMNS
# ======================================================


required_columns = [
    "blocker_id",
    "team_id",
    "date_logged",
    "category",
    "is_external_dependency",
    "resolution_time_days",
    "status"
]


missing_columns = [
    col for col in required_columns
    if col not in df.columns
]


if missing_columns:

    st.error(
        f"Dataset missing columns: {missing_columns}"
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


df["is_external_dependency"] = (
    df["is_external_dependency"]
    .astype(str)
)



# ======================================================
# SIDEBAR FILTERS
# ======================================================


st.sidebar.header(
    "Filters"
)



status_filter = st.sidebar.multiselect(
    "Ticket Status",
    df["status"].unique(),
    default=df["status"].unique()
)



category_filter = st.sidebar.multiselect(
    "Blocker Category",
    df["category"].unique(),
    default=df["category"].unique()
)



team_filter = st.sidebar.multiselect(
    "Team",
    df["team_id"].unique(),
    default=df["team_id"].unique()
)



dependency_filter = st.sidebar.multiselect(
    "External Dependency",
    df["is_external_dependency"].unique(),
    default=df["is_external_dependency"].unique()
)



# ======================================================
# APPLY FILTERS
# ======================================================


filtered_df = df[
    (df["status"].isin(status_filter))
    &
    (df["category"].isin(category_filter))
    &
    (df["team_id"].isin(team_filter))
    &
    (df["is_external_dependency"].isin(dependency_filter))
]



# ======================================================
# EMPTY DATA HANDLING
# ======================================================


if len(filtered_df) == 0:

    st.warning(
        "No data matches current filters. Broaden your selection."
    )

    st.stop()



# ======================================================
# KPI CALCULATIONS
# ======================================================


total_blockers = len(filtered_df)


resolved_blockers = (
    filtered_df["status"]
    .str.lower()
    .eq("resolved")
    .sum()
)


resolution_rate = (
    resolved_blockers /
    total_blockers
    *
    100
)


avg_resolution = (
    filtered_df["resolution_time_days"]
    .mean()
)



external_percentage = (
    filtered_df["is_external_dependency"]
    .eq("True")
    .mean()
    *
    100
)



# ======================================================
# KPI DISPLAY
# ======================================================


col1,col2,col3,col4,col5 = st.columns(5)



with col1:

    st.metric(
        "Total Blockers",
        f"{total_blockers:,}"
    )



with col2:

    st.metric(
        "Resolved",
        f"{resolved_blockers:,}"
    )



with col3:

    st.metric(
        "Resolution Rate",
        f"{resolution_rate:.1f}%"
    )



with col4:

    st.metric(
        "Avg Resolution Days",
        f"{avg_resolution:.2f}"
    )



with col5:

    st.metric(
        "External Dependency",
        f"{external_percentage:.1f}%"
    )



# ======================================================
# CHART 1
# LINE CHART
# ======================================================


st.subheader(
    "Blocker Trend Over Time"
)



trend = (
    filtered_df
    .groupby(
        filtered_df["date_logged"].dt.date
    )
    ["blocker_id"]
    .count()
    .reset_index()
)


trend.columns = [
    "date",
    "blockers"
]



fig1 = px.line(
    trend,
    x="date",
    y="blockers",
    markers=True,
    title="Daily Blocker Trend"
)


fig1.update_layout(
    xaxis_title="Date",
    yaxis_title="Number of Blockers"
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



category_data = (
    filtered_df
    .groupby("category")
    ["blocker_id"]
    .count()
    .reset_index()
)


category_data.columns = [
    "category",
    "count"
]



fig2 = px.bar(
    category_data,
    x="category",
    y="count",
    title="Blockers by Category"
)



fig2.update_layout(
    xaxis_title="Category",
    yaxis_title="Number of Blockers"
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
    nbins=20,
    title="Resolution Time Distribution"
)



fig3.update_layout(
    xaxis_title="Resolution Days",
    yaxis_title="Number of Tickets"
)



st.plotly_chart(
    fig3,
    use_container_width=True
)



# ======================================================
# DATA PREVIEW
# ======================================================


st.subheader(
    "Filtered Data Preview"
)


st.dataframe(
    filtered_df,
    use_container_width=True
)