import pandas as pd

# Excel file
EXCEL_FILE = "Combined_Data.xlsx"


def analyze_support_tickets(file_path):
    print("=" * 60)
    print("1. SUPPORT TICKETS ANALYSIS")
    print("=" * 60)

    try:
        df = pd.read_excel(file_path, sheet_name="Support Tickets")
    except Exception as e:
        print(f"Error reading Support Tickets sheet: {e}")
        return

    required_columns = [
        "Created Time (Ticket)",
        "Ticket Closed Time",
        "First Response Time",
        "Status (Ticket)",
        "Program Name",
        "Project Phase",
    ]

    missing = [col for col in required_columns if col not in df.columns]

    if missing:
        print("Missing columns:")
        print(missing)
        return

    # Convert datetime columns
    for col in [
        "Created Time (Ticket)",
        "Ticket Closed Time",
        "First Response Time",
    ]:
        df[col] = pd.to_datetime(df[col], errors="coerce")

    # Calculate time differences
    df["Resolution_Time_Hrs"] = (
        df["Ticket Closed Time"] - df["Created Time (Ticket)"]
    ).dt.total_seconds() / 3600

    df["First_Response_Hrs"] = (
        df["First Response Time"] - df["Created Time (Ticket)"]
    ).dt.total_seconds() / 3600

    total_tickets = len(df)

    if total_tickets == 0:
        print("No data found.")
        return

    closed_resolved = df["Status (Ticket)"].isin(
        ["Closed", "Resolved"]
    ).sum()

    duplicate_count = (
        df["Status (Ticket)"] == "Duplicate"
    ).sum()

    print(f"Total Support Tickets        : {total_tickets}")
    print(
        f"Resolution Rate             : {(closed_resolved / total_tickets) * 100:.2f}%"
    )
    print(
        f"Duplicate Rate              : {(duplicate_count / total_tickets) * 100:.2f}%"
    )

    print(
        f"Median First Response Time  : {df['First_Response_Hrs'].median():.2f} hours"
    )
    print(
        f"Mean First Response Time    : {df['First_Response_Hrs'].mean():.2f} hours"
    )
    print(
        f"Median Resolution Time      : {df['Resolution_Time_Hrs'].median():.2f} hours"
    )
    print(
        f"Mean Resolution Time        : {df['Resolution_Time_Hrs'].mean():.2f} hours"
    )

    print("\nTickets by Program")
    print(df["Program Name"].value_counts())

    print("\nTop 5 Project Phases")
    print(df["Project Phase"].value_counts().head(5))


def analyze_jira_issues(file_path):
    print("\n" + "=" * 60)
    print("2. JIRA ENGINEERING ANALYSIS")
    print("=" * 60)

    try:
        df = pd.read_excel(file_path, sheet_name="Jira Issues")
    except Exception as e:
        print(f"Error reading Jira Issues sheet: {e}")
        return

    required_columns = [
        "storyPoint",
        "issueType",
        "assignee",
    ]

    missing = [col for col in required_columns if col not in df.columns]

    if missing:
        print("Missing columns:")
        print(missing)
        return

    df["storyPoint"] = pd.to_numeric(
        df["storyPoint"], errors="coerce"
    )

    total_issues = len(df)

    if total_issues == 0:
        print("No data found.")
        return

    print(f"Total Jira Issues           : {total_issues}")
    print(
        f"Total Story Points          : {df['storyPoint'].sum():.0f}"
    )
    print(
        f"Average Story Points        : {df['storyPoint'].mean():.2f}"
    )

    print("\nIssue Type Distribution")
    print(df["issueType"].value_counts())

    print("\nTop 5 Assignees")
    print(df["assignee"].value_counts().head(5))


def analyze_survey_responses(file_path):
    print("\n" + "=" * 60)
    print("3. SURVEY RESPONSES ANALYSIS")
    print("=" * 60)

    try:
        df = pd.read_excel(file_path, sheet_name="Survey Responses")
    except Exception as e:
        print(f"Error reading Survey Responses sheet: {e}")
        return

    total = len(df)

    if total == 0:
        print("No survey responses found.")
        return

    print(f"Total Survey Responses      : {total}")

    gender_col = "What is your gender?"

    if gender_col in df.columns:
        print("\nGender Distribution")
        print(df[gender_col].value_counts(dropna=False))

    productivity_cols = [
        col
        for col in df.columns
        if "Roughly how productive are you" in col
    ]

    if productivity_cols:
        print("\nRemote Productivity Perception")
        print(df[productivity_cols[0]].value_counts())

    else:
        print("\nProductivity column not found.")


def main():
    try:
        analyze_support_tickets(EXCEL_FILE)
        analyze_jira_issues(EXCEL_FILE)
        analyze_survey_responses(EXCEL_FILE)

    except FileNotFoundError:
        print(f"File '{EXCEL_FILE}' not found.")

    except Exception as e:
        print("Unexpected Error:", e)


if __name__ == "__main__":
    main()