/*
LEFT JOIN Analysis

Purpose:
Find all employees and their blockers.

LEFT JOIN keeps employees even when
they have no blocker tickets.
*/


SELECT

e.employee_id,

e.employee_type,

COUNT(b.ticket_id) AS blocker_count,

SUM(b.resolution_hours) AS total_resolution_hours


FROM employees e


LEFT JOIN blockers b

ON e.employee_id = b.employee_id


GROUP BY

e.employee_id,

e.employee_type


ORDER BY total_resolution_hours DESC;

-- Count employees before join

SELECT COUNT(*) AS employee_count
FROM employees;


-- Count rows after LEFT JOIN

SELECT COUNT(*) AS joined_rows

FROM employees e

LEFT JOIN blockers b

ON e.employee_id=b.employee_id;