import requests
from datetime import datetime

from database import insert_article, log_fetch


NEWS_API_URL = "https://newsapi.org/v2/everything"

#builds parameters for the query
def build_params(api_key, country_name):
    return {
        "q": country_name,
        "language": "en",
        "sortBy": "publishedAt",
        "apiKey": api_key
    }


#sends request to newsAPI
def get_articles(api_key, country_name):

    try:
        response = requests.get(
            NEWS_API_URL,
            params=build_params(api_key, country_name),
            timeout=60
        )

        data = response.json()

    except requests.RequestException as error:
        print("Request failed:", error)
        return []

    
    if data.get("status") != "ok":
        print("API error:", data.get("message"))
        return []

    return data.get("articles", [])


#saves the articles fetched into the databse and counts saved and dupes
def save_articles(articles, country_name):
    saved_count = 0
    duplicate_count = 0

    for article in articles:
        title = article["title"]
        source = article["source"]["name"]
        published_at = article["publishedAt"]
        url = article["url"]

        print(title)

        was_saved = insert_article(title, source, country_name, published_at, url)

        if was_saved:
            saved_count += 1
        else:
            duplicate_count += 1

    return saved_count, duplicate_count

#main fetch function for each country, fetches, saves and logs results
def fetch_news(api_key, country_name):
    print(f"\n--- {country_name} ---")

    articles = get_articles(api_key, country_name)

    saved_count, duplicate_count = save_articles(articles, country_name)

    log_fetch(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), country_name, saved_count, duplicate_count)

    print(f"Saved: {saved_count}")
    print(f"Duplicates: {duplicate_count}")