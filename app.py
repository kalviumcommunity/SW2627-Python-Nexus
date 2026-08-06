import streamlit as st
import pandas as pd
from pathlib import Path
from alert_config import ALERT_THRESHOLDS
from report_generator import generate_report
from email_sender import send_report

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
        "Guided Workflow",
        "Overview",
        "Trend Analysis",
        "Data Explorer",
        "Report Generator"
    ]
)

# Shared Data Loading
if "uploaded_df" in st.session_state:
    df_raw = st.session_state["uploaded_df"].copy()
else:
    BASE_DIR = Path(__file__).parent
    DATA_FILE = BASE_DIR / "data" / "raw" / "Combined_Data.xlsx"
    try:
        df_raw = pd.read_excel(DATA_FILE, sheet_name="Support Tickets")
    except Exception:
        df_raw = pd.DataFrame()

# ============================================================
# REPORT GENERATOR & EMAIL DELIVERY PAGE
# ============================================================

if page == "Report Generator":
    st.title("📧 Automated Report Generator & Email Delivery")
    st.write("Generate a structured text summary of current analytics and deliver it directly to stakeholders.")

    if len(df_raw) == 0:
        st.warning("No data available. Please upload a dataset on the 'File Upload & Preview' page.")
        st.stop()

    st.header("1. Generated Report Preview")
    
    # Task 1 & 3: Generate Structured Report
    report_text = generate_report(df_raw)
    st.code(report_text, language="markdown")

    st.divider()

    st.header("2. Stakeholder Email Delivery")
    
    recipient_email = st.text_input("Recipient Email Address:", placeholder="stakeholder@company.com")
    
    if st.button("🚀 Send Email Report", type="primary"):
        if not recipient_email:
            st.error("Please enter a valid recipient email address.")
        else:
            with st.spinner("Connecting to SMTP server..."):
                # Task 2 & 4: Send report with non-blocking error handling
                success, message = send_report(report_text, recipient_email)
                
            if success:
                st.success(message)
            else:
                # Task 4: Logged error displayed cleanly without crashing app
                st.error(f"Email Delivery Status: {message}")
                st.info("Tip: Ensure SENDER_EMAIL and SENDER_PASSWORD are configured in your environment or .env file.")

# ============================================================
# FILE UPLOAD PAGE
# ============================================================

elif page == "File Upload & Preview":
    st.title("📂 Dataset Upload & Preview")
    uploaded_file = st.file_uploader("Upload dataset", type=["csv", "json"])
    if uploaded_file:
        df_upload = pd.read_csv(uploaded_file) if uploaded_file.name.endswith(".csv") else pd.read_json(uploaded_file)
        st.session_state["uploaded_df"] = df_upload
        st.success(f"Loaded {len(df_upload)} rows.")
        st.dataframe(df_upload.head(10))

# ============================================================
# OTHER PAGES (Overview, Trends, Explorer)
# ============================================================

else:
    st.title(f"📊 {page}")
    st.dataframe(df_raw.head(20))