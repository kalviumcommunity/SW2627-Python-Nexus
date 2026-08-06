CREATE DATABASE remote_work_analytics;

USE remote_work_analytics;


------------------------------------------------
-- Users / Employees
------------------------------------------------

CREATE TABLE employees
(
    employee_id INT PRIMARY KEY,
    employee_type VARCHAR(50),
    program_name VARCHAR(100),
    team_id VARCHAR(50)
);



------------------------------------------------
-- Remote Work Tickets
------------------------------------------------

CREATE TABLE blockers
(
    ticket_id INT PRIMARY KEY,

    employee_id INT,

    blocker_type VARCHAR(100),

    status VARCHAR(50),

    created_time TIMESTAMP,

    closed_time TIMESTAMP,

    first_response_time TIMESTAMP,

    project_phase VARCHAR(100),

    resolution_hours FLOAT,


    FOREIGN KEY(employee_id)
    REFERENCES employees(employee_id)

);



------------------------------------------------
-- Teams
------------------------------------------------

CREATE TABLE teams
(
    team_id VARCHAR(50) PRIMARY KEY,

    team_name VARCHAR(100),

    region VARCHAR(50)

);



------------------------------------------------
-- Daily Metrics
------------------------------------------------

CREATE TABLE agg_daily_blockers
(
    metric_date DATE,

    metric_name VARCHAR(100),

    metric_value FLOAT,

    record_count INT,

    updated_at TIMESTAMP

);