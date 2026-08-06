# Remote Work Blocker Analytics Dashboard

## Project Overview

The **Remote Work Blocker Analytics Dashboard** is an analytics product built to
identify, analyze, and monitor blockers faced by students and working
professionals.

The system processes support ticket data, performs data cleaning, creates
analytical features, generates KPIs, visualizes trends, and provides insights
to improve support operations.

The dashboard helps teams answer questions like:

- Which programs have the highest number of blockers?
- Which project phases create the most issues?
- How quickly are tickets resolved?
- Are working professionals or students facing more issues?
- Where should support improvements be prioritized?


---

# Dataset Description

## Dataset Source

Remote Work Blocker Ticket Dataset


## Dataset Columns

| Column Name | Data Type | Description |
|-------------|-----------|-------------|
| Ticket Id | Integer | Unique identifier for every ticket |
| Student or WP | String | User category (Student / Working Professional) |
| Program Name | String | Program associated with the ticket |
| Status (Ticket) | String | Current ticket status |
| Created Time (Ticket) | Datetime | Ticket creation timestamp |
| Ticket Closed Time | Datetime | Ticket resolution timestamp |
| First Response Time | Datetime | First support response timestamp |
| Project Phase | String | Learning phase where blocker occurred |


## Data Refresh

Current dataset:

- Historical CSV based analysis
- Can be replaced with scheduled pipeline ingestion
- Supports future database integration


---

# Project Features


## 1. Data Ingestion

The system supports:

- CSV loading
- Schema validation
- Data type checking
- Missing value detection


## 2. Data Cleaning

Cleaning operations include:

- Removing duplicate records
- Handling missing timestamps
- Converting date columns
- Standardizing categorical values


## 3. Feature Engineering

The pipeline creates additional analytical features:

- Resolution time
- First response delay
- Ticket age
- Closure indicator
- Blocker priority category


## 4. Analytics


### Ticket Analysis

- Total ticket count
- Closed tickets
- Duplicate tickets
- Deleted tickets
- Resolution percentage


### Program Analysis

Analyze blockers across:

- Fullstack Program
- Backend Program
- Fellowship Program


### User Segment Analysis

Compare:

- Students
- Working Professionals


### Phase Analysis

Identify problematic phases:

- Trial phase
- Fullstack phases
- Backend phases
- System issue phases


---

# Project Architecture


```text
                    Raw CSV Dataset
                           |
                           |
                           v

                  Data Ingestion Layer

                           |
                           |

                  Data Cleaning Pipeline

                           |
          -----------------------------------------
          |                                       |
          v                                       v

 Missing Value Handling             Data Type Conversion

                           |
                           |

                  Feature Engineering

                           |
                           |

                  Aggregation Layer

                           |
                           |

                   KPI Calculation

                           |
                           |

              Visualization Dashboard

                           |
                           |

                  Reports and Insights
```


---

# Project Structure


```text
Remote-Work-Blocker-Analytics/

│
├── app.py
│
├── requirements.txt
│
├── README.md
│
├── data/
│   │
│   ├── raw/
│   │   └── normalized_blocker.csv
│   │
│   └── processed/
│
│
├── scripts/
│   │
│   ├── data_pipeline.py
│   ├── analysis.py
│   └── export_report.py
│
│
├── output/
│   │
│   ├── cleaned_data.csv
│   ├── blocker_summary.csv
│   └── reports/
│
│
└── charts/
    │
    ├── blocker_distribution.png
    └── phase_analysis.png
```


---

# Setup Instructions


## Step 1: Clone Repository


```bash
git clone <repository-url>

cd Remote-Work-Blocker-Analytics
```


---

## Step 2: Create Virtual Environment


### Windows

```bash
python -m venv venv

venv\Scripts\activate
```


### Linux / Mac

```bash
python3 -m venv venv

source venv/bin/activate
```


---

## Step 3: Install Dependencies


```bash
pip install -r requirements.txt
```


---

## Step 4: Run Data Pipeline


```bash
python scripts/data_pipeline.py
```


Generated files:

```text
output/
```

---

## Step 5: Start Dashboard


```bash
streamlit run app.py
```


Dashboard URL:

```text
http://localhost:8501
```


---

# Usage Guide


## Upload Dataset


Place the CSV file inside:

```text
data/raw/
```


Example:

```text
data/raw/normalized_blocker.csv
```


---

# Dashboard Filters


Users can filter results using:

- Program Name
- User Type
- Project Phase
- Ticket Status


---

# Dashboard KPIs


| KPI | Description |
|---|---|
| Total Tickets | Total number of support tickets |
| Closed Tickets | Successfully resolved tickets |
| Resolution Rate | Percentage of resolved tickets |
| Avg Resolution Time | Average time taken to close tickets |
| Avg Response Time | Average support response delay |


---

# Visualization


## Ticket Distribution Chart

Shows ticket count by status.


## Program Analysis Chart

Shows blockers by program.


## Phase Analysis Chart

Identifies phases with maximum issues.


## User Segment Chart

Compares Students and Working Professionals.


---

# Derived Features Documentation


| Feature Name | Type | Description | Example |
|---|---|---|---|
| resolution_hours | Float | Hours taken to close ticket | 18.5 |
| response_hours | Float | Time taken for first response | 6.2 |
| ticket_age_days | Integer | Age of unresolved ticket | 3 |
| is_closed | Boolean | Whether ticket is closed | True |
| blocker_priority | String | Severity category | High |


---

# Data Pipeline Documentation


## Stage 1: Data Ingestion

Input:

```text
normalized_blocker.csv
```

Process:

- Load CSV file
- Validate columns
- Check data availability


Output:

Clean DataFrame


---

## Stage 2: Data Cleaning


Operations:

- Remove duplicate tickets
- Handle missing values
- Convert timestamps
- Normalize categories


Output:

Clean dataset


---

## Stage 3: Feature Engineering


Generated columns:


```text
resolution_hours

response_hours

ticket_age_days

is_closed
```


---

## Stage 4: Aggregation


Creates:

- Program-level summaries
- Phase-level summaries
- Status-level metrics


---

## Stage 5: Dashboard


Displays:

- KPIs
- Charts
- Trends
- Insights


---

# Known Limitations


## Dataset Limitations

- Data is historical and not real-time.
- Analysis depends on ticket accuracy.
- Missing timestamps reduce response-time accuracy.


## Business Assumptions

- Closed tickets are considered resolved.
- Duplicate tickets are ignored during blocker analysis.
- Resolution time depends only on available timestamps.


## Technical Limitations

- Pipeline expects fixed column names.
- Large datasets may require database storage.
- Alert thresholds require manual configuration.


---

# Future Improvements


Planned enhancements:

- Real-time ticket monitoring
- Database integration
- Automated email reports
- ML-based blocker prediction
- Root cause recommendation system
- Role-based dashboards


---

# Testing


Before deployment verify:


```text
✓ Dataset loads successfully

✓ Cleaning pipeline completes

✓ Features are generated

✓ Dashboard starts without errors

✓ Charts render correctly

✓ Reports are generated
```


---

# Contribution Guidelines


## Create Feature Branch


```bash
git checkout -b feature-name
```


## Commit Changes


```bash
git add .

git commit -m "describe changes"
```


## Push Changes


```bash
git push origin feature-name
```


---

# Support


For issues related to:

- Dataset
- Data pipeline
- Dashboard
- Analytics logic

refer to this documentation or contact the project maintainer.


---

# License


This project is developed for analytics and educational purposes.