from apify_client import ApifyClient
import os
from dotenv import load_dotenv

load_dotenv()

"""
This script uses the Apify API to scrape tweets from a specified Twitter handle.
Workflow:
1. Prompts the user to enter their Apify API key.
2. Initializes the ApifyClient with the provided API key.
3. Sets up the input parameters for the Apify Twitter scraper actor, including:
    - Twitter handles to scrape (e.g., "elonmusk")
    - Number of tweets to retrieve
    - Whether to include user info
    - Proxy configuration
4. Runs the Apify Twitter scraper actor with the specified input.
5. Iterates through the resulting dataset and prints the text of each tweet.
Requirements:
- apify-client Python package
- Valid Apify API key
Note:
- The script prints a separator line after each tweet for readability.
"""

api_key = os.getenv("apify_api_key")

client = ApifyClient(api_key)

run_input = {
    "handles": ["elonmusk"], #change hanndle here to scrape tweets from a different user
    "tweetsDesired": 1,
    "addUserInfo": True,
    "startUrls": [],
    "proxyConfig": { "useApifyProxy": True },
}

run = client.actor("u6ppkMWAx2E2MpEuF").call(run_input=run_input)

for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    text = item.get('text')
    
    print(text)
    print('-' *25)