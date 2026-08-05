SELECT

"Program Name",

COUNT(*) AS total_tickets,

COUNT(DISTINCT "Student or WP") AS unique_students,

SUM(
CASE
WHEN "Ticket Closed Time" IS NOT NULL
THEN 1
ELSE 0
END
) AS closed_tickets,

ROUND(

AVG("Resolution Hours"),

2

) AS avg_resolution_time,

ROUND(

AVG("First Response Hours"),

2

) AS avg_first_response

FROM Support_Tickets

GROUP BY "Program Name"

ORDER BY total_tickets DESC;