-- ==========================================
-- Ticket Priority Ranking Using Window Function
-- ==========================================


WITH phase_metrics AS
(
SELECT

project_phase,

COUNT(*) AS total_tickets,

COUNT(*) FILTER(
WHERE status='Closed'
) AS closed_tickets


FROM tickets

GROUP BY project_phase

)


SELECT

project_phase,

total_tickets,

closed_tickets,


RANK() OVER(
ORDER BY total_tickets DESC
)
AS blocker_rank


FROM phase_metrics;