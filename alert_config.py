# alert_config.py

ALERT_THRESHOLDS = {

    "open_ticket_rate": {
        "metric": "Open Ticket Rate",
        "threshold": 40,
        "direction": "above",
        "severity": "critical",
        "message": "Too many tickets remain open. Investigate pending issues."
    },

    "closed_ticket_rate": {
        "metric": "Closed Ticket Rate",
        "threshold": 60,
        "direction": "below",
        "severity": "warning",
        "message": "Ticket resolution rate is below the expected target."
    },

    "null_percentage": {
        "metric": "Dataset Quality",
        "threshold": 5,
        "direction": "above",
        "severity": "warning",
        "message": "Dataset contains too many missing values."
    }

}