/*
Find employees without blockers

Why important:

These are employees who have no recorded issues.
They should NOT be removed because they may be
new employees or have no problems.
*/


SELECT


e.employee_id,

e.employee_type,

e.program_name


FROM employees e


LEFT JOIN blockers b

ON e.employee_id=b.employee_id


WHERE b.ticket_id IS NULL;

/*
Find blockers without valid employees.

Business impact:

These records indicate:

1. Incorrect employee IDs
2. Data ingestion problems
3. Deleted employee records

They should be investigated before reporting metrics.
*/


SELECT


b.ticket_id,

b.employee_id,

b.project_phase


FROM blockers b


LEFT JOIN employees e

ON b.employee_id=e.employee_id


WHERE e.employee_id IS NULL;
