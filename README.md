## Pint AI - Google RSS Scraper & API

Built using Python - Flask & Newspaper & SQLite

Create a virtual environment

`python -m venv ENV`

For Windows:
`ENV/Scripts/activate`

For Unix or Linux:
`ENV/bin/activate`

Install required packages
`pip install -r requirement.txt`

### Retrieve articles from the SQLite database based on specified filters.

Returns:
A JSON response containing a list of articles matching the filters.

Query Parameters:
- title (str): Filter articles by title (optional).
- url (str): Filter articles by URL (optional).
- limit (int): Limit the number of articles returned (default: 10).
- publish_date (str): Filter articles by publish date (optional).
- publisher (str): Filter articles by publisher (optional).

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


### Retrieves summary articles from the SQLite database based on the provided filters.

Parameters:
- hour (str): Optional. Filter articles by hour.
- publisher (str): Optional. Filter articles by publisher.
- limit (int): Optional. Limit the number of articles to retrieve. Default is 10.

Returns:
- list: A list of dictionaries representing the summary articles.
    Each dictionary contains the following keys:
    - hour (str): The hour of the article.
    - publisher (str): The publisher of the article.
    - count (int): The count of articles for the given hour and publisher.
