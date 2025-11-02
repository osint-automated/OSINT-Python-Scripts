import requests
"""
This script performs a Google Custom Search using the Custom Search JSON API.
Prompts the user for:
    - API key
    - Search engine ID
    - Search term
Searches for the specified query, restricted to results from the last 30 days (`dateRestrict='d30'`), and retrieves up to `max_pages` pages of results (default: 1 page, 10 results per page).
For each search result, prints:
    - Title
    - Description (snippet)
    - Long description (from Open Graph metadata, if available)
    - URL
Dependencies:
    - requests
Note:
    - Requires a valid Google API key and Custom Search Engine ID.
    - Handles missing metadata gracefully.
"""

API_KEY = input('Enter API key here: ')
SEARCH_ENGINE_ID = input('Enter search engine ID here: ')

query = input('Enter search term here: ')
date_restrict = 'd30'
max_pages = 1
results_per_page = 10

for page in range(1, max_pages + 1):
    start = (page - 1) * results_per_page + 1
    url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}&start={start}&dateRestrict={date_restrict}"

    data = requests.get(url).json()

    search_items = data.get("items")
    for i, search_item in enumerate(search_items, start=1):
        try:
            long_description = search_item["pagemap"]["metatags"][0]["og:description"]
        except KeyError:
            long_description = "N/A"
        title = search_item.get("title")
        snippet = search_item.get("snippet")
        html_snippet = search_item.get("htmlSnippet")
        link = search_item.get("link")
        print("-"*10, f"Result #{(page-1)*results_per_page + i}", "-"*10)
        print("Title:", title)
        print("Description:", snippet)
        print("Long description:", long_description)
        print("URL:", link, "\n")
