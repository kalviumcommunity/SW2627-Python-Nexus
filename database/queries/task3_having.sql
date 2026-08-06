/*
HAVING filters aggregated groups.

WHERE:
filters rows

HAVING:
filters groups after aggregation
*/


SELECT


project_phase,


COUNT(ticket_id)
AS blocker_count,


AVG(resolution_hours)
AS avg_resolution



FROM blockers


WHERE status='Closed'


GROUP BY project_phase


HAVING COUNT(ticket_id) > 5


AND AVG(resolution_hours)>10


ORDER BY blocker_count DESC;