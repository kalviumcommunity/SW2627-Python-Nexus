import os
from datetime import datetime
import pandas as pd
import markdown


def export_analysis(
        df,
        summary_text,
        charts_dict,
        output_dir="output"
):
    """
    Export Remote Work Blocker Analysis.

    Generates:
    1. CSV dataset
    2. PDF executive report
    3. Interactive HTML dashboard
    4. Metadata README

    """


    timestamp = datetime.now().strftime(
        "%Y-%m-%d_%H%M"
    )


    report_dir = os.path.join(
        output_dir,
        f"{timestamp}_analysis"
    )


    os.makedirs(
        report_dir,
        exist_ok=True
    )


    # =====================================================
    # 1. CSV Export
    # =====================================================


    csv_path = os.path.join(
        report_dir,
        "cleaned_blockers.csv"
    )


    df.to_csv(
        csv_path,
        index=False
    )


    print(
        "CSV created:",
        csv_path
    )



    # =====================================================
    # 2. HTML Report
    # =====================================================


    html_path = os.path.join(
        report_dir,
        "interactive_report.html"
    )


    html = f"""

    <html>

    <head>

    <title>
    Remote Work Blocker Analysis
    </title>


    <style>

    body {{
        font-family: Arial;
        margin:40px;
    }}

    h1 {{
        color:#2563eb;
    }}


    </style>


    </head>


    <body>


    <h1>
    Remote Work Blocker Report
    </h1>


    <h2>
    Executive Summary
    </h2>


    {markdown.markdown(summary_text)}


    """


    for name, fig in charts_dict.items():

        html += f"""

        <h2>
        {name}
        </h2>

        {fig.to_html(
            include_plotlyjs='cdn'
        )}

        """



    html += """

    </body>

    </html>

    """



    with open(
        html_path,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(html)



    print(
        "HTML created:",
        html_path
    )



    # =====================================================
    # 3. PDF Export
    # =====================================================


    try:

        from weasyprint import HTML


        pdf_path = os.path.join(
            report_dir,
            "blocker_report.pdf"
        )


        HTML(
            string=html
        ).write_pdf(
            pdf_path
        )


        print(
            "PDF created:",
            pdf_path
        )


    except Exception as e:

        print(
            "PDF generation failed:",
            e
        )



    # =====================================================
    # 4. Metadata
    # =====================================================


    metadata_path = os.path.join(
        report_dir,
        "README.md"
    )


    with open(
        metadata_path,
        "w",
        encoding="utf-8"
    ) as f:


        f.write(
f"""
# Remote Work Blocker Analysis Export


## Generated

{datetime.now()}


## Dataset Information


Rows:
{len(df)}


Columns:

{list(df.columns)}



## Files Generated


### cleaned_blockers.csv

Contains processed blocker records.


Use:
- Excel analysis
- Filtering
- Pivot tables



### blocker_report.pdf

Executive summary report.


Use:
- Management meetings
- Presentations



### interactive_report.html

Interactive charts.

Use:
- Browser exploration
- Sharing with stakeholders



Refresh:

Generated automatically.


"""
        )



    return report_dir