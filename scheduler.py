import schedule
import time

from fetcher import fetch_news
from reporter import generate_report


#runs the the full project
def run_pipeline(api_key, countries):
    print("\nStarting news fetch...")

    for country_name in countries:
        fetch_news(api_key, country_name)

    print("\nNews fetch complete. Next fetch in an hour")
    print("Waiting for next scheduled run...")
    print("Press Ctrl+C to stop.")

    generate_report()
    print("Report generated.")
    print("Waiting for next scheduled run...")


#starts the hourly scheduler so news gets fetched every  hour
def start_scheduler(api_key, countries):
    schedule.every(1).hours.do(run_pipeline, api_key, countries)

    print("Scheduler started.")
    print("Pipeline will run once every hour.")
    print("Press Ctrl+C to stop.")

    run_pipeline(api_key, countries)

    try:
        while True:
            schedule.run_pending()
            time.sleep(1)

    except KeyboardInterrupt:   
        print("\nScheduler stopped.")