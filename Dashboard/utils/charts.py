import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict

# Consistent Brand Color Palette
COLOR_MAP = {
    "Primary": "#1E88E5",    # Professional Blue
    "Secondary": "#3B82F6",  # Light Blue
    "Success": "#10B981",    # Emerald Green
    "Warning": "#F59E0B",    # Amber Orange
    "Critical": "#EF4444",   # Crimson Red
    "Neutral": "#6B7280",    # Cool Grey
    "LightGrey": "#F3F4F6",
    "DarkGrey": "#374151"
}

CATEGORY_COLORS = [
    "#1E88E5", "#3B82F6", "#F59E0B", "#10B981", "#8B5CF6", "#EC4899", "#6B7280"
]

def apply_chart_theme(fig: go.Figure, title: str = "", height: int = 380) -> go.Figure:
    """Applies a clean, modern business design theme to Plotly figures."""
    fig.update_layout(
        title={
            "text": f"<b>{title}</b>",
            "font": {"size": 16, "family": "Inter, sans-serif", "color": "#1F2937"},
            "x": 0.01,
            "xanchor": "left"
        },
        height=height,
        margin=dict(l=40, r=40, t=50, b=40),
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(family="Inter, sans-serif", color="#374151", size=12),
        hoverlabel=dict(bgcolor="#1F2937", font_size=12, font_family="Inter, sans-serif", font_color="white"),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(size=11)
        )
    )
    fig.update_xaxes(
        showgrid=True,
        gridcolor="#E5E7EB",
        showline=True,
        linecolor="#D1D5DB",
        tickfont=dict(size=11)
    )
    fig.update_yaxes(
        showgrid=True,
        gridcolor="#E5E7EB",
        showline=True,
        linecolor="#D1D5DB",
        tickfont=dict(size=11)
    )
    return fig

# -------------------------------------------------------------
# 1. CATEGORY DISTRIBUTION BAR CHART
# -------------------------------------------------------------
def create_category_bar_chart(df: pd.DataFrame) -> go.Figure:
    if df.empty:
        return go.Figure()
    
    cat_counts = df["category"].value_counts().reset_index()
    cat_counts.columns = ["category", "count"]
    cat_counts = cat_counts.sort_values(by="count", ascending=True)

    fig = px.bar(
        cat_counts,
        x="count",
        y="category",
        orientation="h",
        text="count",
        color_discrete_sequence=[COLOR_MAP["Primary"]]
    )
    fig.update_traces(
        texttemplate="%{text}",
        textposition="outside",
        cliponaxis=False,
        marker_color=COLOR_MAP["Primary"],
        hovertemplate="<b>%{y}</b><br>Blockers: %{x}<extra></extra>"
    )
    fig.update_xaxes(title_text="Number of Blockers")
    fig.update_yaxes(title_text="Blocker Category")

    # Add insight annotation for highest category
    if not cat_counts.empty:
        top_cat = cat_counts.iloc[-1]["category"]
        top_val = cat_counts.iloc[-1]["count"]
        fig.add_annotation(
            x=top_val,
            y=top_cat,
            text=f"Most Common: {top_cat}",
            showarrow=True,
            arrowhead=2,
            arrowcolor=COLOR_MAP["Critical"],
            ax=40,
            ay=0,
            font=dict(size=10, color=COLOR_MAP["Critical"])
        )

    return apply_chart_theme(fig, "Blocker Category Distribution", height=360)

# -------------------------------------------------------------
# 2. TEAM-WISE BLOCKER HORIZONTAL BAR CHART
# -------------------------------------------------------------
def create_team_bar_chart(df: pd.DataFrame) -> go.Figure:
    if df.empty:
        return go.Figure()

    team_counts = df["team_id"].value_counts().reset_index()
    team_counts.columns = ["team_id", "count"]
    team_counts = team_counts.sort_values(by="count", ascending=True)

    fig = px.bar(
        team_counts,
        x="count",
        y="team_id",
        orientation="h",
        text="count",
        color="team_id",
        color_discrete_sequence=CATEGORY_COLORS
    )
    fig.update_traces(
        texttemplate="%{text}",
        textposition="outside",
        cliponaxis=False,
        hovertemplate="<b>%{y}</b><br>Blocker Volume: %{x}<extra></extra>"
    )
    fig.update_xaxes(title_text="Number of Blockers")
    fig.update_yaxes(title_text="Engineering Team")
    return apply_chart_theme(fig, "Team-wise Blocker Volume", height=360)

# -------------------------------------------------------------
# 3. EXTERNAL DEPENDENCY DONUT CHART
# -------------------------------------------------------------
def create_dependency_donut_chart(df: pd.DataFrame) -> go.Figure:
    if df.empty:
        return go.Figure()

    dep_counts = df["is_external_dependency"].map({True: "External Dependency", False: "Internal Coordination"}).value_counts().reset_index()
    dep_counts.columns = ["dependency_type", "count"]

    color_discrete_map = {
        "External Dependency": COLOR_MAP["Warning"],
        "Internal Coordination": COLOR_MAP["Primary"]
    }

    fig = px.pie(
        dep_counts,
        names="dependency_type",
        values="count",
        hole=0.55,
        color="dependency_type",
        color_discrete_map=color_discrete_map
    )
    fig.update_traces(
        textinfo="percent+label",
        hovertemplate="<b>%{label}</b><br>Count: %{value} (%{percent})<extra></extra>",
        marker=dict(line=dict(color="#FFFFFF", width=2))
    )
    
    total = len(df)
    ext_val = int(df["is_external_dependency"].sum())
    ext_pct = (ext_val / total * 100) if total > 0 else 0

    fig.add_annotation(
        text=f"<b>{ext_pct:.1f}%</b><br><span style='font-size:10px;'>External</span>",
        x=0.5, y=0.5,
        showarrow=False,
        font=dict(size=18, color=COLOR_MAP["Warning"])
    )

    return apply_chart_theme(fig, "Internal vs External Dependency Breakdown", height=360)

# -------------------------------------------------------------
# 4. BLOCKER TREND OVER TIME LINE CHART
# -------------------------------------------------------------
def create_trend_line_chart(df: pd.DataFrame) -> go.Figure:
    if df.empty:
        return go.Figure()

    trend = df.groupby(df["date_logged"].dt.date)["blocker_id"].count().reset_index()
    trend.columns = ["date", "count"]
    trend = trend.sort_values(by="date")

    # Calculate 7-day rolling average for smooth trendline
    trend["rolling_avg"] = trend["count"].rolling(window=3, min_periods=1).mean()

    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=trend["date"],
        y=trend["count"],
        mode="lines+markers",
        name="Daily Blockers",
        line=dict(color=COLOR_MAP["Primary"], width=2),
        marker=dict(size=6, color=COLOR_MAP["Primary"]),
        hovertemplate="<b>Date: %{x}</b><br>Blockers: %{y}<extra></extra>"
    ))

    fig.add_trace(go.Scatter(
        x=trend["date"],
        y=trend["rolling_avg"],
        mode="lines",
        name="Trendline (3-Day Moving Avg)",
        line=dict(color=COLOR_MAP["Warning"], width=2, dash="dash"),
        hovertemplate="<b>3-Day Avg: %{y:.1f}</b><extra></extra>"
    ))

    fig.update_xaxes(title_text="Date Logged")
    fig.update_yaxes(title_text="Blocker Count")

    if not trend.empty:
        peak_row = trend.iloc[trend["count"].idxmax()]
        fig.add_annotation(
            x=peak_row["date"],
            y=peak_row["count"],
            text=f"Peak Activity ({peak_row['count']} blockers)",
            showarrow=True,
            arrowhead=2,
            arrowcolor=COLOR_MAP["Critical"],
            ax=0,
            ay=-30,
            font=dict(size=10, color=COLOR_MAP["Critical"])
        )

    return apply_chart_theme(fig, "Blocker Volume Trend Over Time", height=380)

# -------------------------------------------------------------
# 5. SPRINT BOTTLENECK HEATMAP (Sprint vs Blocker Category)
# -------------------------------------------------------------
def create_sprint_category_heatmap(df: pd.DataFrame) -> go.Figure:
    if df.empty:
        return go.Figure()

    pivot = pd.crosstab(df["sprint_id"], df["category"])
    
    # Sort sprints logically
    sprint_order = sorted(pivot.index, key=lambda s: int(s.split("-")[-1]) if "-" in s and s.split("-")[-1].isdigit() else 0)
    pivot = pivot.reindex(sprint_order)

    fig = px.imshow(
        pivot,
        labels=dict(x="Blocker Category", y="Sprint ID", color="Blocker Count"),
        x=pivot.columns,
        y=pivot.index,
        color_continuous_scale="Blues",
        text_auto=True
    )
    fig.update_traces(
        hovertemplate="<b>%{y} | %{x}</b><br>Blockers: %{z}<extra></extra>"
    )
    fig.update_xaxes(title_text="Blocker Category", side="bottom")
    fig.update_yaxes(title_text="Sprint")

    return apply_chart_theme(fig, "Sprint Bottleneck Heatmap (Sprint vs Category)", height=380)

# -------------------------------------------------------------
# 6. RESOLUTION TIME BOX PLOT BY CATEGORY
# -------------------------------------------------------------
def create_resolution_box_plot(df: pd.DataFrame) -> go.Figure:
    if df.empty:
        return go.Figure()

    fig = px.box(
        df,
        x="category",
        y="resolution_time_days",
        color="category",
        points="all",
        color_discrete_sequence=CATEGORY_COLORS
    )
    
    overall_avg = df["resolution_time_days"].mean()
    fig.add_hline(
        y=overall_avg,
        line_dash="dash",
        line_color=COLOR_MAP["Critical"],
        annotation_text=f"Portfolio Avg: {overall_avg:.2f}d",
        annotation_position="top right"
    )

    fig.update_xaxes(title_text="Blocker Category")
    fig.update_yaxes(title_text="Resolution Time (Days)")
    fig.update_layout(showlegend=False)

    return apply_chart_theme(fig, "Resolution Time Distribution by Category (Box Plot)", height=380)
