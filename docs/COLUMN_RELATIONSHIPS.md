# Column Relationships

This document explains how multiple columns work together to produce meaningful engineering and operational insights.

---

# Sprint Velocity

## Definition

Measures sprint execution efficiency.

## Formula

completed_points / committed_points × 100

## Related Columns

- committed_points
- completed_points
- velocity_completion_pct

## Business Impact

Determines whether teams deliver planned work.

## Example

Backend Core completed 35 of 36 committed points, achieving 97.2% sprint velocity.

---

# Team Productivity

## Definition

Total completed work delivered by each engineering team.

## Formula

SUM(completed_points)
GROUP BY team_name

## Related Columns

- team_id
- team_name
- completed_points

## Business Impact

Identifies high-performing engineering teams.

---

# Software Quality

## Definition

Relationship between sprint delivery and software defects.

## Related Columns

- completed_points
- bugs_logged

## Business Impact

Helps determine whether faster delivery increases defect rates.

---

# Support Resolution Time

## Definition

Time between ticket creation and ticket closure.

## Formula

Ticket Closed Time − Created Time

## Related Columns

- Created Time (Ticket)
- Ticket Closed Time
- Status (Ticket)

## Business Impact

Measures support team efficiency and SLA compliance.

---

# Customer Response SLA

## Definition

Measures how quickly support agents respond.

## Formula

First Response Time − Created Time

## Related Columns

- Created Time (Ticket)
- First Response Time

## Business Impact

Tracks customer experience and operational responsiveness.

---

# Program-wise Support Load

## Definition

Counts tickets raised for each learning program.

## Formula

COUNT(Ticket Id)
GROUP BY Program Name

## Related Columns

- Ticket Id
- Program Name

## Business Impact

Identifies products requiring additional support resources.

---

# Blocker Resolution Performance

## Definition

Average time required to resolve engineering blockers.

## Formula

AVG(resolution_time_days)

## Related Columns

- blocker_id
- resolution_time_days
- status

## Business Impact

Measures operational efficiency of engineering teams.

---

# External Dependency Analysis

## Definition

Measures blockers caused by dependencies outside the engineering team.

## Formula

COUNT(is_external_dependency=True)

## Related Columns

- is_external_dependency
- category
- team_id

## Business Impact

Identifies organizational bottlenecks requiring cross-team coordination.

---

# Systemic Issue Detection

## Definition

Combines multiple rule indicators to classify blockers.

## Formula

Classification based on:

- rule_1_recurs_3_sprints
- rule_2_cross_team_pattern
- rule_3_duration_gt_5days
- rule_4_external_dependency

## Related Columns

- rules_triggered_count
- final_classification

## Business Impact

Distinguishes recurring organizational problems from isolated incidents.

---

# Engineering Health Score

## Definition

Combines sprint velocity, blocker severity, and software quality.

## Related Columns

- velocity_completion_pct
- bugs_logged
- resolution_time_days
- final_classification

## Business Impact

Provides a high-level indicator of engineering organization health and delivery performance.