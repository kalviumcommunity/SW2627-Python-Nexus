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
# Task 1, 2 & 5: Safely Initialise Session State with Descriptive Keys & Documentation
# -------------------------------------------------

# "selected_segment" - Stores the user's segment/program choice confirmed in Step 1
# so it survives script reruns when interacting with Step 2 or Step 3 widgets.
if "selected_segment" not in st.session_state:
    st.session_state["selected_segment"] = "All"

# "workflow_step" - Tracks which stage of the multi-step workflow the user is currently on (1, 2, or 3).
# Prevents Step 2 or Step 3 from displaying before Step 1 is explicitly confirmed.
if "workflow_step" not in st.session_state:
    st.session_state["workflow_step"] = 1

# "analysis_result" - Caches the computed DataFrame/summary generated in Step 2
# so it does not recompute or reset when unrelated widgets on the page are toggled.
if "analysis_result" not in st.session_state:
    st.session_state["analysis_result"] = None

# "export_ready" - Tracks whether final analytics are calculated and ready for export
# so download controls remain active across reruns.
if "export_ready" not in st.session_state:
    st.session_state["export_ready"] = False


# -------------------------------------------------
# Sidebar Navigation
# -------------------------------------------------

st.sidebar.title("📊 Navigation")

page = st.sidebar.radio(
    "Select Section",
    [
        "File Upload & Preview",
        "Guided Workflow",
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

            # Persist dataset in session state across page navigation
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

    else:
        st.info("Upload a CSV or JSON file to begin.")

# ============================================================
# SHARED DATA LOADING FOR DASHBOARD & WORKFLOW
# ============================================================

else:
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

    date_col = "Created Time (Ticket)" if "Created Time (Ticket)" in df_raw.columns else None
    if date_col:
        df_raw[date_col] = pd.to_datetime(df_raw[date_col], dayfirst=True, errors="coerce")

    # ============================================================
    # TASK 3 & 4: MULTI-STEP WORKFLOW & SESSION STATE RESET
    # ============================================================

    if page == "Guided Workflow":
        st.title("🔄 Multi-Step Guided Workflow")
        st.caption("Walk through a 3-step analytics pipeline that maintains progress across widget updates.")

        # Task 4: Workflow Reset Controls
        st.sidebar.markdown("---")
        st.sidebar.header("🔄 Workflow Reset")
        if st.sidebar.button("Reset Workflow", use_container_width=True):
            # Clear all workflow state keys
            for key in ["selected_segment", "workflow_step", "analysis_result", "export_ready"]:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()

        # Visual Progress Indicator
        step_names = {1: "1. Select Segment", 2: "2. Deep-Dive Analysis", 3: "3. Export & Insights"}
        st.info(f"📍 **Current Stage**: Step {st.session_state['workflow_step']} of 3 - {step_names[st.session_state['workflow_step']]}")

        # -------------------------------------------------
        # STEP 1: Select Segment
        # -------------------------------------------------
        st.header("Step 1: Select Segment / Program")
        seg_col = "Program Name" if "Program Name" in df_raw.columns else df_raw.columns[0]
        segments = ["All"] + sorted(df_raw[seg_col].dropna().unique().tolist())

        # Selectbox default bound to session state
        default_index = segments.index(st.session_state["selected_segment"]) if st.session_state["selected_segment"] in segments else 0
        chosen_segment = st.selectbox("Choose Target Segment:", segments, index=default_index)

        if st.button("Confirm Segment & Proceed to Step 2 ➡️"):
            st.session_state["selected_segment"] = chosen_segment
            st.session_state["workflow_step"] = max(st.session_state["workflow_step"], 2)
            st.rerun()

        st.divider()

        # -------------------------------------------------
        # STEP 2: Configure & Perform Analysis (Dependent on Step 1)
        # -------------------------------------------------
        if st.session_state["workflow_step"] >= 2:
            st.header("Step 2: Analysis & Metrics Computation")
            st.write(f"Target Segment: **{st.session_state['selected_segment']}**")

            # Filter data according to Step 1 choice
            if st.session_state["selected_segment"] == "All":
                segment_df = df_raw.copy()
            else:
                segment_df = df_raw[df_raw[seg_col] == st.session_state["selected_segment"]]

            # Interactive widget within Step 2
            analysis_focus = st.radio(
                "Metric Focus:",
                ["Ticket Status Summary", "Project Phase Breakdown"],
                horizontal=True
            )

            if st.button("Run Analysis & Proceed to Step 3 ⚙️"):
                # Store calculated intermediate result into session state
                if analysis_focus == "Ticket Status Summary":
                    status_col = "Status (Ticket)" if "Status (Ticket)" in segment_df.columns else segment_df.columns[0]
                    res = segment_df[status_col].value_counts().reset_index()
                    res.columns = ["Status", "Ticket Count"]
                else:
                    phase_col = "Project Phase" if "Project Phase" in segment_df.columns else segment_df.columns[0]
                    res = segment_df[phase_col].value_counts().reset_index()
                    res.columns = ["Project Phase", "Ticket Count"]

                st.session_state["analysis_result"] = res
                st.session_state["export_ready"] = True
                st.session_state["workflow_step"] = 3
                st.rerun()

            st.divider()

        # -------------------------------------------------
        # STEP 3: Results & Export (Dependent on Step 2)
        # -------------------------------------------------
        if st.session_state["workflow_step"] >= 3:
            st.header("Step 3: Actionable Insights & Export")

            if st.session_state["analysis_result"] is not None:
                st.subheader("Cached Analysis Output")
                res_df = st.session_state["analysis_result"]
                st.dataframe(res_df, use_container_width=True)

                st.bar_chart(res_df.set_index(res_df.columns[0]))

                # Export option
                csv_data = res_df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    label="📥 Export Analysis CSV",
                    data=csv_data,
                    file_name=f"analysis_{st.session_state['selected_segment']}.csv",
                    mime="text/csv"
                )
            else:
                st.warning("No analysis results found. Please rerun Step 2.")

    # ============================================================
    # OVERVIEW PAGE
    # ============================================================

    elif page == "Overview":
        st.title("📊 Business Overview")
        df = df_raw

        total_tickets = len(df)
        status_col = "Status (Ticket)" if "Status (Ticket)" in df.columns else None
        prog_col = "Program Name" if "Program Name" in df.columns else None
        phase_col = "Project Phase" if "Project Phase" in df.columns else None

        open_tickets = df[status_col].astype(str).str.contains("Open", case=False, na=False).sum() if status_col else 0
        closed_tickets = df[status_col].astype(str).str.contains("Closed", case=False, na=False).sum() if status_col else 0
        programs = df[prog_col].nunique() if prog_col else 0
        phases = df[phase_col].nunique() if phase_col else 0

        open_ticket_rate = round((open_tickets / total_tickets) * 100, 2) if total_tickets > 0 else 0
        closed_ticket_rate = round((closed_tickets / total_tickets) * 100, 2) if total_tickets > 0 else 0
        
        total_cells = df.shape[0] * df.shape[1]
        null_percentage = round((df.isna().sum().sum() / total_cells) * 100, 2) if total_cells > 0 else 0

        current_metrics = {
            "open_ticket_rate": open_ticket_rate,
            "closed_ticket_rate": closed_ticket_rate,
            "null_percentage": null_percentage
        }

        st.header("🚨 Dashboard Alerts")
        for key, config in ALERT_THRESHOLDS.items():
            value = current_metrics.get(key, 0)
            breached = False
            if config["direction"] == "above":
                breached = value > config["threshold"]
            elif config["direction"] == "below":
                breached = value < config["threshold"]

            if breached:
                alert = f"{config['metric']} = {value:.2f}% | Threshold = {config['threshold']}% | {config['message']}"
                if config["severity"] == "critical":
                    st.error(alert)
                else:
                    st.warning(alert)

        c1, c2, c3, c4, c5 = st.columns(5)
        c1.metric("Total Tickets", f"{total_tickets:,}")
        c2.metric("Open Tickets", f"{open_tickets:,}")
        c3.metric("Closed Tickets", f"{closed_tickets:,}")
        c4.metric("Programs", programs)
        c5.metric("Project Phases", phases)

    # ============================================================
    # TREND ANALYSIS PAGE
    # ============================================================

    elif page == "Trend Analysis":
        st.title("📈 Trend Analysis")
        df = df_raw

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

    # ============================================================
    # DATA EXPLORER PAGE
    # ============================================================

    elif page == "Data Explorer":
        st.title("📂 Data Explorer")
        st.dataframe(df_raw, use_container_width=True, height=450)