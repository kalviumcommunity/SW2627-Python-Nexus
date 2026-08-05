# Data Dictionary

## Dataset Overview

This project integrates multiple operational datasets to analyze engineering productivity, support operations, and blocker management. The datasets are sourced from Jira, Slack, and internally normalized engineering records to support analytics, reporting, and decision-making.

**Datasets Included**

1. Jira Velocity
2. Slack Queries
3. Normalized Blockers
4. Systemic Classification Ground Truth

**Update Frequency:** Daily (or as new operational data becomes available)

**Maintained By:** Data Engineering / Analytics Team

---

# Dataset: jira_velocity

Contains sprint-level engineering metrics used to measure Agile team performance.

---

## sprint_id

- **Type:** String
- **Business Meaning:** Unique identifier for an Agile sprint.
- **Example:** `SPRINT-001`
- **Null Handling:** Never null.
- **Related KPI:** Sprint Performance
- **Updates:** Generated when a sprint is created.

---

## team_id

- **Type:** String
- **Business Meaning:** Unique identifier of the engineering team.
- **Example:** `TEAM-ALPHA`
- **Null Handling:** Never null.
- **Related KPI:** Team Productivity
- **Updates:** Assigned by project management system.

---

## team_name

- **Type:** String
- **Business Meaning:** Human-readable engineering team name.
- **Example:** Backend Core
- **Null Handling:** Never null.
- **Related KPI:** Team Performance Dashboard
- **Updates:** Maintained by engineering management.

---

## sprint_name

- **Type:** String
- **Business Meaning:** Display name of the sprint.
- **Example:** Sprint 41.1
- **Null Handling:** Never null.
- **Related KPI:** Sprint Tracking
- **Updates:** Generated during sprint planning.

---

## start_date

- **Type:** Date
- **Business Meaning:** Sprint start date.
- **Example:** 2026-04-06
- **Null Handling:** Never null.
- **Related KPI:** Sprint Duration
- **Updates:** Fixed after sprint creation.

---

## end_date

- **Type:** Date
- **Business Meaning:** Sprint completion date.
- **Example:** 2026-04-17
- **Null Handling:** Never null.
- **Related KPI:** Sprint Duration
- **Updates:** Fixed after sprint creation.

---

## committed_points

- **Type:** Integer
- **Business Meaning:** Total story points planned for the sprint.
- **Example:** 36
- **Null Handling:** Never null.
- **Related KPI:** Planning Accuracy
- **Updates:** Recorded before sprint starts.

---

## completed_points

- **Type:** Integer
- **Business Meaning:** Story points successfully completed.
- **Example:** 35
- **Null Handling:** Never null.
- **Related KPI:** Sprint Velocity
- **Updates:** Updated when sprint closes.

---

## velocity_completion_pct

- **Type:** Float
- **Business Meaning:** Percentage of committed work completed.
- **Example:** 97.2
- **Unit:** Percentage
- **Related KPI:** Sprint Velocity
- **Updates:** Calculated after sprint completion.

---

## avg_cycle_time_days

- **Type:** Float
- **Business Meaning:** Average number of days required to complete work items.
- **Example:** 2.9
- **Unit:** Days
- **Related KPI:** Cycle Time
- **Updates:** Calculated automatically.

---

## bugs_logged

- **Type:** Integer
- **Business Meaning:** Number of defects reported during the sprint.
- **Example:** 4
- **Null Handling:** Default is 0.
- **Related KPI:** Defect Rate
- **Updates:** Updated whenever bugs are logged.

---

# Dataset: slack_queries

Contains customer support tickets collected from Slack support operations.

---

## Ticket Id

- **Type:** Integer
- **Business Meaning:** Unique support ticket identifier.
- **Example:** 6403
- **Null Handling:** Never null.
- **Related KPI:** Ticket Volume
- **Updates:** Generated automatically.

---

## Student or WP

- **Type:** String
- **Business Meaning:** Customer category indicating Student or Working Professional.
- **Example:** Student
- **Valid Values:** Student, Working Professionals
- **Related KPI:** Customer Distribution
- **Updates:** Assigned during registration.

---

## Program Name

- **Type:** String
- **Business Meaning:** Program enrolled by the learner.
- **Example:** Fullstack Program
- **Related KPI:** Program Popularity
- **Updates:** Pulled from CRM.

---

## Status (Ticket)

- **Type:** String
- **Business Meaning:** Current lifecycle state of the support ticket.
- **Example:** Closed
- **Valid Values:** Closed, Deleted, Duplicate
- **Related KPI:** Resolution Rate
- **Updates:** Updated whenever ticket status changes.

---

## Created Time (Ticket)

- **Type:** Datetime
- **Business Meaning:** Timestamp when the ticket was created.
- **Example:** 14-05-2021 01:09
- **Related KPI:** Daily Ticket Volume
- **Updates:** Automatically generated.

---

## Ticket Closed Time

- **Type:** Datetime
- **Business Meaning:** Timestamp when ticket was resolved.
- **Example:** 14-05-2021 19:04
- **Null Handling:** Null if unresolved.
- **Related KPI:** Average Resolution Time
- **Updates:** Updated upon ticket closure.

---

## First Response Time

- **Type:** Datetime
- **Business Meaning:** Time of first agent response.
- **Example:** 14-05-2021 08:51
- **Null Handling:** Null if no response.
- **Related KPI:** First Response SLA
- **Updates:** Recorded automatically.

---

## Project Phase

- **Type:** String
- **Business Meaning:** Learning phase in which the issue occurred.
- **Example:** trial phase
- **Related KPI:** Phase-wise Ticket Distribution
- **Updates:** Derived from learning platform.

---

# Dataset: normalized_blockers

Contains engineering blockers consolidated from multiple operational systems.

---

## blocker_id

- **Type:** String
- **Business Meaning:** Unique blocker identifier.
- **Example:** BLK-1001
- **Related KPI:** Blocker Count
- **Null Handling:** Never null.

---

## source_type

- **Type:** String
- **Business Meaning:** System from which blocker originated.
- **Example:** Jira
- **Valid Values:** Jira, Slack, CSV
- **Related KPI:** Source Distribution

---

## source_id

- **Type:** String
- **Business Meaning:** Original identifier in the source system.
- **Example:** SRC-5001
- **Related KPI:** Data Traceability

---

## team_id

- **Type:** String
- **Business Meaning:** Engineering team responsible for blocker.
- **Example:** TEAM-GAMMA
- **Related KPI:** Team Health

---

## sprint_id

- **Type:** String
- **Business Meaning:** Sprint where blocker occurred.
- **Example:** SPRINT-006
- **Related KPI:** Sprint Health

---

## date_logged

- **Type:** Date
- **Business Meaning:** Date blocker was reported.
- **Example:** 2026-04-07
- **Related KPI:** Incident Trend

---

## category

- **Type:** String
- **Business Meaning:** Category describing blocker type.
- **Example:** Environment & Access
- **Related KPI:** Blocker Category Distribution

---

## description

- **Type:** String
- **Business Meaning:** Human-readable blocker description.
- **Example:** Impediment related to environment access.
- **Related KPI:** Incident Reporting

---

## is_external_dependency

- **Type:** Boolean
- **Business Meaning:** Indicates dependency on another team or system.
- **Example:** True
- **Related KPI:** Dependency Risk

---

## resolution_time_days

- **Type:** Integer
- **Business Meaning:** Days required to resolve blocker.
- **Example:** 5
- **Unit:** Days
- **Related KPI:** Mean Time to Resolution (MTTR)

---

## status

- **Type:** String
- **Business Meaning:** Current blocker status.
- **Example:** Resolved
- **Related KPI:** Resolution Rate

---

# Dataset: systemic_classification_ground_truth

Contains labels generated using rule-based logic for identifying systemic engineering issues.

---

## blocker_id

- **Type:** String
- **Business Meaning:** Identifier linking to normalized blocker.
- **Example:** BLK-1001
- **Related KPI:** Systemic Issue Tracking

---

## team_id

- **Type:** String
- **Business Meaning:** Engineering team owning blocker.
- **Example:** TEAM-GAMMA
- **Related KPI:** Team Health

---

## category

- **Type:** String
- **Business Meaning:** Blocker category used during classification.
- **Example:** Environment & Access
- **Related KPI:** Category Trends

---

## rule_1_recurs_3_sprints

- **Type:** Boolean
- **Business Meaning:** Indicates blocker recurred for three consecutive sprints.
- **Example:** True
- **Related KPI:** Recurring Issues

---

## rule_2_cross_team_pattern

- **Type:** Boolean
- **Business Meaning:** Indicates issue affects multiple engineering teams.
- **Example:** True
- **Related KPI:** Cross-Team Collaboration

---

## rule_3_duration_gt_5days

- **Type:** Boolean
- **Business Meaning:** Indicates blocker required more than five days to resolve.
- **Example:** False
- **Related KPI:** MTTR Compliance

---

## rule_4_external_dependency

- **Type:** Boolean
- **Business Meaning:** Indicates blocker depends on an external team or vendor.
- **Example:** True
- **Related KPI:** External Dependency Risk

---

## rules_triggered_count

- **Type:** Integer
- **Business Meaning:** Total number of rule conditions satisfied.
- **Example:** 3
- **Valid Range:** 0–4
- **Related KPI:** Systemic Risk Score

---

## final_classification

- **Type:** String
- **Business Meaning:** Final engineering classification of blocker.
- **Example:** Systemic
- **Valid Values:** Systemic, Transient
- **Related KPI:** Systemic Blocker Rate

---

## explainable_reason

- **Type:** String
- **Business Meaning:** Human-readable explanation of the classification decision.
- **Example:** Triggers systemic alert due to recurring Environment & Access issue.
- **Related KPI:** Model Explainability
- **Updates:** Generated by the rule engine.