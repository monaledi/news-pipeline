from dotenv import load_dotenv
import os
import sys

from database import create_database
from scheduler import start_scheduler
from reporter import generate_report


load_dotenv()


def main():

    api_key = os.getenv("NEWS_API_KEY")

    countries = os.getenv("COUNTRIES").split(",")

    create_database()

    if len(sys.argv) < 2:
        print("Usage:\npython main.py run\npython main.py report")
        return

    command = sys.argv[1]

    if command == "run":
        start_scheduler(api_key, countries)

    elif command == "report":
        generate_report()

    else:
        print("Unkown command\nAvailable commands:\npython main.py run\npython main.py report")


if __name__ == "__main__":
    main()