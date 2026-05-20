#!SECTION Import/callout libraries
import pandas as pd
import numpy as np
from datetime import datetime
import calendar
from pathlib import Path
# =========================
# FILE PATHS
# =========================
# Get the folder where this script lives
BASE_DIR = Path(__file__).parent
input_csv  = BASE_DIR / "exports" / "output_schedule_fixed.csv"
output_html = BASE_DIR / "exports" / "worldcup_dashboard.html"

# input_csv = r"N:/Parada A/9-Github Projects/worldcup/exports/output_schedule_fixed.csv"
# output_html = r"N:/Parada A/9-Github Projects/worldcup/exports/worldcup_dashboard.html"

# =========================
# READ CSV
# =========================
df = pd.read_csv(input_csv, dtype=str)
# =========================
# HTML HEADER
# =========================
html = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>World Cup 2026 Schedule</title>

<style>

body {
    background-color: #0f172a;
    color: white;
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 30px;
}

h1 {
    text-align: center;
    color: #38bdf8;
    margin-bottom: 40px;
}

.day-section {
    margin-bottom: 40px;
}

.day-title {
    font-size: 28px;
    margin-bottom: 20px;
    color: #facc15;
    border-bottom: 2px solid #334155;
    padding-bottom: 10px;
}

.game-card {
    background-color: #1e293b;
    border-radius: 14px;
    padding: 18px;
    margin-bottom: 15px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.4);
    transition: transform 0.2s ease;
}

.game-card:hover {
    transform: scale(1.02);
}

.late-game {
    border-left: 8px solid #ef4444;
    background-color: #3b1d1d;
}

.match-title {
    font-size: 22px;
    font-weight: bold;
    margin-bottom: 8px;
}

.game-info {
    color: #cbd5e1;
    margin-top: 5px;
}

.highlight {
    color: #f87171;
    font-weight: bold;
    margin-top: 10px;
}

.location {
    color: #94a3b8;
    margin-top: 8px;
    font-size: 14px;
}

</style>
</head>
<body>

<h1>⚽ FIFA World Cup 2026 Schedule</h1>
<h1> brought to you by ALDO </h1>
"""
# =========================
# SORT BY REAL DATE
# =========================

# Convert edt_time into actual datetime for sorting
df["sort_datetime"] = pd.to_datetime(
    df["edt_time"].str.replace(", at ", " ", regex=False) + " 2026",
    format="%A, %B %d %I:%M %p %Y"
)
# Sort entire dataframe chronologically

df = df.sort_values(by="sort_datetime")
# =========================
# GROUP BY ACTUAL DATE
# =========================

# This fixes the issue where:
# Friday games from different weeks were grouped together.
# Now every real calendar date gets its own section.

for game_date, games in df.groupby(df["sort_datetime"].dt.date):

    formatted_date = pd.Timestamp(game_date).strftime(
        "%A, %B %d, %Y"
    )

    html += f'<div class="day-section">'
    html += f'<div class="day-title">{formatted_date}</div>'

    for _, row in games.iterrows():

        late_class = "late-game" if row["after_4pm_pt"] == "True" else ""

        html += f'''
        <div class="game-card {late_class}">

            <div class="match-title">
                Match {row['Match']} — {row['Team_1']} vs {row['Team_2']}
            </div>

            <div class="game-info">
                🕒 {row['pt_time']} PT
            </div>

            <div class="game-info">
                📍 {row['Location']}
            </div>

            <div class="game-info">
                🏆 {row['Stage']}
            </div>
        '''

        if row["highlight"]:
            html += f'''
            <div class="highlight">
                {row['highlight']}
            </div>
            '''

        html += '</div>'

    html += '</div>'

# =========================
# HTML FOOTER
# =========================
html += """
</body>
</html>
"""
# =========================
# WRITE HTML FILE
# =========================
with open(output_html, "w", encoding="utf-8") as f:
    f.write(html)

print(f"\nDashboard created:\n{output_html}")
# =========================
# OPTIONAL AUTO OPEN
# =========================
import webbrowser
webbrowser.open(Path(output_html).as_uri())
