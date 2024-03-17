import feedparser
from newspaper import Article
import sqlite3
import schedule
import time
import json
import datetime
import logging

# Create a logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler = logging.FileHandler('error.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Define the RSS feed URL
rss_feed_url = "https://news.google.com/rss"

# Connect to the SQLite database
conn = sqlite3.connect("news_articles.db")
cursor = conn.cursor()

# Create a table to store the articles
cursor.execute("""
    CREATE TABLE IF NOT EXISTS articles (
        feed_id TEXT PRIMARY KEY,
        title TEXT,
        url TEXT,
        publish_date DATE,
        publisher TEXT,
        publisher_url TEXT
    )
""")

# Parse the RSS feed
feed = feedparser.parse(rss_feed_url)

def fetch_data():
    print('I am inini!!!')
    try:
        # Parse the RSS feed
        feed = feedparser.parse(rss_feed_url)
        # Save the feed to a JSON file
        with open('feed.json', 'w') as file:
            json.dump(feed, file)
        # Iterate over the entries in the feed
        for entry in feed.entries:
            print(entry.id)
            # Get the article URL
            article_url = entry.link

            # Check if the article is already in the database
            entry_check = cursor.execute("SELECT * FROM articles WHERE feed_id = ?", (entry.id,)).fetchone()
            if not entry_check:
                
                # AVL: Scrape the article content using newspaper4k
                # article = Article(article_url)
                # article.download()
                # article.parse()

                # Store the relevant information in the database
                try:
                    publish_date = datetime.datetime.strptime(entry.published, "%a, %d %b %Y %H:%M:%S %Z")
                    cursor.execute("""
                        INSERT INTO articles (feed_id,title, url,  publish_date, publisher, publisher_url)
                        VALUES (?, ?, ?,?, ?,?)
                    """, (entry.id,entry.title, entry.link,  publish_date, entry.source.title, entry.source.href))
                except Exception as e:
                    logger.error(e)
                    pass
        # Commit the changes and close the database connection
        conn.commit()
        # Generate the summary table
        generate_summary_table()
    except Exception as e:
        logger.error(e)

def generate_summary_table():
    try:
        # Query the database to get the count of articles published by each news publisher per hour
        cursor.execute("""
            SELECT strftime('%Y-%m-%d %H:00:00', publish_date) AS hour, publisher, COUNT(*) AS article_count
            FROM articles
            GROUP BY hour, publisher
        """)
        summary_data = cursor.fetchall()

        # Create a summary table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS summary (
                hour DATE,
                publisher TEXT,
                article_count INTEGER
            )
        """)

        # Insert the summary data into the summary table
        cursor.executemany("""
            INSERT INTO summary (hour, publisher, article_count)
            VALUES (?, ?, ?)
        """, summary_data)

        # Commit the changes
        conn.commit()
    except Exception as e:
        logger.error(e)
        pass

if __name__ == "__main__":
    fetch_data()
    
    # while True:
#         schedule.every(2).seconds.do(fetch_data)
# def schedule_fetch_data():
#     # Schedule the fetch_data function to run every hour

#     while True:
#         # Run the pending scheduled tasks
#         schedule.run_pending()
#         time.sleep(1)

# # Call the schedule_fetch_data function to start fetching data from the feed
# schedule_fetch_data()


