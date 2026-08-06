/*
WHERE filters individual rows BEFORE aggregation.

Use case:
Remove invalid blocker records before calculating metrics.
*/

SELECT

project_phase,

COUNT(ticket_id) AS blocker_count,

SUM(resolution_hours) AS total_resolution_hours

FROM blockers


WHERE status = 'Closed'
AND resolution_hours > 0
AND created_time >= '2021-01-01'


GROUP BY project_phase


ORDER BY blocker_count DESC;