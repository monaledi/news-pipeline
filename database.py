import sqlite3


def create_database():
    connection = sqlite3.connect("news.db")
    cursor = connection.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS articles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        source TEXT,
        country TEXT,
        published_at TEXT,
        url TEXT UNIQUE)""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS fetch_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fetched_at TEXT,
        country TEXT,
        articles_fetched INTEGER,
        duplicates_skipped INTEGER)""")

    connection.commit()
    connection.close()


def insert_article(title, source, country, published_at, url):
    connection = sqlite3.connect("news.db")
    cursor = connection.cursor()

    try:
        cursor.execute("""INSERT INTO articles
        (title, source, country, published_at, url)
        VALUES (?, ?, ?, ?, ?)""", (title, source, country, published_at, url))

        connection.commit()

        return True

    except sqlite3.IntegrityError:

        return False

    finally:
        connection.close()


def log_fetch(fetched_at, country, articles_fetched, duplicates_skipped):

    connection = sqlite3.connect("news.db")
    cursor = connection.cursor()

    cursor.execute("""
    INSERT INTO fetch_logs
    (fetched_at, country, articles_fetched, duplicates_skipped)
    VALUES (?, ?, ?, ?)
    """, (
        fetched_at,
        country,
        articles_fetched,
        duplicates_skipped
    ))

    connection.commit()
    connection.close()