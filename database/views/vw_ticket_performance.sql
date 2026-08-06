CREATE VIEW vw_ticket_performance AS


SELECT


project_phase,


COUNT(ticket_id)
AS total_tickets,


AVG(resolution_hours)
AS avg_resolution,


SUM(
CASE
WHEN status='Closed'
THEN 1
ELSE 0
END
)

AS closed_tickets


FROM blockers


GROUP BY project_phase;
