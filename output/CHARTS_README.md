
# Analysis Visualizations

## Chart 1: Blockers by Category

- Type: Bar Chart
- Business Question:
  Which blocker category occurs most frequently?
- Insight:
  Categories with the highest blocker counts require immediate attention.
- Annotation:
  Highest blocker category highlighted.

------------------------------------------------------------

## Chart 2: Daily Blocker Trend

- Type: Line Chart
- Business Question:
  How are blockers changing over time?
- Insight:
  Peaks indicate days with unusually high blocker creation.
- Annotation:
  Highest daily blocker count marked.

------------------------------------------------------------

## Chart 3: Resolution Time Distribution

- Type: Histogram
- Business Question:
  How long do blockers usually take to resolve?
- Insight:
  Most blockers are resolved within the average resolution window.
- Annotation:
  Average resolution time shown with dashed line.

------------------------------------------------------------

## Chart 4: Blockers by Source and Status

- Type: Stacked Bar Chart
- Business Question:
  Which source contributes the most blockers and what is their status?
- Insight:
  Helps compare resolved vs unresolved blockers across Jira, Slack and CSV.
- Annotation:
  Source with highest blocker volume highlighted.

------------------------------------------------------------

## Chart 5: Resolution Time vs External Dependency

- Type: Scatter Plot
- Business Question:
  Do external dependencies increase blocker resolution time?
- Insight:
  Trend line shows the relationship between dependency and resolution.
- Annotation:
  Longest resolution case highlighted.

------------------------------------------------------------

All charts were generated using:

- Matplotlib
- Pandas
- NumPy

Image Format:
PNG (300 DPI)

Output Folder:
output/
