from datetime import datetime
import pandas as pd

def generate_report(df: pd.DataFrame, report_date=None) -> str:
    """
    Generates a structured text report containing:
    1. KPI Summary
    2. Key Finding
    3. Recommended Action
    """
    if report_date is None:
        report_date = datetime.now().strftime("%Y-%m-%d")

    total_records = len(df)
    
    # Identify relevant columns dynamically
    status_col = "Status (Ticket)" if "Status (Ticket)" in df.columns else ("status" if "status" in df.columns else None)
    prog_col = "Program Name" if "Program Name" in df.columns else ("segment" if "segment" in df.columns else None)
    rev_col = "revenue" if "revenue" in df.columns else None

    lines = []
    lines.append("==========================================")
    lines.append("        WEEKLY ANALYTICS REPORT           ")
    lines.append("==========================================")
    lines.append(f"Date Generated: {report_date}")
    lines.append("")
    lines.append("== KPI SUMMARY ==")
    lines.append(f"Total Records Evaluated: {total_records:,}")

    if rev_col:
        revenue = df[rev_col].sum()
        avg_order = df[rev_col].mean()
        lines.append(f"Total Revenue: ${revenue:,.2f}")
        lines.append(f"Average Order Value: ${avg_order:,.2f}")

    if status_col:
        open_cnt = df[status_col].astype(str).str.contains("Open", case=False, na=False).sum()
        closed_cnt = df[status_col].astype(str).str.contains("Closed", case=False, na=False).sum()
        lines.append(f"Open Tickets: {open_cnt:,}")
        lines.append(f"Closed Tickets: {closed_cnt:,}")
        if total_records > 0:
            lines.append(f"Resolution Rate: {(closed_cnt / total_records * 100):.1f}%")

    lines.append("")
    lines.append("== KEY FINDING ==")
    if prog_col and not df[prog_col].dropna().empty:
        top_seg = df[prog_col].value_counts().idxmax()
        top_count = df[prog_col].value_counts().max()
        pct = (top_count / total_records * 100) if total_records > 0 else 0
        lines.append(f"Highest Activity Category: '{top_seg}' ({top_count:,} items, representing {pct:.1f}% of volume).")
    else:
        lines.append("High volume concentration observed across top active segments.")

    lines.append("")
    lines.append("== RECOMMENDED ACTION ==")
    lines.append("1. Reallocate operational support resources to top active categories.")
    lines.append("2. Prioritize unresolved open items exceeding SLA thresholds.")
    lines.append("==========================================")

    return "\n".join(lines)