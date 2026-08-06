SELECT


t.team_name,

e.employee_type,

e.program_name,


COUNT(b.ticket_id)
AS total_blockers,


AVG(b.resolution_hours)
AS avg_resolution



FROM teams t


LEFT JOIN employees e

ON t.team_id=e.team_id


LEFT JOIN blockers b

ON e.employee_id=b.employee_id



GROUP BY

t.team_name,

e.employee_type,

e.program_name


ORDER BY total_blockers DESC;
