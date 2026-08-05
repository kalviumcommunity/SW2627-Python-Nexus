# Column to KPI Mapping

This document maps dataset columns to the key business metrics (KPIs) used throughout the analytics pipeline.

---

# Sprint Velocity

**Formula**

Completed Story Points / Committed Story Points × 100

**Related Columns**

- committed_points
- completed_points
- velocity_completion_pct

**Business Importance**

Measures how effectively engineering teams complete planned sprint work.

**Update Frequency**

At the end of every sprint.

---

# Team Productivity

**Formula**

SUM(completed_points) GROUP BY team_name

**Related Columns**

- team_id
- team_name
- completed_points

**Business Importance**

Compares engineering output across different teams.

**Update Frequency**

Every sprint.

---

# Average Cycle Time

**Formula**

AVG(avg_cycle_time_days)

**Related Columns**

- avg_cycle_time_days
- sprint_id
- team_name

**Business Importance**

Measures how quickly engineering work items move from start to completion.

**Update Frequency**

Every sprint.

---

# Defect Rate

**Formula**

SUM(bugs_logged)

or

AVG(bugs_logged)

**Related Columns**

- bugs_logged
- sprint_id
- team_name

**Business Importance**

Measures software quality during sprint execution.

**Update Frequency**

Every sprint.

---

# Ticket Resolution Rate

**Formula**

COUNT(Status='Closed') / COUNT(Ticket Id)

**Related Columns**

- Ticket Id
- Status (Ticket)

**Business Importance**

Measures customer support effectiveness.

**Update Frequency**

Daily

---

# First Response SLA

**Formula**

AVG(First Response Time - Created Time)

**Related Columns**

- Created Time (Ticket)
- First Response Time

**Business Importance**

Measures responsiveness of the support team.

**Update Frequency**

Daily

---

# Program-wise Ticket Volume

**Formula**

COUNT(Ticket Id) GROUP BY Program Name

**Related Columns**

- Ticket Id
- Program Name

**Business Importance**

Identifies programs generating the highest support demand.

**Update Frequency**

Weekly

---

# Phase-wise Support Issues

**Formula**

COUNT(Ticket Id) GROUP BY Project Phase

**Related Columns**

- Project Phase
- Ticket Id

**Business Importance**

Highlights learning phases with the highest support requests.

**Update Frequency**

Weekly

---

# Mean Time To Resolution (MTTR)

**Formula**

AVG(resolution_time_days)

**Related Columns**

- resolution_time_days
- category

**Business Importance**

Measures how quickly engineering blockers are resolved.

**Update Frequency**

Daily

---

# External Dependency Risk

**Formula**

COUNT(is_external_dependency=True)

**Related Columns**

- is_external_dependency
- category

**Business Importance**

Tracks blockers caused by external teams or vendors.

**Update Frequency**

Daily

---

# Systemic Blocker Rate

**Formula**

COUNT(final_classification='Systemic') /
COUNT(blocker_id)

**Related Columns**

- blocker_id
- final_classification

**Business Importance**

Measures the percentage of recurring engineering problems.

**Update Frequency**

Daily

---

# Rule Trigger Score

**Formula**

AVG(rules_triggered_count)

**Related Columns**

- rules_triggered_count

**Business Importance**

Measures the severity of engineering impediments.

**Update Frequency**

Daily