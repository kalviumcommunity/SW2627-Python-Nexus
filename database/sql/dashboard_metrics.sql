-- ==============================================
-- Remote Work Blocker Dashboard Metrics
-- ==============================================


-- KPI 1: Total Tickets

SELECT 
    COUNT(*) AS total_tickets
FROM tickets;



-- KPI 2: Closed Tickets

SELECT
    COUNT(*) AS closed_tickets
FROM tickets
WHERE status = 'Closed';



-- KPI 3: Average Resolution Time

SELECT
    ROUND(
        AVG(
            EXTRACT(EPOCH FROM 
            (closed_time - created_time))/3600
        ),2
    ) AS avg_resolution_hours
FROM tickets
WHERE closed_time IS NOT NULL;



-- KPI 4: First Response SLA

SELECT
    ROUND(
        AVG(
        EXTRACT(EPOCH FROM 
        (first_response_time-created_time))/3600
        ),2
    )
    AS avg_first_response_hours
FROM tickets
WHERE first_response_time IS NOT NULL;



-- KPI 5: Open Ticket Percentage

SELECT
    ROUND(
        COUNT(*) FILTER(
        WHERE status!='Closed'
        )*100.0/COUNT(*),2
    )
AS open_ticket_percentage
FROM tickets;