from apify_client import ApifyClient
import os
from dotenv import load_dotenv

load_dotenv()

"""
This script scrapes public profile information from Instagram using the Apify API.
Workflow:
1. Prompts the user for their Apify API key and the Instagram handle to search.
2. Initializes the Apify client with the provided API key.
3. Runs the Apify Instagram Profile Scraper actor with the specified username.
4. Iterates over the results in the returned dataset and extracts profile details:
    - id
    - username
    - url
    - full name
    - biography
    - external URL
    - follower count
    - follow count
    - profile picture URL
5. Prints the extracted information for each profile.
Requirements:
- apify_client library
- Valid Apify API key
Note:
- Only public profile information is accessible.
- The script prints the results to the console.
"""

apify_api_key = os.getenv("apify_api_key")

client = ApifyClient(apify_api_key)

search = input('Enter Instagram handle here: ')

run_input = { "usernames": [search] }

run = client.actor("dSCLg0C3YEZ83HzYX").call(run_input=run_input)

for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    id = item.get('id')
    username = item.get('username')
    url = item.get('url')
    fullname = item.get('fullName')
    biography = item.get('biography')
    external_url = item.get('externalUrl')
    follower_count = item.get('followersCount')
    follow_count = item.get('followsCount')
    profile_pic_url = item.get('profilePicUrl')
    
    
    print(f'Username: ', username)
    print(f'URL: ', url)
    print(f'Instagram ID: ', id)
    print(f'Full Name: ', fullname)
    print(f'Biography: ', biography)
    print(f'External URL: ', external_url)
    print(f'Follower Count: ', follower_count)
    print(f'Follow Count: ', follow_count)
    print(f'Profile Pic URL: ', profile_pic_url)
    print('------------------------')