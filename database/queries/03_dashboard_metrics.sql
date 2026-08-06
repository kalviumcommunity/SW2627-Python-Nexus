
SELECT

COUNT(*) 
AS total_blockers,


SUM(
CASE
WHEN status='Closed'
THEN 1
ELSE 0
END
)

AS resolved,


AVG(resolution_hours)

AS avg_resolution,


COUNT(
DISTINCT employee_id
)

AS affected_users,


COUNT(
DISTINCT project_phase
)

AS impacted_phases


FROM blockers;

SELECT

DATE(created_time)

AS day,


COUNT(ticket_id)

AS blockers


FROM blockers


GROUP BY DATE(created_time)


ORDER BY day;
