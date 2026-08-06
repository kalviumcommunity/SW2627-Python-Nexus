WITH monthly_tickets AS
(
SELECT

DATE_TRUNC(
'month',
created_time
) AS month,


COUNT(*) AS tickets


FROM tickets


GROUP BY month

)


SELECT

month,

tickets,


LAG(tickets)
OVER(
ORDER BY month
)
AS previous_month_tickets,


tickets -
LAG(tickets)
OVER(
ORDER BY month
)
AS ticket_change


FROM monthly_tickets

ORDER BY month;