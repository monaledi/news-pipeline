from dotenv import load_dotenv
import os

from database import create_database
from fetcher import fetch_news


load_dotenv()


def main():

    api_key = os.getenv("NEWS_API_KEY")

    countries = os.getenv("COUNTRIES").split(",")

    create_database()

    for country_name in countries:
        fetch_news(api_key, country_name)


if __name__ == "__main__":
    main()