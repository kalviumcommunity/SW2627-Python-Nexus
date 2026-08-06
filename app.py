import streamlit as st
import pandas as pd
from pathlib import Path

# -------------------------------------------------
# Page Configuration
# -------------------------------------------------

st.set_page_config(
    page_title="Support Ticket Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

# -------------------------------------------------
# Load Dataset
# -------------------------------------------------

BASE_DIR = Path(__file__).parent

DATA_FILE = BASE_DIR / "data" / "raw" / "Combined_Data.xlsx"

df = pd.read_excel(
    DATA_FILE,
    sheet_name="Support Tickets"
)

# -------------------------------------------------
# Data Cleaning
# -------------------------------------------------

df["Created Time (Ticket)"] = pd.to_datetime(
    df["Created Time (Ticket)"],
    dayfirst=True,
    errors="coerce"
)

df["Ticket Closed Time"] = pd.to_datetime(
    df["Ticket Closed Time"],
    dayfirst=True,
    errors="coerce"
)

# -------------------------------------------------
# Sidebar
# -------------------------------------------------

st.sidebar.title("📊 Navigation")

page = st.sidebar.radio(
    "Select Section",
    [
        "Overview",
        "Trend Analysis",
        "Data Explorer"
    ]
)
# ============================================================
# OVERVIEW
# ============================================================

if page == "Overview":

    st.title("📊 Business Overview")

    total_tickets = len(df)

    open_tickets = (
        df["Status (Ticket)"]
        .astype(str)
        .str.contains("Open", case=False, na=False)
        .sum()
    )

    closed_tickets = (
        df["Status (Ticket)"]
        .astype(str)
        .str.contains("Closed", case=False, na=False)
        .sum()
    )

    programs = df["Program Name"].nunique()

    phases = df["Project Phase"].nunique()

    # ---------------- KPI Cards ----------------

    c1,c2,c3,c4,c5 = st.columns(5)

    c1.metric(
        "Total Tickets",
        total_tickets
    )

    c2.metric(
        "Open Tickets",
        open_tickets
    )

    c3.metric(
        "Closed Tickets",
        closed_tickets
    )

    c4.metric(
        "Programs",
        programs
    )

    c5.metric(
        "Project Phases",
        phases
    )

    st.divider()

    st.header("Dataset Summary")

    left,right = st.columns(2)

    with left:

        st.subheader("Ticket Status")

        st.write(
            df["Status (Ticket)"]
            .value_counts()
        )

    with right:

        st.subheader("Program Distribution")

        st.write(
            df["Program Name"]
            .value_counts()
            .head(10)
        )

    with st.expander("About these Metrics"):

        st.write("""
These KPIs summarize the Support Ticket dataset.

• Total Tickets → Number of support requests.

• Open Tickets → Tickets awaiting closure.

• Closed Tickets → Successfully resolved tickets.

• Programs → Unique academic programs.

• Project Phases → Different lifecycle stages.
""")

# ============================================================
# TREND ANALYSIS
# ============================================================

elif page == "Trend Analysis":

    st.title("📈 Trend Analysis")

    st.header("Ticket Creation Trend")

    daily = (
        df.groupby(
            df["Created Time (Ticket)"].dt.date
        )
        .size()
        .reset_index(name="Tickets")
    )

    st.line_chart(
        daily.set_index("Created Time (Ticket)")
    )

    st.divider()

    st.header("Project Phase Distribution")

    st.bar_chart(
        df["Project Phase"].value_counts()
    )

    with st.expander("Trend Notes"):

        st.write("""
Daily ticket creation is useful for identifying workload spikes.

Project Phase distribution highlights where most support activity occurs.
""")

# ============================================================
# DATA EXPLORER
# ============================================================

elif page == "Data Explorer":

    st.title("📂 Data Explorer")

    st.header("Filters")

    status = st.multiselect(
        "Status",
        df["Status (Ticket)"].dropna().unique(),
        default=df["Status (Ticket)"].dropna().unique()
    )

    program = st.multiselect(
        "Program",
        df["Program Name"].dropna().unique(),
        default=df["Program Name"].dropna().unique()
    )

    filtered = df[
        df["Status (Ticket)"].isin(status) &
        df["Program Name"].isin(program)
    ]

    st.subheader("Filtered Dataset")

    st.dataframe(filtered)

    st.write(f"Rows: {len(filtered)}")

    with st.expander("Dataset Information"):

        st.write(filtered.describe(include="all"))