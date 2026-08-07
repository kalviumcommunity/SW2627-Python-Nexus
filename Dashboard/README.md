# Remote Engineering Delivery Intelligence Dashboard

> **Portfolio Analytics Dashboard for Engineering Leadership**

## 📌 Problem Statement
A remote-first engineering company stores standup notes, sprint velocity, and blocker updates across separate tools (Jira, Slack, CSV). Leadership cannot easily distinguish temporary coordination issues from systemic delivery bottlenecks. 

This interactive analytics dashboard enables engineering leadership to:
1. Identify recurring blockers and systemic bottlenecks.
2. Quantify delivery risks caused by external dependencies and environment provisioning delays.
3. Drive operational improvements through dynamic, data-driven recommendation cards.

---

## 🛠️ Project Structure
```text
Dashboard/
├── app.py                     # Main Streamlit web application
├── requirements.txt           # Python dependencies
├── utils/
│   ├── data_loader.py         # Data pipeline, @st.cache_data, validation & feature engineering
│   ├── metrics.py             # Dynamic 7 KPI calculations & root cause insights generator
│   └── charts.py              # Interactive Plotly chart builders with brand theme
├── assets/                    # Static UI assets and screenshots
└── README.md                  # Project documentation
```

---

## 📊 Dashboard Key Features

### 1. Executive Overview & Dynamic KPIs
Calculated dynamically from the dataset:
- **Total Blockers**: Aggregate volume of logged impediments.
- **Resolved Blockers**: Successfully closed tickets.
- **Resolution Rate (%)**: Proportion of resolved issues.
- **Average Resolution Time**: Mean days to resolution.
- **External Dependency (%)**: Percentage of blockers tied to 3rd-party/cross-team bottlenecks.
- **Most Affected Team**: Engineering team experiencing highest impediment volume.
- **Most Common Category**: Primary blocker type.

### 2. Blocker Analysis
- **Category Distribution**: Bar chart identifying dominant blocker categories.
- **Team-wise Blocker Volume**: Horizontal bar chart comparing team friction.
- **Dependency Breakdown**: Donut chart displaying Internal vs External issue proportions.

### 3. Delivery Trend Analysis
- **Blocker Trend Over Time**: Line chart with 3-day moving average trendlines.
- **Sprint Bottleneck Heatmap**: Matrix mapping Sprint cycle vs Blocker Category.
- **Resolution Delay Box Plot**: Category-level resolution distribution highlighting outliers.

### 4. Root Cause Analysis & Automated Recommendations
Dynamic diagnostic engine generating structured insight cards:
- **"🚨 High External Dependency Risk"**: Triggered when external blockers exceed threshold.
- **"⚠️ Concentrated Blocker Volume"**: Highlights disproportionately impacted teams.
- **"⏳ Category Delay"**: Flags categories taking significantly longer than average resolution times.
- **"📊 Sprint Bottleneck"**: Pinpoints peak blocker activity sprints.

### 5. Interactive Multi-Filter Control
Sidebar filters update all charts and metrics automatically:
- Date Range Selector
- Engineering Team Multi-select
- Sprint Cycle Multi-select
- Blocker Category Multi-select
- Ticket Status Multi-select

---

## 🚀 Getting Started

### Prerequisites
- Python 3.9 or higher

### Installation
```bash
# Navigate to Dashboard folder
cd Dashboard

# Install dependencies
pip install -r requirements.txt
```

### Running the Dashboard
```bash
streamlit run app.py
```

Open browser at `http://localhost:8501`.

---

## 🎨 Color Palette & Aesthetics
- **Primary (Blue)**: `#1E88E5` - Core visual emphasis
- **Success (Green)**: `#10B981` - Resolution metrics
- **Warning (Orange)**: `#F59E0B` - External dependency alerts
- **Critical (Red)**: `#EF4444` - High risk / resolution delay flags
- **Neutral (Grey)**: `#6B7280` - Subtle UI borders & subtext
