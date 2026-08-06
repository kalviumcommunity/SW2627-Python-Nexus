import streamlit as st
import pandas as pd
from pathlib import Path
from alert_config import ALERT_THRESHOLDS

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
# Sidebar Navigation
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
# OVERVIEW PAGE
# ============================================================

if page == "Overview":

    st.title("📊 Business Overview")

    # -------------------------------------------------
    # KPI Calculations
    # -------------------------------------------------

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

    total_rows = len(df)

    open_ticket_rate = round(
        (open_tickets / total_rows) * 100,
        2
    )

    closed_ticket_rate = round(
        (closed_tickets / total_rows) * 100,
        2
    )

    null_percentage = round(
        (
            df.isna().sum().sum()
            / (df.shape[0] * df.shape[1])
        ) * 100,
        2
    )

    current_metrics = {
        "open_ticket_rate": open_ticket_rate,
        "closed_ticket_rate": closed_ticket_rate,
        "null_percentage": null_percentage
    }

    # -------------------------------------------------
    # Alert System
    # -------------------------------------------------

    st.header("🚨 Dashboard Alerts")

    for key, config in ALERT_THRESHOLDS.items():

        value = current_metrics.get(key, 0)

        breached = False

        if config["direction"] == "above":
            breached = value > config["threshold"]

        elif config["direction"] == "below":
            breached = value < config["threshold"]

        if breached:

            alert = (
                f"{config['metric']} = {value:.2f}% | "
                f"Threshold = {config['threshold']}% | "
                f"{config['message']}"
            )

            if config["severity"] == "critical":
                st.error(alert)
            else:
                st.warning(alert)

    # -------------------------------------------------
    # KPI Cards
    # -------------------------------------------------

    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric(
        "Total Tickets",
        f"{total_tickets:,}"
    )

    c2.metric(
        "Open Tickets",
        f"{open_tickets:,}"
    )

    c3.metric(
        "Closed Tickets",
        f"{closed_tickets:,}"
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

    # -------------------------------------------------
    # Dataset Summary
    # -------------------------------------------------

    st.header("Dataset Summary")

    left, right = st.columns(2)

    with left:

        st.subheader("Ticket Status")

        st.dataframe(
            df["Status (Ticket)"]
            .value_counts()
            .reset_index()
            .rename(
                columns={
                    "index": "Status",
                    "Status (Ticket)": "Count"
                }
            ),
            use_container_width=True
        )

    with right:

        st.subheader("Top Programs")

        st.dataframe(
            df["Program Name"]
            .value_counts()
            .head(10)
            .reset_index()
            .rename(
                columns={
                    "index": "Program",
                    "Program Name": "Tickets"
                }
            ),
            use_container_width=True
        )

    st.divider()

    # -------------------------------------------------
    # About Metrics
    # -------------------------------------------------

    with st.expander("📖 About These Metrics"):

        st.markdown("""

### Total Tickets
Total number of support tickets.

### Open Tickets
Tickets currently waiting for resolution.

### Closed Tickets
Tickets successfully resolved.

### Programs
Number of unique academic programs.

### Project Phases
Different phases where support requests originated.

### Alert System
Alerts are generated automatically whenever KPI values cross configured thresholds.

""")
    # ============================================================
# TREND ANALYSIS
# ============================================================

elif page == "Trend Analysis":

    st.title("📈 Trend Analysis")

    # -------------------------------------------------
    # Daily Ticket Trend
    # -------------------------------------------------

    st.header("Daily Ticket Creation Trend")

    daily = (
        df.groupby(
            df["Created Time (Ticket)"].dt.date
        )
        .size()
        .reset_index(name="Tickets")
    )

    daily.columns = ["Date", "Tickets"]

    st.line_chart(
        daily.set_index("Date")
    )

    st.caption(
        "Shows the number of support tickets created each day."
    )

    st.divider()

    # -------------------------------------------------
    # Monthly Ticket Trend
    # -------------------------------------------------

    st.header("Monthly Ticket Trend")

    monthly = (
        df.groupby(
            df["Created Time (Ticket)"].dt.to_period("M")
        )
        .size()
        .reset_index(name="Tickets")
    )

    monthly["Month"] = monthly["Created Time (Ticket)"].astype(str)

    st.bar_chart(
        monthly.set_index("Month")["Tickets"]
    )

    st.caption(
        "Monthly distribution of support tickets."
    )

    st.divider()

    # -------------------------------------------------
    # Ticket Status Trend
    # -------------------------------------------------

    st.header("Ticket Status Distribution")

    status_counts = (
        df["Status (Ticket)"]
        .value_counts()
    )

    st.bar_chart(status_counts)

    st.caption(
        "Comparison of different ticket statuses."
    )

    st.divider()

    # -------------------------------------------------
    # Program Distribution
    # -------------------------------------------------

    st.header("Top 10 Programs")

    top_programs = (
        df["Program Name"]
        .value_counts()
        .head(10)
    )

    st.bar_chart(top_programs)

    st.caption(
        "Programs generating the highest number of support tickets."
    )

    st.divider()

    # -------------------------------------------------
    # Project Phase Distribution
    # -------------------------------------------------

    st.header("Project Phase Distribution")

    phase_counts = (
        df["Project Phase"]
        .value_counts()
    )

    st.bar_chart(phase_counts)

    st.caption(
        "Support tickets across different project phases."
    )

    st.divider()

    # -------------------------------------------------
    # Quick Statistics
    # -------------------------------------------------

    st.header("Quick Statistics")

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Total Days with Tickets",
            daily.shape[0]
        )

        st.metric(
            "Maximum Tickets in One Day",
            int(daily["Tickets"].max())
        )

    with col2:

        st.metric(
            "Average Tickets per Day",
            round(daily["Tickets"].mean(), 2)
        )

        st.metric(
            "Total Tickets",
            int(daily["Tickets"].sum())
        )

    st.divider()

    # -------------------------------------------------
    # Additional Notes
    # -------------------------------------------------

    with st.expander("📖 Trend Analysis Notes"):

        st.markdown("""

### Daily Trend
Displays ticket creation volume for every day.

### Monthly Trend
Summarizes workload over months.

### Ticket Status
Shows how many tickets are Open, Closed, Pending, etc.

### Program Distribution
Highlights which academic programs generate the most tickets.

### Project Phase
Shows support requests by lifecycle stage.

These visualizations help identify workload spikes, recurring issues,
and resource planning opportunities.

""")
    # ============================================================
# DATA EXPLORER
# ============================================================

elif page == "Data Explorer":

    st.title("📂 Data Explorer")

    st.header("Filter Dataset")

    # -------------------------------------------------
    # Filters
    # -------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        status = st.multiselect(
            "Ticket Status",
            sorted(df["Status (Ticket)"].dropna().unique()),
            default=sorted(df["Status (Ticket)"].dropna().unique())
        )

    with col2:

        program = st.multiselect(
            "Program Name",
            sorted(df["Program Name"].dropna().unique()),
            default=sorted(df["Program Name"].dropna().unique())
        )

    # -------------------------------------------------
    # Apply Filters
    # -------------------------------------------------

    filtered = df[
        (df["Status (Ticket)"].isin(status))
        &
        (df["Program Name"].isin(program))
    ]

    # -------------------------------------------------
    # Calculate Metrics
    # -------------------------------------------------

    total_rows = len(filtered)

    if total_rows > 0:

        open_rate = round(
            filtered["Status (Ticket)"]
            .astype(str)
            .str.contains("Open", case=False, na=False)
            .mean() * 100,
            2
        )

        closed_rate = round(
            filtered["Status (Ticket)"]
            .astype(str)
            .str.contains("Closed", case=False, na=False)
            .mean() * 100,
            2
        )

        null_percentage = round(
            (
                filtered.isna().sum().sum()
                /
                (filtered.shape[0] * filtered.shape[1])
            ) * 100,
            2
        )

    else:

        open_rate = 0
        closed_rate = 0
        null_percentage = 0

    current_metrics = {

        "open_ticket_rate": open_rate,
        "closed_ticket_rate": closed_rate,
        "null_percentage": null_percentage

    }

    # -------------------------------------------------
    # Dynamic Alerts
    # -------------------------------------------------

    st.header("🚨 Live Alerts")

    for key, config in ALERT_THRESHOLDS.items():

        value = current_metrics.get(key, 0)

        breached = False

        if config["direction"] == "above":

            breached = value > config["threshold"]

        elif config["direction"] == "below":

            breached = value < config["threshold"]

        if breached:

            alert = (
                f"{config['metric']} = {value:.2f}% | "
                f"Threshold = {config['threshold']}% | "
                f"{config['message']}"
            )

            if config["severity"] == "critical":

                st.error(alert)

            else:

                st.warning(alert)

    # -------------------------------------------------
    # Summary Metrics
    # -------------------------------------------------

    st.header("Filtered Summary")

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Filtered Tickets",
        f"{len(filtered):,}"
    )

    c2.metric(
        "Open Ticket %",
        f"{open_rate:.2f}%"
    )

    c3.metric(
        "Closed Ticket %",
        f"{closed_rate:.2f}%"
    )

    st.divider()

    # -------------------------------------------------
    # Search Box
    # -------------------------------------------------

    search = st.text_input(
        "Search Ticket ID"
    )

    if search != "":

        filtered = filtered[
            filtered["Ticket Id"]
            .astype(str)
            .str.contains(
                search,
                case=False,
                na=False
            )
        ]

    # -------------------------------------------------
    # Dataset
    # -------------------------------------------------

    st.header("Filtered Dataset")

    st.dataframe(
        filtered,
        use_container_width=True,
        height=450
    )

    # -------------------------------------------------
    # Download CSV
    # -------------------------------------------------

    csv = filtered.to_csv(index=False).encode("utf-8")

    st.download_button(

        label="📥 Download Filtered Data",

        data=csv,

        file_name="filtered_support_tickets.csv",

        mime="text/csv"

    )

    st.divider()

    # -------------------------------------------------
    # Dataset Statistics
    # -------------------------------------------------

    with st.expander("Dataset Statistics"):

        st.write("Rows:", filtered.shape[0])

        st.write("Columns:", filtered.shape[1])

        st.write("Missing Values")

        st.write(filtered.isnull().sum())

        st.write("Summary Statistics")

        st.dataframe(
            filtered.describe(include="all"),
            use_container_width=True
        )

    # -------------------------------------------------
    # Footer
    # -------------------------------------------------

    st.caption(
        "Support Ticket Analytics Dashboard | Built with Streamlit"
    )