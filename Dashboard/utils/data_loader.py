import pandas as pd
import numpy as np
import streamlit as st
from pathlib import Path

# Color palette definition for unified usage
COLOR_PALETTE = {
    "primary": "#1E88E5",    # Professional Blue
    "success": "#10B981",    # Emerald Green
    "warning": "#F59E0B",    # Amber Orange
    "critical": "#EF4444",   # Crimson Red
    "neutral": "#6B7280",    # Muted Grey
    "secondary": "#3B82F6",  # Light Blue Accent
    "dark_bg": "#1F2937",
    "light_bg": "#F8FAFC"
}

@st.cache_data
def load_and_preprocess_data(file_path: str = None) -> pd.DataFrame:
    """
    Loads, cleans, validates, and engineers features for the Blocker Dataset.
    Uses @st.cache_data for performance optimization.
    """
    if file_path is None or not Path(file_path).exists():
        # Fallback paths inside the workspace
        possible_paths = [
            Path(__file__).resolve().parent.parent.parent / "data" / "raw" / "normalized_blocker.csv",
            Path(__file__).resolve().parent.parent / "data" / "raw" / "normalized_blocker.csv",
            Path("data/raw/normalized_blocker.csv"),
            Path("../data/raw/normalized_blocker.csv"),
            Path("normalized_blocker.csv")
        ]
        found_path = None
        for p in possible_paths:
            if p.exists():
                found_path = p
                break
        
        if found_path is None:
            raise FileNotFoundError("normalized_blocker.csv could not be located in workspace paths.")
        file_path = str(found_path)

    # Load dataset
    df = pd.read_csv(file_path)

    # Column Validation
    required_cols = [
        "blocker_id", "team_id", "sprint_id", "date_logged",
        "category", "is_external_dependency", "resolution_time_days", "status"
    ]
    
    missing = [col for col in required_cols if col not in df.columns]
    if missing:
        raise ValueError(f"Dataset is missing required columns: {missing}")

    # Data Type Conversions & Cleaning
    df["date_logged"] = pd.to_datetime(df["date_logged"], errors="coerce")
    df["resolution_time_days"] = pd.to_numeric(df["resolution_time_days"], errors="coerce").fillna(0)
    
    # Standardize Boolean / Strings for External Dependency
    if df["is_external_dependency"].dtype == object:
        df["is_external_dependency"] = df["is_external_dependency"].astype(str).str.strip().str.lower().isin(["true", "1", "yes"])
    else:
        df["is_external_dependency"] = df["is_external_dependency"].astype(bool)

    # Fill missing categorical values
    df["source_type"] = df.get("source_type", pd.Series(["Unknown"]*len(df))).fillna("Unknown")
    df["category"] = df["category"].fillna("Uncategorized")
    df["team_id"] = df["team_id"].fillna("Unknown Team")
    df["sprint_id"] = df["sprint_id"].fillna("SPRINT-000")
    df["status"] = df["status"].fillna("Open")
    df["description"] = df.get("description", pd.Series(["No description"]*len(df))).fillna("No description")

    # Feature Engineering
    # 1. Sprint number integer for sorting
    df["sprint_num"] = df["sprint_id"].str.extract(r'(\d+)').astype(float).fillna(0).astype(int)
    
    # 2. Resolution speed category
    df["resolution_bucket"] = pd.cut(
        df["resolution_time_days"],
        bins=[-1, 2, 5, 14, 100],
        labels=["Fast (0-2d)", "Moderate (3-5d)", "Slow (6-14d)", "Critical (>14d)"]
    )
    
    # 3. Risk Flag (External & Slow resolution)
    df["high_risk"] = (df["is_external_dependency"]) & (df["resolution_time_days"] >= 5)

    return df

@st.cache_data
def load_joined_sprint_data() -> pd.DataFrame:
    """
    Loads joined velocity + blocker dataset if available for correlation analysis.
    """
    possible_paths = [
        Path(__file__).resolve().parent.parent.parent / "output" / "sprint_blocker_joined.csv",
        Path("output/sprint_blocker_joined.csv"),
        Path("../output/sprint_blocker_joined.csv")
    ]
    for p in possible_paths:
        if p.exists():
            df = pd.read_csv(p)
            df["date_logged"] = pd.to_datetime(df["date_logged"], errors="coerce")
            df["is_external_dependency"] = df["is_external_dependency"].astype(bool)
            return df
    return pd.DataFrame()
