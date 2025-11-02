from apify_client import ApifyClient
import os
from dotenv import load_dotenv

load_dotenv()

"""
This script downloads comments from a specified TikTok video using the Apify API.
Prompts the user for:
    - Apify API key
    - TikTok video URL
    - Number of comments to download (max 1000)
Validates the number of comments input and exits if invalid.
Uses the ApifyClient to run the TikTok scraper actor with the provided video URL and comment limits.
Iterates through the results and prints each comment's video URL, user ID, and text.
Requirements:
    - apify_client package
    - Valid Apify API key
Note:
    - The maximum number of comments per post is capped at 100.
    - The maximum number of replies per comment is set to the user-specified number.
"""

api_key = os.getenv('apify_api_key')


client = ApifyClient(api_key)

video_url = input('Enter TikTok URL here: ')
num_of_comments = input('Enter number of comments to download (max 1000): ')

try:
    num_of_comments = int(num_of_comments)
    if num_of_comments <= 0 or num_of_comments > 1000:
        raise ValueError("The number of comments must be between 1 and 1000.")
except ValueError as e:
    print(f"Invalid input: {e}")
    exit(1)

run_input = {
    "postURLs": [video_url],
    "commentsPerPost": min(num_of_comments, 100),
    "maxRepliesPerComment": num_of_comments,
}

run = client.actor("BDec00yAmCm1QbMEI").call(run_input=run_input)

for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    video_web_url = item.get("videoWebUrl")
    text = item.get('text')
    uid = item.get('uid')
    
    print(f'Video URL: {video_web_url}')
    print(f'User ID: {uid}')
    print(f'Comment: {text}')
    print('------------------------')
