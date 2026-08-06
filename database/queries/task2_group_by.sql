/*
GROUP BY multiple dimensions.

Business question:
Which program and employee type generates most blockers?
*/


SELECT


e.employee_type,

e.program_name,


COUNT(b.ticket_id)
AS total_blockers,


AVG(b.resolution_hours)
AS avg_resolution_time,


SUM(b.resolution_hours)
AS total_resolution_hours


FROM blockers b


JOIN employees e

ON b.employee_id=e.employee_id


WHERE b.status='Closed'


GROUP BY

e.employee_type,

e.program_name


ORDER BY total_blockers DESC;