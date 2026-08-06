/*
Real analytics scenario:

WHERE:
Remove bad records

HAVING:
Keep important blocker categories
*/


SELECT


e.program_name,


COUNT(b.ticket_id)
AS blockers,


AVG(b.resolution_hours)
AS avg_resolution



FROM blockers b


JOIN employees e

ON b.employee_id=e.employee_id



WHERE

b.status='Closed'

AND b.resolution_hours > 0



GROUP BY

e.program_name



HAVING

COUNT(b.ticket_id)>=5


AND AVG(b.resolution_hours)>5



ORDER BY blockers DESC;