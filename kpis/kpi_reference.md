# KPI Reference Document

---

## KPI 1: Total Tickets

**Definition**

Total number of support tickets created.

**Formula**

COUNT(Ticket Id)

**Data Source**

Support Tickets Sheet

**Target**

1000+

**Owner**

Support Manager

**Update Frequency**

Daily

**Notes**

Represents total workload handled by the support team.

---

## KPI 2: Closed Ticket Rate

**Definition**

Percentage of tickets that have been closed.

**Formula**

Closed Tickets / Total Tickets × 100

**Data Source**

Ticket Closed Time

**Target**

> 90%

**Owner**

Operations Team

**Update Frequency**

Daily

**Notes**

Measures operational efficiency.

---

## KPI 3: Average Resolution Time

**Definition**

Average hours taken to close a ticket.

**Formula**

Average(Resolution Hours)

**Data Source**

Created Time & Ticket Closed Time

**Target**

< 48 Hours

**Owner**

Support Lead

**Update Frequency**

Daily

**Notes**

Lower values indicate faster customer support.

---

## KPI 4: Average First Response Time

**Definition**

Average time taken to send the first response.

**Formula**

Average(First Response Hours)

**Data Source**

Created Time & First Response Time

**Target**

< 2 Hours

**Owner**

Customer Success

**Update Frequency**

Daily

**Notes**

Critical SLA metric.

---

## KPI 5: Ticket Health Score

**Definition**

Composite score combining response speed, resolution speed, status and project phase.

**Formula**

0.4 × Resolution Score
+ 0.3 × Response Score
+ 0.2 × Status Score
+ 0.1 × Phase Score

**Data Source**

Engineered Features

**Target**

> 8

**Owner**

Operations

**Update Frequency**

Daily

**Notes**

Higher score indicates healthier support operations.

---

## KPI 6: Active Programs

**Definition**

Number of unique academic programs raising tickets.

**Formula**

COUNT(DISTINCT Program Name)

**Target**

N/A

**Owner**

Academic Operations

---

## KPI 7: Active Students

**Definition**

Unique students who created support tickets.

**Formula**

COUNT(DISTINCT Student or WP)

**Target**

N/A

**Owner**

Student Success Team