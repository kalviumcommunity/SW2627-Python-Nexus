SELECT

strftime('%Y-%m', "Created Time (Ticket)") AS month,

COUNT(DISTINCT "Ticket Id") AS total_tickets,

COUNT(DISTINCT "Student or WP") AS active_students,

COUNT(DISTINCT "Program Name") AS active_programs,

SUM(
CASE
WHEN "Ticket Closed Time" IS NOT NULL
THEN 1
ELSE 0
END
) AS closed_tickets

FROM Support_Tickets

GROUP BY month

ORDER BY month;