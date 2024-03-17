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

API will run on `localhost:5000` 

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
`GET` `/articles?title=example_title`

To retrieve articles with a specific URL:
`GET` `/articles?url=example_url`

To retrieve articles with a specific publisher:
`GET` `/articles?publisher=example_publisher`

To retrieve articles published on a specific date:
`GET` `/articles?publish_date=yyyy-mm-dd`

To retrieve a limited number of articles:
`GET` `/articles?limit=5`


### Retrieves summary articles from the SQLite database based on the provided filters.

To use this API, make a GET request to the `/summary` endpoint with the following query parameters:

- `hour`: (Optional) A string representing the hour to filter articles by `yyyy-mm-dd HH:00:00`.
- `publisher`: (Optional) A string representing the publisher to filter articles by.
- `limit`: (Optional) An integer representing the maximum number of articles to retrieve. The default is 10.

Example:

```bash
curl "http://example.com/articles?hour=yyyy-mm-dd HH:00:00&publisher=nytimes&limit=5"


```bash
curl "http://example.com/articles?hour=yyyy-mm-dd HH:00:00&publisher=nytimes&limit=5"
