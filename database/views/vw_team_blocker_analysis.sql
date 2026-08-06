CREATE VIEW vw_team_blocker_analysis AS


SELECT


e.employee_type,


e.program_name,


COUNT(b.ticket_id)
AS blocker_count,


AVG(b.resolution_hours)
AS avg_resolution


FROM employees e


LEFT JOIN blockers b

ON e.employee_id=b.employee_id


GROUP BY

e.employee_type,

e.program_name;
