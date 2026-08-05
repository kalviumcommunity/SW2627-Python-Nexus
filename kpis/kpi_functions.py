import pandas as pd
import numpy as np


# =====================================================
# Helper Function
# =====================================================

def prepare_dataset(df):
    """
    Prepare dataset by converting date columns and creating
    Resolution Hours and First Response Hours if not present.
    """

    df = df.copy()

    # Convert dates
    df["Created Time (Ticket)"] = pd.to_datetime(
        df["Created Time (Ticket)"],
        format="%d-%m-%Y %H:%M",
        errors="coerce"
    )

    df["Ticket Closed Time"] = pd.to_datetime(
        df["Ticket Closed Time"],
        format="%d-%m-%Y %H:%M",
        errors="coerce"
    )

    df["First Response Time"] = pd.to_datetime(
        df["First Response Time"],
        format="%d-%m-%Y %H:%M",
        errors="coerce"
    )

    # Resolution Hours
    if "Resolution Hours" not in df.columns:

        df["Resolution Hours"] = (
            df["Ticket Closed Time"] -
            df["Created Time (Ticket)"]
        ).dt.total_seconds() / 3600

    # First Response Hours
    if "First Response Hours" not in df.columns:

        df["First Response Hours"] = (
            df["First Response Time"] -
            df["Created Time (Ticket)"]
        ).dt.total_seconds() / 3600

    return df


# =====================================================
# KPI 1
# =====================================================

def calculate_total_tickets(df):

    return int(df["Ticket Id"].nunique())


# =====================================================
# KPI 2
# =====================================================

def calculate_closed_ticket_rate(df):

    total = len(df)

    closed = df["Ticket Closed Time"].notna().sum()

    if total == 0:
        return 0

    return round((closed / total) * 100, 2)


# =====================================================
# KPI 3
# =====================================================

def calculate_average_resolution_time(df):

    df = prepare_dataset(df)

    return round(
        df["Resolution Hours"].mean(),
        2
    )


# =====================================================
# KPI 4
# =====================================================

def calculate_average_first_response(df):

    df = prepare_dataset(df)

    return round(
        df["First Response Hours"].mean(),
        2
    )


# =====================================================
# KPI 5
# =====================================================

def calculate_active_programs(df):

    return int(
        df["Program Name"].nunique()
    )


# =====================================================
# KPI 6
# =====================================================

def calculate_active_students(df):

    return int(
        df["Student or WP"].nunique()
    )


# =====================================================
# KPI 7
# =====================================================

def calculate_ticket_status_distribution(df):

    return (
        df["Status (Ticket)"]
        .value_counts()
    )


# =====================================================
# KPI 8
# =====================================================

def calculate_project_phase_distribution(df):

    return (
        df["Project Phase"]
        .value_counts()
    )


# =====================================================
# KPI 9
# =====================================================

def calculate_average_ticket_health(df):

    if "Ticket Health Score" not in df.columns:
        return np.nan

    return round(
        df["Ticket Health Score"].mean(),
        2
    )


# =====================================================
# KPI 10
# =====================================================

def calculate_open_ticket_rate(df):

    total = len(df)

    open_tickets = (
        df["Ticket Closed Time"]
        .isna()
        .sum()
    )

    if total == 0:
        return 0

    return round(
        (open_tickets / total) * 100,
        2
    )


# =====================================================
# Compute All KPIs
# =====================================================

def calculate_all_kpis(df):

    return {

        "Total Tickets":
            calculate_total_tickets(df),

        "Closed Ticket Rate (%)":
            calculate_closed_ticket_rate(df),

        "Average Resolution Time (Hours)":
            calculate_average_resolution_time(df),

        "Average First Response Time (Hours)":
            calculate_average_first_response(df),

        "Average Ticket Health Score":
            calculate_average_ticket_health(df),

        "Active Programs":
            calculate_active_programs(df),

        "Active Students":
            calculate_active_students(df),

        "Open Ticket Rate (%)":
            calculate_open_ticket_rate(df)

    }