# News Pipeline

An automated news data pipeline built with Python, SQLite, and NewsAPI.  
The application fetches international news articles hourly, stores them in a local SQLite database, tracks duplicates, logs fetch activity, and generates detailed text reports.

---

## Features

- Fetches news articles from multiple countries using NewsAPI
- Stores articles in a local SQLite database
- Prevents duplicate articles using unique URLs
- Logs every fetch run with statistics
- Automatically generates reports
- Runs hourly using a scheduler
- Uses environment variables for configuration
- Modular project structure

---

## Technologies Used

- Python
- SQLite
- NewsAPI
- requests
- schedule
- python-dotenv

---

## Project Structure

```txt
news-pipeline/
│
├── reports/
│
├── main.py
├── fetcher.py
├── database.py
├── reporter.py
├── scheduler.py
│
├── news.db
├── requirements.txt
├── .env
├── .env.example
├── .gitignore
└── README.md
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/monaledi/news-pipeline
cd news-pipeline
```

Create and activate a virtual environment:

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Mac/Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## NewsAPI Setup

Create a free account at:

:contentReference[oaicite:0]{index=0}

Create a `.env` file in the project root:

```env
NEWS_API_KEY=your_api_key_here
COUNTRIES=United States,Germany,France,Italy,United Kingdom,Brazil,Russia,India,China,South Africa
```

---

## Running the Application

Start the hourly scheduler:

```bash
python main.py run
```

Generate a report manually:

```bash
python main.py report
```

---

## Database Schema

### articles

| Column | Type |
|---|---|
| id | INTEGER |
| title | TEXT |
| source | TEXT |
| country | TEXT |
| published_at | TEXT |
| url | TEXT UNIQUE |

---

### fetch_logs

| Column | Type |
|---|---|
| id | INTEGER |
| fetched_at | TEXT |
| country | TEXT |
| articles_fetched | INTEGER |
| duplicates_skipped | INTEGER |

---

## Reports

Reports are automatically generated after every scheduled pipeline run.

Reports are stored in the `reports/` folder.

Example report filename:

```txt
report_2026-05-25.txt
```

---

## Example Report Output

```txt
NEWS PIPELINE REPORT
====================

TOTAL ARTICLES STORED PER COUNTRY
---------------------------------
Germany: 125
India: 98
South Africa: 77

TOP 5 MOST RECENT HEADLINES PER COUNTRY
---------------------------------------

Germany
- Example headline
  Source: BBC News
  Published: 2026-05-25T18:30:00Z

LAST FETCH TIME PER COUNTRY
---------------------------
Germany: 2026-05-25 20:00:01

TOTAL DUPLICATES SKIPPED
------------------------
342
```

---

## Notes

The scheduler runs continuously until manually stopped using:

```txt
Ctrl + C
```

This project uses script-level scheduling via the `schedule` library.  
In production environments, a system service, cron job, Docker container, or orchestration tool such as n8n would typically be used instead.

---

## Future Improvements

- Add keyword-based article search
- Add category filtering
- Add CSV or PDF export support
- Add dashboards or visual analytics
- Add support for multiple news APIs