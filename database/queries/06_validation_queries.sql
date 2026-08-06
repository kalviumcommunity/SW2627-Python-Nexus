
-- Total blockers

SELECT COUNT(*)

FROM blockers;



-- Average resolution time

SELECT

AVG(resolution_hours)

FROM blockers;



-- Duplicate tickets

SELECT

COUNT(*)

FROM blockers

WHERE status='Duplicate';



-- Missing response time

SELECT COUNT(*)

FROM blockers

WHERE first_response_time IS NULL;
