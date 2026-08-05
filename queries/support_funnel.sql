SELECT

DATE("Created Time (Ticket)") AS created_date,

COUNT(*) AS tickets_created,

SUM(

CASE

WHEN "First Response Time" IS NOT NULL

THEN 1

ELSE 0

END

) AS first_response,

SUM(

CASE

WHEN "Ticket Closed Time" IS NOT NULL

THEN 1

ELSE 0

END

) AS closed,

ROUND(

100.0*

SUM(

CASE

WHEN "Ticket Closed Time" IS NOT NULL

THEN 1

ELSE 0

END

)

/COUNT(*),

2

) AS closure_percentage

FROM Support_Tickets

GROUP BY DATE("Created Time (Ticket)")

ORDER BY created_date;