SELECT

project_phase,

COUNT(ticket_id)
AS blocker_count,


AVG(resolution_hours)
AS avg_resolution,


SUM(resolution_hours)
AS total_hours


FROM blockers


WHERE status='Closed'
AND resolution_hours > 0


GROUP BY project_phase


HAVING COUNT(ticket_id)>10


ORDER BY blocker_count DESC;