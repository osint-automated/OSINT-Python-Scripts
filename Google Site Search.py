import requests
import time

'''
This Python script uses the Google Custom Search API to find recent results for a given search term restricted to a specific website (e.g., 4chan.org, bsky.app, etc.).

It automates:

Querying Google’s Custom Search JSON API.

Paginating through multiple result sets.

Collecting and displaying key details (title, snippet, URL, and description metadata).
'''

SEARCH_ENGINE_ID = input('Enter your Custom Search Engine ID here: ')
API_KEY = input('Enter your Google API key here: ')

query = input('Enter search term here: ')
site = input('Enter site here: e.g.:4chan.org OR bsky.app ')
search_string = f'{query} site:{site}'

start = 1
all_results = []

while True:
    url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={search_string}&start={start}&dateRestrict=d30"
    response = requests.get(url)
    data = response.json()

    if not data.get("items"):
        break

    all_results.extend(data["items"])
    start += 10
    time.sleep(0.5)

if not all_results:
    print("No results found for the given search term.")
else:
    for i, item in enumerate(all_results, start=1):
        title = item.get("title")
        snippet = item.get("snippet")
        link = item.get("link")
        try:
            description = item["pagemap"]["metatags"][0].get("og:description", "N/A")
        except (KeyError, IndexError):
            description = "N/A"

        print("=" * 10)
        print("Title:", title)
        print("Description:", snippet)
        print("URL:", link, "\n")