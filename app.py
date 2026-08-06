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
# Sidebar Navigation
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
# FILE UPLOAD & PREVIEW
# ============================================================

if page == "File Upload & Preview":
    st.title("📂 Dataset Upload & Preview")
    st.write("Upload a CSV or JSON file to immediately preview, validate, and summarize your data.")

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

        except Exception:
            st.error("Could not read this file. Check the format and try again.")
            st.stop()

        st.divider()

        # Dataset Preview
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

        st.header("Descriptive Statistics")
        st.dataframe(df_upload.describe(), use_container_width=True)

        st.divider()

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
# SHARED DATA LOADING & FILTER CHAIN FOR DASHBOARD PAGES
# ============================================================

else:
    # 1. Load raw DataFrame
    if "uploaded_df" in st.session_state:
        df_raw = st.session_state["uploaded_df"].copy()
    else:
        BASE_DIR = Path(__file__).parent
        DATA_FILE = BASE_DIR / "data" / "raw" / "Combined_Data.xlsx"
        try:
            df_raw = pd.read_excel(DATA_FILE, sheet_name="Support Tickets")
        except Exception:
            st.error("Default dataset not found. Please upload a dataset on the 'File Upload & Preview' page.")
            st.stop()

    # Preprocess Datetime columns if available
    date_col = "Created Time (Ticket)" if "Created Time (Ticket)" in df_raw.columns else None
    if date_col:
        df_raw[date_col] = pd.to_datetime(df_raw[date_col], dayfirst=True, errors="coerce")

    # -------------------------------------------------
    # Task 5: Implement Filter Reset Logic
    # -------------------------------------------------
    if st.sidebar.button("Reset Filters"):
        # Clear filter keys from session state to restore widget default values
        for key in ["filter_date_range", "filter_segments", "filter_numeric_range"]:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()

    st.sidebar.header("🔍 Interactive Filters")

    # -------------------------------------------------
    # Task 1 & Task 3: Interactive Widgets with Meaningful Defaults
    # -------------------------------------------------
    
    # Widget 1: Date Range Picker
    if date_col and not df_raw[date_col].dropna().empty:
        min_date = df_raw[date_col].min().date()
        max_date = df_raw[date_col].max().date()
        date_range = st.sidebar.date_input(
            "Date Range",
            value=st.session_state.get("filter_date_range", (min_date, max_date)),
            min_value=min_date,
            max_value=max_date,
            key="filter_date_range"
        )
    else:
        date_range = None

    # Widget 2: Multi-select for Segments / Programs
    seg_col = "Program Name" if "Program Name" in df_raw.columns else df_raw.select_dtypes(include=["object", "category"]).columns[0] if len(df_raw.select_dtypes(include=["object", "category"]).columns) > 0 else None
    if seg_col:
        all_segments = sorted(df_raw[seg_col].dropna().unique().tolist())
        selected_segments = st.sidebar.multiselect(
            f"Select {seg_col}",
            options=all_segments,
            default=st.session_state.get("filter_segments", all_segments),
            key="filter_segments"
        )
    else:
        selected_segments = None

    # Widget 3: Numeric Threshold Slider
    num_cols = df_raw.select_dtypes(include="number").columns.tolist()
    slider_col = "Ticket Id" if "Ticket Id" in num_cols else (num_cols[0] if num_cols else None)
    if slider_col:
        min_val = int(df_raw[slider_col].min())
        max_val = int(df_raw[slider_col].max())
        if min_val == max_val:
            max_val += 1
        num_range = st.sidebar.slider(
            f"{slider_col} Range",
            min_value=min_val,
            max_value=max_val,
            value=st.session_state.get("filter_numeric_range", (min_val, max_val)),
            key="filter_numeric_range"
        )
    else:
        num_range = None

    # -------------------------------------------------
    # Task 2: Wire Widgets to Filter the DataFrame
    # -------------------------------------------------
    filtered_df = df_raw.copy()

    # Apply Date Range Filter
    if date_range and len(date_range) == 2:
        start_date, end_date = date_range
        filtered_df = filtered_df[
            (filtered_df[date_col].dt.date >= start_date) &
            (filtered_df[date_col].dt.date <= end_date)
        ]

    # Apply Multi-select Segment Filter
    if seg_col:
        filtered_df = filtered_df[filtered_df[seg_col].isin(selected_segments)]

    # Apply Numeric Range Slider Filter
    if slider_col and num_range:
        filtered_df = filtered_df[
            (filtered_df[slider_col] >= num_range[0]) &
            (filtered_df[slider_col] <= num_range[1])
        ]

    # -------------------------------------------------
    # Task 4: Handle Empty Filter Combinations
    # -------------------------------------------------
    if len(filtered_df) == 0:
        st.warning("⚠️ No data matches the current filters. Try broadening your selection or click 'Reset Filters'.")
        st.stop()

    df = filtered_df  # Assign globally for downstream pages

    # ============================================================
    # OVERVIEW PAGE
    # ============================================================

    if page == "Overview":

        st.title("📊 Business Overview")
        st.caption(f"Showing {len(df):,} of {len(df_raw):,} total records")

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

        # Dynamic Alerts
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
        st.header("Filtered Dataset Summary")
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

        with right:
            st.subheader("Top Programs")
            if prog_col:
                st.dataframe(
                    df[prog_col].value_counts().head(10).reset_index().rename(
                        columns={"index": "Program", prog_col: "Tickets"}
                    ),
                    use_container_width=True
                )

    # ============================================================
    # TREND ANALYSIS PAGE
    # ============================================================

    elif page == "Trend Analysis":

        st.title("📈 Trend Analysis")
        st.caption(f"Showing trends for {len(df):,} filtered records")

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

        st.header("Quick Statistics")
        st.dataframe(df.describe(), use_container_width=True)

    # ============================================================
    # DATA EXPLORER PAGE
    # ============================================================

    elif page == "Data Explorer":

        st.title("📂 Data Explorer")
        st.write(f"Showing **{len(df):,}** of **{len(df_raw):,}** total records based on sidebar filters.")

        st.dataframe(df, use_container_width=True, height=450)

        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download Filtered Dataset",
            data=csv,
            file_name="filtered_dataset.csv",
            mime="text/csv"
        )