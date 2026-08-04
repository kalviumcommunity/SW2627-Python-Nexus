import pandas as pd
import numpy as np
from datetime import datetime, timedelta

np.random.seed(42)

# --- 1. JIRA VELOCITY DATASET (108 rows) ---
teams = [("TEAM-ALPHA", "Backend Core"), ("TEAM-BETA", "Frontend Web"), ("TEAM-GAMMA", "DevOps & Infra")]
sprints = [f"SPRINT-00{i}" for i in range(1, 7)]
jira_rows = []

start_date = datetime(2026, 4, 6)
for s_idx, (s_id) in enumerate(sprints):
    s_start = start_date + timedelta(weeks=s_idx*2)
    s_end = s_start + timedelta(days=11)
    for t_id, t_name in teams:
        for variation in range(6): # Creates 108 records across sub-modules/sprints
            committed = np.random.randint(30, 50)
            # Create a systemic drop in Sprints 2, 3, 4 for Alpha & Gamma due to Environment blockers
            if s_idx in [1, 2, 3] and t_id in ["TEAM-ALPHA", "TEAM-GAMMA"]:
                completed = int(committed * np.random.uniform(0.55, 0.72))
                cycle_time = round(np.random.uniform(6.0, 9.5), 1)
                bugs = np.random.randint(7, 14)
            else:
                completed = int(committed * np.random.uniform(0.88, 1.0))
                cycle_time = round(np.random.uniform(2.5, 4.5), 1)
                bugs = np.random.randint(1, 5)
            
            jira_rows.append({
                "sprint_id": s_id,
                "team_id": t_id,
                "team_name": t_name,
                "sprint_name": f"Sprint {40+s_idx+1}.{variation+1}",
                "start_date": s_start.strftime("%Y-%m-%d"),
                "end_date": s_end.strftime("%Y-%m-%d"),
                "committed_points": committed,
                "completed_points": completed,
                "velocity_completion_pct": round((completed / committed) * 100, 1),
                "avg_cycle_time_days": cycle_time,
                "bugs_logged": bugs
            })

df_jira = pd.DataFrame(jira_rows)
df_jira.to_csv("jira_velocity.csv", index=False)


# --- 2. SLACK STANDUPS DATASET (180 rows) ---
authors = {
    "TEAM-ALPHA": [("USR-101", "Alex Chen"), ("USR-102", "Ravi Patel")],
    "TEAM-BETA": [("USR-201", "Sarah Jenkins"), ("USR-202", "Elena Rostova")],
    "TEAM-GAMMA": [("USR-301", "David Miller"), ("USR-302", "Marcus Vance")]
}

categories = ["Environment & Access", "CI/CD & Pipeline", "Cross-Team Dependency", "PTO / Outage", "Process & Approval"]
blocker_phrases = [
    "Waiting on staging DB credentials from SecOps",
    "Flaky CI runner failing build suite",
    "Waiting on Backend API spec updates",
    "Out sick with flu",
    "Third-party API rate limits hit during testing",
    "PR review blocked waiting on Tech Lead signoff"
]

slack_rows = []
msg_id = 8800
for i in range(180):
    msg_id += 1
    t_id, t_name = teams[i % 3]
    author_id, author_name = authors[t_id][i % 2]
    has_blocker = np.random.choice([True, False], p=[0.65, 0.35])
    blocker_text = np.random.choice(blocker_phrases) if has_blocker else "None! Smooth sailing."
    
    slack_rows.append({
        "message_id": f"MSG-{msg_id}",
        "team_id": t_id,
        "channel_name": f"#standup-{t_name.split()[0].lower()}",
        "author_id": author_id,
        "author_name": author_name,
        "timestamp": (datetime(2026, 4, 6) + timedelta(days=i//2)).strftime("%Y-%m-%dT09:%M:00Z"),
        "yesterday_text": "Worked on assigned backlog items and code review.",
        "today_text": "Continuing development and integration testing.",
        "blocker_raw_text": blocker_text,
        "has_blocker_flag": has_blocker
    })

df_slack = pd.DataFrame(slack_rows)
df_slack.to_csv("slack_standups.csv", index=False)


# --- 3. NORMALIZED BLOCKERS & 4. GROUND TRUTH (120 rows) ---
norm_rows = []
truth_rows = []

for i in range(1, 121):
    blk_id = f"BLK-{1000+i}"
    t_id = np.random.choice(["TEAM-ALPHA", "TEAM-BETA", "TEAM-GAMMA"])
    s_id = f"SPRINT-00{np.random.randint(1, 7)}"
    category = np.random.choice(categories, p=[0.35, 0.20, 0.20, 0.15, 0.10])
    is_ext = category in ["Environment & Access", "Cross-Team Dependency"]
    
    # Simulate realistic duration
    if category == "Environment & Access":
        duration = np.random.randint(5, 10)
    else:
        duration = np.random.randint(1, 4)
        
    norm_rows.append({
        "blocker_id": blk_id,
        "source_type": np.random.choice(["Slack", "Jira", "CSV"]),
        "source_id": f"SRC-{5000+i}",
        "team_id": t_id,
        "sprint_id": s_id,
        "date_logged": (datetime(2026, 4, 6) + timedelta(days=i)).strftime("%Y-%m-%d"),
        "category": category,
        "description": f"Impediment related to {category.lower()} impacting sprint delivery.",
        "is_external_dependency": is_ext,
        "resolution_time_days": duration,
        "status": "Resolved"
    })
    
    # Classification Logic (Section 8 rules)
    r1 = category == "Environment & Access" # Same category recurs >=3 sprints
    r2 = category in ["Environment & Access", "Cross-Team Dependency"] and t_id in ["TEAM-ALPHA", "TEAM-GAMMA"]
    r3 = duration > 5
    r4 = is_ext
    
    score = sum([r1, r2, r3, r4])
    classification = "Systemic" if score > 2 else "Transient"
    
    reason = f"Met {score}/4 criteria. " + (
        f"Triggers systemic alert due to recurring '{category}' issue." if classification == "Systemic" 
        else "Transient isolated impediment with quick turnaround."
    )
    
    truth_rows.append({
        "blocker_id": blk_id,
        "team_id": t_id,
        "category": category,
        "rule_1_recurs_3_sprints": r1,
        "rule_2_cross_team_pattern": r2,
        "rule_3_duration_gt_5days": r3,
        "rule_4_external_dependency": r4,
        "rules_triggered_count": score,
        "final_classification": classification,
        "explainable_reason": reason
    })

df_norm = pd.DataFrame(norm_rows)
df_norm.to_csv("normalized_blockers.csv", index=False)

df_truth = pd.DataFrame(truth_rows)
df_truth.to_csv("systemic_classification_ground_truth.csv", index=False)

print("Successfully generated 4 CSV datasets with >100 records each!")