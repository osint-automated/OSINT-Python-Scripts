import requests
import time
import os
from dotenv import load_dotenv

load_dotenv()

SEARCH_ENGINE_ID = os.getenv('google_search_engine_id')
API_KEY = os.getenv('google_api_key')

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


