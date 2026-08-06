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
# Sidebar Navigation & Global File Upload
# -------------------------------------------------

st.sidebar.title("📊 Navigation")

page = st.sidebar.radio(
    "Select Section",
    [
        "File Upload & Preview",
        "Overview",
        "Trend Analysis",
        "Data Explorer"
    ]
)

# ============================================================
# TASK 1, 2, 3, 4, 5: FILE UPLOAD & AUTOMATIC PREVIEW PAGE
# ============================================================

if page == "File Upload & Preview":
    st.title("📂 Dataset Upload & Preview")
    st.write("Upload a CSV or JSON file to immediately preview, validate, and summarize your data.")

    # -------------------------------------------------
    # Task 1 & Task 4: File Uploader & Error Handling
    # -------------------------------------------------
    uploaded_file = st.file_uploader("Upload your dataset", type=["csv", "json"])

    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith(".csv"):
                df_upload = pd.read_csv(uploaded_file)
            elif uploaded_file.name.endswith(".json"):
                df_upload = pd.read_json(uploaded_file)
            else:
                st.error("Unsupported file type.")
                st.stop()

            if len(df_upload) == 0:
                st.warning("Uploaded file is empty.")
                st.stop()

            # Store in session state for downstream pages
            st.session_state["uploaded_df"] = df_upload

            st.success(
                f"Loaded: {uploaded_file.name} "
                f"({len(df_upload):,} rows, {len(df_upload.columns)} columns)"
            )

        except Exception as e:
            st.error("Could not read this file. Check the format and try again.")
            st.stop()

        st.divider()

        # -------------------------------------------------
        # Task 2: Display Automatic Preview
        # -------------------------------------------------
        st.header("Dataset Preview")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Rows", f"{len(df_upload):,}")
        with col2:
            st.metric("Columns", str(len(df_upload.columns)))
        with col3:
            total_cells = df_upload.shape[0] * df_upload.shape[1]
            null_pct = (df_upload.isnull().sum().sum() / total_cells * 100) if total_cells > 0 else 0
            st.metric("Null %", f"{null_pct:.1f}%")

        st.subheader("First 10 Rows")
        st.dataframe(df_upload.head(10), use_container_width=True)

        st.subheader("Column Summary")
        summary = pd.DataFrame({
            "Column": df_upload.columns,
            "Type": df_upload.dtypes.astype(str).values,
            "Non-Null": df_upload.notnull().sum().values,
            "Null Count": df_upload.isnull().sum().values,
            "Null %": (df_upload.isnull().sum() / len(df_upload) * 100).round(1).values
        })
        st.dataframe(summary, use_container_width=True)

        st.divider()

        # -------------------------------------------------
        # Task 3: Display Basic Statistics
        # -------------------------------------------------
        st.header("Descriptive Statistics")
        st.dataframe(df_upload.describe(), use_container_width=True)

        st.divider()

        # -------------------------------------------------
        # Task 5: Downstream Usage / Quick Exploration
        # -------------------------------------------------
        st.header("Quick Exploration")
        numeric_cols = df_upload.select_dtypes(include="number").columns.tolist()
        categorical_cols = df_upload.select_dtypes(include=["object", "category"]).columns.tolist()
        all_cols = numeric_cols + categorical_cols

        if all_cols:
            selected_col = st.selectbox("Select a column to visualise", all_cols)
            st.bar_chart(df_upload[selected_col].value_counts().head(20))
        else:
            st.info("No plottable columns available.")

    else:
        st.info("Upload a CSV or JSON file to begin.")

# ============================================================
# SHARED DATA LOADING FOR DASHBOARD PAGES
# ============================================================

else:
    # Use uploaded dataset if present, otherwise load default Excel data
    if "uploaded_df" in st.session_state:
        df = st.session_state["uploaded_df"]
    else:
        BASE_DIR = Path(__file__).parent
        DATA_FILE = BASE_DIR / "data" / "raw" / "Combined_Data.xlsx"
        try:
            df = pd.read_excel(DATA_FILE, sheet_name="Support Tickets")
            if "Created Time (Ticket)" in df.columns:
                df["Created Time (Ticket)"] = pd.to_datetime(df["Created Time (Ticket)"], dayfirst=True, errors="coerce")
            if "Ticket Closed Time" in df.columns:
                df["Ticket Closed Time"] = pd.to_datetime(df["Ticket Closed Time"], dayfirst=True, errors="coerce")
        except Exception:
            st.error("Default dataset not found. Please upload a dataset on the 'File Upload & Preview' page.")
            st.stop()

    # ============================================================
    # OVERVIEW PAGE
    # ============================================================

    if page == "Overview":

        st.title("📊 Business Overview")

        # KPI Calculations
        total_tickets = len(df)
        
        status_col = "Status (Ticket)" if "Status (Ticket)" in df.columns else None
        prog_col = "Program Name" if "Program Name" in df.columns else None
        phase_col = "Project Phase" if "Project Phase" in df.columns else None

        open_tickets = (
            df[status_col].astype(str).str.contains("Open", case=False, na=False).sum()
            if status_col else 0
        )
        closed_tickets = (
            df[status_col].astype(str).str.contains("Closed", case=False, na=False).sum()
            if status_col else 0
        )
        programs = df[prog_col].nunique() if prog_col else 0
        phases = df[phase_col].nunique() if phase_col else 0

        total_rows = len(df)
        open_ticket_rate = round((open_tickets / total_rows) * 100, 2) if total_rows > 0 else 0
        closed_ticket_rate = round((closed_tickets / total_rows) * 100, 2) if total_rows > 0 else 0
        
        total_cells = df.shape[0] * df.shape[1]
        null_percentage = round((df.isna().sum().sum() / total_cells) * 100, 2) if total_cells > 0 else 0

        current_metrics = {
            "open_ticket_rate": open_ticket_rate,
            "closed_ticket_rate": closed_ticket_rate,
            "null_percentage": null_percentage
        }

        # Alert System
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

        # KPI Cards
        c1, c2, c3, c4, c5 = st.columns(5)
        c1.metric("Total Tickets", f"{total_tickets:,}")
        c2.metric("Open Tickets", f"{open_tickets:,}")
        c3.metric("Closed Tickets", f"{closed_tickets:,}")
        c4.metric("Programs", programs)
        c5.metric("Project Phases", phases)

        st.divider()

        # Dataset Summary
        st.header("Dataset Summary")
        left, right = st.columns(2)

        with left:
            st.subheader("Ticket Status")
            if status_col:
                st.dataframe(
                    df[status_col].value_counts().reset_index().rename(
                        columns={"index": "Status", status_col: "Count"}
                    ),
                    use_container_width=True
                )
            else:
                st.info("Status column not found.")

        with right:
            st.subheader("Top Programs")
            if prog_col:
                st.dataframe(
                    df[prog_col].value_counts().head(10).reset_index().rename(
                        columns={"index": "Program", prog_col: "Tickets"}
                    ),
                    use_container_width=True
                )
            else:
                st.info("Program column not found.")

        st.divider()

        with st.expander("📖 About These Metrics"):
            st.markdown("""
### Total Tickets
Total number of support tickets.
### Open / Closed Tickets
Current operational status of requests.
### Alert System
Alerts trigger automatically when KPIs cross pre-configured thresholds.
""")

    # ============================================================
    # TREND ANALYSIS PAGE
    # ============================================================

    elif page == "Trend Analysis":

        st.title("📈 Trend Analysis")

        date_col = "Created Time (Ticket)" if "Created Time (Ticket)" in df.columns else None

        if date_col and pd.api.types.is_datetime64_any_dtype(df[date_col]):
            st.header("Daily Ticket Creation Trend")
            daily = df.groupby(df[date_col].dt.date).size().reset_index(name="Tickets")
            daily.columns = ["Date", "Tickets"]
            st.line_chart(daily.set_index("Date"))

            st.divider()

            st.header("Monthly Ticket Trend")
            monthly = df.groupby(df[date_col].dt.to_period("M")).size().reset_index(name="Tickets")
            monthly["Month"] = monthly[date_col].astype(str)
            st.bar_chart(monthly.set_index("Month")["Tickets"])
            st.divider()

        # Quick Statistics
        st.header("Quick Statistics")
        st.dataframe(df.describe(), use_container_width=True)

    # ============================================================
    # DATA EXPLORER PAGE
    # ============================================================

    elif page == "Data Explorer":

        st.title("📂 Data Explorer")
        st.dataframe(df, use_container_width=True, height=450)

        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download Dataset",
            data=csv,
            file_name="dataset.csv",
            mime="text/csv"
        )