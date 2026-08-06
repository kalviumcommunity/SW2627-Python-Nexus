-- INNER JOIN
-- Only employees with blockers


SELECT

COUNT(*)

FROM employees e

INNER JOIN blockers b

ON e.employee_id=b.employee_id;



-- LEFT JOIN
-- All employees retained


SELECT

COUNT(*)

FROM employees e

LEFT JOIN blockers b

ON e.employee_id=b.employee_id;



-- FULL OUTER JOIN
-- Everything from both tables


SELECT

COUNT(*)

FROM employees e

FULL OUTER JOIN blockers b

ON e.employee_id=b.employee_id;
