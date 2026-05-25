import os
import sqlite3
from datetime import date

#function that generates reports in a sub folder it creates called reports
def generate_report():
    conn = sqlite3.connect("news.db")
    cursor = conn.cursor()

    report_lines = []

    report_lines.append("NEWS PIPELINE REPORT")
    report_lines.append("====================\n")

    add_total_articles(cursor, report_lines)
    add_recent_headlines(cursor, report_lines)
    add_last_fetch_times(cursor, report_lines)
    add_duplicate_count(cursor, report_lines)

    conn.close()

    report_text = "\n".join(report_lines)

    print(report_text)

    os.makedirs("reports", exist_ok=True)

    filename = f"reports/report_{date.today()}.txt"

    with open(filename, "w", encoding="utf-8") as file:
        file.write(report_text)

    print(f"\nReport saved as {filename}")


#function that gets total articles saved per country
def add_total_articles(cursor, report_lines):
    report_lines.append("TOTAL ARTICLES STORED PER COUNTRY")
    report_lines.append("---------------------------------")

    cursor.execute("""SELECT country, COUNT(*)
    FROM articles
    GROUP BY country
    ORDER BY country""")

    rows = cursor.fetchall()

    if not rows:
        report_lines.append("No articles stored yet.\n")
        return

    for country, total in rows:
        report_lines.append(f"{country}: {total}")

    report_lines.append("")


#function that adds top 5 most recent headlines per country
def add_recent_headlines(cursor, report_lines):
    report_lines.append("TOP 5 MOST RECENT HEADLINES PER COUNTRY")
    report_lines.append("---------------------------------------")

    cursor.execute("""
    SELECT DISTINCT country
    FROM articles
    ORDER BY country
    """)

    countries = cursor.fetchall()

    if not countries:
        report_lines.append("No headlines available yet.\n")
        return

    for country_row in countries:
        country = country_row[0]

        report_lines.append(f"\n{country}")

        cursor.execute("""SELECT title, source, published_at
        FROM articles
        WHERE country = ?
        ORDER BY published_at DESC
        LIMIT 5""", (country,))

        headlines = cursor.fetchall()

        for title, source, published_at in headlines:
            report_lines.append(f"- {title}")
            report_lines.append(f"  Source: {source}")
            report_lines.append(f"  Published: {published_at}")

    report_lines.append("")


#function that says last fetch time for each country
def add_last_fetch_times(cursor, report_lines):
    report_lines.append("LAST FETCH TIME PER COUNTRY")
    report_lines.append("---------------------------")

    cursor.execute("""SELECT country, MAX(fetched_at)
    FROM fetch_logs
    GROUP BY country
    ORDER BY country""")

    rows = cursor.fetchall()

    if not rows:
        report_lines.append("No fetch logs available yet.\n")
        return

    for country, last_fetch in rows:
        report_lines.append(f"{country}: {last_fetch}")

    report_lines.append("")


#function that keeps track of duplicates skipped
def add_duplicate_count(cursor, report_lines):
    report_lines.append("TOTAL DUPLICATES SKIPPED")
    report_lines.append("------------------------")

    cursor.execute("""SELECT SUM(duplicates_skipped)
    FROM fetch_logs""")

    total_duplicates = cursor.fetchone()[0] or 0

    report_lines.append(str(total_duplicates))