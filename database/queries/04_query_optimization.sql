
WITH recent_blockers AS
(

SELECT

ticket_id,

employee_id,

status,

created_time


FROM blockers


WHERE created_time >= '2021-01-01'

)


SELECT


rb.ticket_id,

rb.status,

e.employee_type,

e.program_name


FROM recent_blockers rb


JOIN employees e

ON rb.employee_id=e.employee_id;
