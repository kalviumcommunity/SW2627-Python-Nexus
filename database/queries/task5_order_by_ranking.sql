/*
Ranking teams based on blocker impact
*/


SELECT


t.team_name,


COUNT(b.ticket_id)
AS blocker_count,


AVG(b.resolution_hours)
AS avg_resolution,


RANK() OVER
(
ORDER BY COUNT(b.ticket_id) DESC
)
AS blocker_rank



FROM blockers b


JOIN employees e

ON b.employee_id=e.employee_id


JOIN teams t

ON e.team_id=t.team_id



GROUP BY

t.team_name



HAVING COUNT(b.ticket_id)>2



ORDER BY blocker_count DESC


LIMIT 20;