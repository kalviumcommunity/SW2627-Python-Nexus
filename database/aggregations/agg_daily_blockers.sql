INSERT INTO agg_daily_blockers


SELECT


DATE(created_time),


'Daily Blockers',


COUNT(ticket_id),


COUNT(ticket_id),


CURRENT_TIMESTAMP


FROM blockers


GROUP BY DATE(created_time);
