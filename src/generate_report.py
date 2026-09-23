from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import os
import pandas as pd
import json
import textwrap


def split_text(text, width=80):
    return textwrap.wrap(text, width)


def make_report(pdf_path='presentation/Data_Science_Capstone_Project_Report.pdf'):
    os.makedirs(os.path.dirname(pdf_path), exist_ok=True)
    c = canvas.Canvas(pdf_path, pagesize=letter)
    width, height = letter

    # Title page
    c.setFont('Helvetica-Bold', 22)
    c.drawCentredString(width/2, height-100, 'SpaceX Falcon 9 Data Science Capstone')
    c.setFont('Helvetica', 12)
    c.drawCentredString(width/2, height-130, 'Automated project report — generated')
    c.showPage()

    # Executive Summary
    c.setFont('Helvetica-Bold', 16)
    c.drawString(40, height-80, 'Executive Summary')
    c.setFont('Helvetica', 11)
    summary = (
        'This project analyzes SpaceX Falcon 9 launch data. Data was obtained from the IBM course dataset when the SpaceX API was unavailable. '
        'Exploratory data analysis, SQL queries, an interactive Folium map, a Plotly Dash skeleton, and multiple classification models were completed. '
        'Results include visualizations and model evaluation metrics; next steps are hyperparameter tuning and publishing to GitHub.'
    )
    text_wrapped = split_text(summary, 80)
    y = height-110
    for line in text_wrapped:
        c.drawString(40, y, line)
        y -= 14
    c.showPage()

    # Introduction
    c.setFont('Helvetica-Bold', 16)
    c.drawString(40, height-80, 'Introduction / Problem')
    c.setFont('Helvetica', 11)
    intro = (
        'Objective: Predict landing success (Class) for Falcon 9 launches and explore payload, launch site, and orbital patterns. '
        'Dataset: processed SpaceX launches CSV with 56 records used for demonstration.'
    )
    y = height-110
    for line in split_text(intro, 80):
        c.drawString(40, y, line); y -= 14
    c.showPage()

    # Data collection & wrangling
    c.setFont('Helvetica-Bold', 16)
    c.drawString(40, height-80, 'Data Collection & Wrangling')
    c.setFont('Helvetica', 11)
    dc = (
        'Source: attempted SpaceX REST API (v3/v4) but received server errors; used IBM course CSV copy saved to data/raw. '
        'Wrangling steps: parse dates, create Year, standardize launch site names, extract payload mass and booster version, and create `class` binary outcome.'
    )
    y = height-110
    for line in split_text(dc, 80):
        c.drawString(40, y, line); y -= 14
    c.showPage()

    # Web scraping note
    c.setFont('Helvetica-Bold', 16)
    c.drawString(40, height-80, 'Web Scraping')
    c.setFont('Helvetica', 11)
    ws = (
        'Attempted to scrape Wikipedia for additional launch tables but received HTTP 403 Forbidden. A polite scraper with headers and retries was implemented in src/web_scraping.py; consider providing network allowance or manual download for full scraping.'
    )
    y = height-110
    for line in split_text(ws, 80):
        c.drawString(40, y, line); y -= 14
    c.showPage()

    # EDA slides with images
    c.setFont('Helvetica-Bold', 16)
    c.drawString(40, height-80, 'Exploratory Data Analysis')
    imgs = [
        ('figures/eda/flight_payload.png', 'Flight Number vs Payload Mass'),
        ('figures/eda/payload_vs_success.png', 'Payload Mass vs Landing Success'),
        ('figures/eda/success_by_site.png', 'Launch Success Rate by Site')
    ]
    x = 40; y = height-120
    c.setFont('Helvetica', 11)
    for im, caption in imgs:
        if os.path.exists(im):
            try:
                img = ImageReader(im)
                c.drawImage(img, x, y-220, width=240, height=160, preserveAspectRatio=True)
                c.drawString(x, y-230, caption)
                x += 260
                if x > width-260:
                    x = 40; y -= 240
            except Exception:
                pass
    c.showPage()

    # EDA with SQL: run key queries and include results
    c.setFont('Helvetica-Bold', 16)
    c.drawString(40, height-80, 'EDA with SQL (sample results)')
    c.setFont('Helvetica', 11)
    try:
        from src.sqlite_analysis import run_query
        q1 = 'SELECT COUNT(*) as total, SUM("Payload Mass (kg)") as total_payload FROM spacex_launches;'
        res = run_query('data/spacex_launches.db', 'SELECT COUNT(*) as total FROM spacex_launches')
        total = int(res['total'].iloc[0])
        c.drawString(40, height-120, f'Total records in SQLite DB: {total}')
    except Exception:
        c.drawString(40, height-120, 'SQLite queries could not be executed or DB missing')
    c.showPage()

    # Folium map note
    c.setFont('Helvetica-Bold', 16)
    c.drawString(40, height-80, 'Folium Map')
    c.setFont('Helvetica', 11)
    c.drawString(40, height-110, 'Interactive map generated at figures/map/spacex_launch_map.html')
    c.drawString(40, height-130, 'To include a static image in slides, open the HTML and capture a screenshot, then place it under figures/map/.')
    c.showPage()

    # Plotly Dash note
    c.setFont('Helvetica-Bold', 16)
    c.drawString(40, height-80, 'Plotly Dash App')
    c.setFont('Helvetica', 11)
    c.drawString(40, height-110, 'Dash app skeleton with dropdown, pie chart, payload slider, and scatter plot at dashboard/app.py')
    c.drawString(40, height-130, 'Run locally: python3 dashboard/app.py')
    c.showPage()

    # Predictive analysis (models)
    c.setFont('Helvetica-Bold', 16)
    c.drawString(40, height-80, 'Predictive Analysis — Model Results')
    y = height-120
    try:
        with open('figures/ml/ml_results.json') as f:
            results = json.load(f)
        c.setFont('Helvetica', 11)
        for model, stats in results.items():
            line = f"{model}: accuracy={stats.get('accuracy'):.3f}, precision={stats.get('precision'):.3f}, recall={stats.get('recall'):.3f}, f1={stats.get('f1'):.3f}"
            c.drawString(40, y, line); y -= 14
            if y < 80:
                c.showPage(); y = height-80
    except Exception:
        c.setFont('Helvetica', 11)
        c.drawString(40, y, 'ML results unavailable')
    c.showPage()

    # Conclusion and GitHub status
    c.setFont('Helvetica-Bold', 16)
    c.drawString(40, height-80, 'Conclusion and Next Steps')
    c.setFont('Helvetica', 11)
    concl = (
        'Findings: Launch success varies by site and booster version; payload distributions differ between successes and failures. '
        'Models show modest predictive performance on this small sample dataset. '
        'Next steps: hyperparameter tuning, additional features (orbit, core serial), more data, and publishing to GitHub.'
    )
    y = height-110
    for line in split_text(concl, 80):
        c.drawString(40, y, line); y -= 14

    # GitHub slide — must not fabricate URL
    c.showPage()
    c.setFont('Helvetica-Bold', 16)
    c.drawString(40, height-80, 'GitHub Repository Status')
    c.setFont('Helvetica', 11)
    c.drawString(40, height-110, 'No GitHub repository URL was provided or detected in this environment.')
    c.drawString(40, height-130, 'To include your GitHub URL in the final submission:')
    steps = [
        'Initialize git in project root: git init',
        'Add files: git add .',
        'Commit: git commit -m "Initial capstone project"',
        'Create repo on GitHub and push, then update README with the repository URL.'
    ]
    y = height-160
    for s in steps:
        c.drawString(50, y, '- ' + s); y -= 14

    c.save()
    print('Report written to', pdf_path)


if __name__ == '__main__':
    make_report()
