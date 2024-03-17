import feedparser
from newspaper import Article
import sqlite3
import schedule
import time
from flask import Flask, jsonify, request
import sqlite3


app = Flask(__name__)

# Define the route for querying articles
@app.route('/summary', methods=['GET'])
def get_summary_articles():
    """
    Retrieves summary articles from the SQLite database based on the provided filters.

    Parameters:
        hour (str): Optional. Filter articles by hour.
        publisher (str): Optional. Filter articles by publisher.
        limit (int): Optional. Limit the number of articles to retrieve. Default is 10.

    Returns:
        list: A list of dictionaries representing the summary articles.
            Each dictionary contains the following keys:
                - hour (str): The hour of the article.
                - publisher (str): The publisher of the article.
                - count (int): The count of articles for the given hour and publisher.
    """

    # Connect to the SQLite database
    conn = sqlite3.connect("news_articles.db")
    cursor = conn.cursor()

    # Get the query parameters for filtering
    hour = request.args.get('hour')
    publisher = request.args.get('publisher')
    limit = request.args.get('limit') or 10

    # Build the SQL query based on the filters
    query = "SELECT * FROM summary WHERE 1=1"
    params = []

    if hour:
        query += " AND hour = ?"
        params.append(hour)

    if publisher:
        query += " AND publisher = ?"
        params.append(publisher)

    query += " LIMIT ?"
    params.append(limit)

    # Execute the query with the filters
    cursor.execute(query, params)
    summary_articles = cursor.fetchall()

    # Close the database connection
    conn.close()

    # Convert the summary articles to a list of dictionaries
    summary_articles_list = []
    for article in summary_articles:
        article_dict = {
            'hour': article[0],
            'publisher': article[1],
            'count': article[2]
        }
        summary_articles_list.append(article_dict)

    # Return the summary articles as JSON response
    return jsonify(summary_articles_list)

@app.route('/articles', methods=['GET'])
def get_articles():
    """
    Retrieve articles from the SQLite database based on specified filters.

    Returns:
        A JSON response containing a list of articles matching the filters.

    Query Parameters:
        title (str): Filter articles by title (optional).
        url (str): Filter articles by URL (optional).
        limit (int): Limit the number of articles returned (default: 10).
        publish_date (str): Filter articles by publish date (optional).
        publisher (str): Filter articles by publisher (optional).

    Example Usage:
        To retrieve articles with a specific title:
        GET /articles?title=example_title

        To retrieve articles with a specific URL:
        GET /articles?url=example_url

        To retrieve articles with a specific publisher:
        GET /articles?publisher=example_publisher

        To retrieve articles published on a specific date:
        GET /articles?publish_date=yyyy-mm-dd

        To retrieve a limited number of articles:
        GET /articles?limit=5
    """
 
    # Connect to the SQLite database
    conn = sqlite3.connect("news_articles.db")
    cursor = conn.cursor()

    # Get the query parameters for filtering
    title = request.args.get('title')
    url = request.args.get('url')
    limit = request.args.get('limit') or 10
    publish_date = request.args.get('publish_date')  # Add publish_date parameter
    publisher = request.args.get('publisher')  # Add publish_date parameter

    # Build the SQL query based on the filters
    query = "SELECT * FROM articles WHERE 1=1"
    params = []

    if title:
        query += " AND title LIKE ?"
        params.append(f"%{title}%")

    if publisher:
        query += " AND publisher LIKE ?"
        params.append(f"%{publisher}%")

    if url:
        query += " AND url LIKE ?"
        params.append(f"%{url}%")

    if publish_date:  # Add filter for publish_date
        publish_date = publish_date.split(' ')[0]
        start_publish_date = f"{publish_date} 00:00:00"  # Add date start time component
        end_publish_date = f"{publish_date} 23:59:59"
        query += " AND publish_date BETWEEN ? AND ?"  # Modify the query to include the date range
        params.append(start_publish_date)
        params.append(end_publish_date)

    query += " LIMIT ?"  # Add limit clause to the query
    params.append(limit)

    # Execute the query with the filters
    cursor.execute(query, params)
    articles = cursor.fetchall()

    # Close the database connection
    conn.close()

    # Convert the articles to a list of dictionaries
    articles_list = []
    for article in articles:
        article_dict = {
            'feed_id': article[0],
            'title': article[1],
            'url': article[2],
            'publish_date': article[3],
            'publisher': article[4],
            'publisher_url': article[5]
        }
        articles_list.append(article_dict)

    # Return the articles as JSON response
    return jsonify(articles_list)



if __name__ == '__main__':
    app.run(debug=True)