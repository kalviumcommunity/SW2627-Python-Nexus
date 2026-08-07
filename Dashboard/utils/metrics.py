import pandas as pd
import numpy as np
from typing import Dict, Any, List

def calculate_kpis(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Dynamically calculates all 7 leadership KPI metrics from the filtered DataFrame.
    """
    if df.empty:
        return {
            "total_blockers": 0,
            "resolved_blockers": 0,
            "resolution_rate": 0.0,
            "avg_resolution_time": 0.0,
            "external_dependency_pct": 0.0,
            "most_affected_team": "N/A",
            "most_common_category": "N/A"
        }

    total_blockers = len(df)
    
    # Resolved count (matching case-insensitive 'resolved' or 'closed')
    resolved_mask = df["status"].astype(str).str.strip().str.lower().isin(["resolved", "closed"])
    resolved_blockers = int(resolved_mask.sum())
    
    resolution_rate = (resolved_blockers / total_blockers * 100) if total_blockers > 0 else 0.0
    
    avg_resolution_time = float(df["resolution_time_days"].mean()) if total_blockers > 0 else 0.0
    
    ext_count = int(df["is_external_dependency"].sum())
    external_dependency_pct = (ext_count / total_blockers * 100) if total_blockers > 0 else 0.0

    # Most affected team (mode)
    team_counts = df["team_id"].value_counts()
    most_affected_team = team_counts.index[0] if not team_counts.empty else "N/A"
    most_affected_team_count = int(team_counts.iloc[0]) if not team_counts.empty else 0

    # Most common category (mode)
    cat_counts = df["category"].value_counts()
    most_common_category = cat_counts.index[0] if not cat_counts.empty else "N/A"
    most_common_category_count = int(cat_counts.iloc[0]) if not cat_counts.empty else 0

    return {
        "total_blockers": total_blockers,
        "resolved_blockers": resolved_blockers,
        "resolution_rate": round(resolution_rate, 1),
        "avg_resolution_time": round(avg_resolution_time, 2),
        "external_dependency_pct": round(external_dependency_pct, 1),
        "most_affected_team": most_affected_team,
        "most_affected_team_count": most_affected_team_count,
        "most_common_category": most_common_category,
        "most_common_category_count": most_common_category_count
    }


def generate_root_cause_insights(df: pd.DataFrame) -> List[Dict[str, str]]:
    """
    Generates actionable root cause recommendation cards dynamically based on filtered data.
    """
    if df.empty:
        return []

    insights = []
    total = len(df)

    # Insight 1: External Dependency Impact
    ext_df = df[df["is_external_dependency"]]
    int_df = df[~df["is_external_dependency"]]
    
    ext_pct = (len(ext_df) / total * 100) if total > 0 else 0
    ext_avg_res = ext_df["resolution_time_days"].mean() if not ext_df.empty else 0
    int_avg_res = int_df["resolution_time_days"].mean() if not int_df.empty else 0

    if ext_pct > 25:
        diff_days = ext_avg_res - int_avg_res
        insights.append({
            "title": "🚨 High External Dependency Risk",
            "type": "warning" if ext_pct < 50 else "critical",
            "category": "External Dependencies",
            "observation": f"External dependencies account for **{ext_pct:.1f}%** of all logged blockers.",
            "impact": f"External blockers take an average of **{ext_avg_res:.1f} days** to resolve compared to **{int_avg_res:.1f} days** for internal issues (+{diff_days:.1f} days delay).",
            "recommendation": "Establish SLAs with third-party vendors and cross-team dependencies. Assign designated integration champions to avoid sprint stalling."
        })

    # Insight 2: Team-specific Bottleneck
    team_counts = df["team_id"].value_counts()
    if not team_counts.empty:
        top_team = team_counts.index[0]
        top_team_cnt = team_counts.iloc[0]
        top_team_pct = (top_team_cnt / total * 100)
        
        if top_team_pct > 30:
            insights.append({
                "title": f"⚠️ Concentrated Blocker Volume in {top_team}",
                "type": "warning",
                "category": "Team Allocation",
                "observation": f"**{top_team}** generated **{top_team_cnt} blockers** ({top_team_pct:.1f}% of total).",
                "impact": f"High recurring impediment density indicates environment or architectural complexity bottlenecking {top_team}.",
                "recommendation": f"Conduct a focused retrospective with {top_team} to streamline environment provisioning and unblock technical dependencies."
            })

    # Insight 3: Category with Longest Resolution Time
    cat_res = df.groupby("category")["resolution_time_days"].agg(["mean", "count"]).sort_values("mean", ascending=False)
    if not cat_res.empty:
        slowest_cat = cat_res.index[0]
        slowest_avg = cat_res.iloc[0]["mean"]
        slowest_cnt = int(cat_res.iloc[0]["count"])
        
        overall_avg = df["resolution_time_days"].mean()
        
        if slowest_avg > overall_avg:
            insights.append({
                "title": f"⏳ Category Delay: {slowest_cat}",
                "type": "critical" if slowest_avg > overall_avg * 1.3 else "warning",
                "category": "Resolution Speed",
                "observation": f"**{slowest_cat}** exhibits the longest average resolution time of **{slowest_avg:.2f} days** ({slowest_cnt} tickets).",
                "impact": f"Resolving {slowest_cat} takes **{slowest_avg - overall_avg:.1f} days longer** than the portfolio average ({overall_avg:.2f} days).",
                "recommendation": f"Standardize triage protocols and runbooks for '{slowest_cat}' to reduce resolution cycle time."
            })

    # Insight 4: Sprint Bottleneck Pattern
    sprint_counts = df.groupby("sprint_id").size().sort_values(ascending=False)
    if not sprint_counts.empty:
        peak_sprint = sprint_counts.index[0]
        peak_cnt = sprint_counts.iloc[0]
        insights.append({
            "title": f"📊 Sprint Bottleneck: {peak_sprint}",
            "type": "primary",
            "category": "Delivery Velocity",
            "observation": f"**{peak_sprint}** logged the highest blocker spikes with **{peak_cnt} issues**.",
            "impact": "Unusually high blocker concentration during specific sprints signals major scope changes or mid-sprint requirement shifts.",
            "recommendation": "Enforce strict Definition of Ready (DoR) during sprint planning to prevent unvetted tasks from entering active sprints."
        })

    return insights
