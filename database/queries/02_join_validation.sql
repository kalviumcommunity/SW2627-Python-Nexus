/*
Purpose:
Find employees and their blockers.

LEFT JOIN keeps employees
even if they have no tickets.
*/


SELECT

e.employee_id,

e.employee_type,

COUNT(b.ticket_id)
AS blocker_count


FROM employees e


LEFT JOIN blockers b

ON e.employee_id=b.employee_id


GROUP BY

e.employee_id,

e.employee_type;

SELECT

e.employee_id,

e.employee_type


FROM employees e


LEFT JOIN blockers b

ON e.employee_id=b.employee_id


WHERE b.ticket_id IS NULL;


-- INNER JOIN

SELECT COUNT(*)

FROM employees e

INNER JOIN blockers b

ON e.employee_id=b.employee_id;



-- LEFT JOIN

SELECT COUNT(*)

FROM employees e

LEFT JOIN blockers b

ON e.employee_id=b.employee_id;



-- FULL JOIN

SELECT COUNT(*)

FROM employees e

FULL OUTER JOIN blockers b

ON e.employee_id=b.employee_id;
