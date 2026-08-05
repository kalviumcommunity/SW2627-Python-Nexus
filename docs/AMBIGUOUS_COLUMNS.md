# Ambiguous Columns & Business Interpretation

This document identifies columns whose names may be unclear to new analysts and proposes more descriptive business names.

---

# Column: sprint_id

## Original Ambiguity

Does this identify a sprint template, sprint instance, or project iteration?

## Resolved Meaning

Unique identifier for a specific Agile sprint.

## Business Interpretation

Represents the development iteration where engineering work was executed.

## Proposed Rename

agile_sprint_id

## Risk if Misunderstood

Incorrect sprint trend analysis.

---

# Column: team_id

## Original Ambiguity

Is this an HR team, engineering team, or business unit?

## Resolved Meaning

Engineering team identifier.

## Business Interpretation

Represents the software development team responsible for work.

## Proposed Rename

engineering_team_id

## Risk if Misunderstood

Incorrect productivity comparisons.

---

# Column: Status (Ticket)

## Original Ambiguity

Does status represent workflow state, SLA status, or customer status?

## Resolved Meaning

Current lifecycle state of the support ticket.

## Business Interpretation

Indicates whether customer issues have been resolved.

## Proposed Rename

ticket_status

## Risk if Misunderstood

Incorrect support performance reporting.

---

# Column: source_type

## Original Ambiguity

Could represent file format or business system.

## Resolved Meaning

Operational system where blocker originated.

## Business Interpretation

Shows whether blocker came from Jira, Slack, or imported CSV.

## Proposed Rename

source_system

## Risk if Misunderstood

Incorrect source quality analysis.

---

# Column: category

## Original Ambiguity

Category of what?

## Resolved Meaning

Engineering blocker classification.

## Business Interpretation

Groups engineering issues into business problem domains.

## Proposed Rename

blocker_category

## Risk if Misunderstood

Incorrect reporting by issue type.

---

# Column: rules_triggered_count

## Original Ambiguity

Which rules?

## Resolved Meaning

Number of systemic detection rules satisfied.

## Business Interpretation

Represents blocker severity according to the rule engine.

## Proposed Rename

systemic_rule_score

## Risk if Misunderstood

Incorrect interpretation of classification confidence.

---

# Column: final_classification

## Original Ambiguity

Classification of what?

## Resolved Meaning

Final engineering assessment of blocker.

## Business Interpretation

Indicates whether the blocker is Systemic or Transient.

## Proposed Rename

blocker_classification

## Risk if Misunderstood

Incorrect predictive model training.