"""
This script searches for news articles using the NewsData.io API.
It prompts the user for a search term, queries the API for the latest news
matching the term, and then prints the title and link of each article found.
"""
from newsdataapi import NewsDataApiClient
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('newsdata_api_key')

api = NewsDataApiClient(apikey=api_key)

query = input('Enter search term here: ')

response = api.latest_api(q=query)

if response and 'results' in response:
    for article in response['results']:
        if 'title' in article:
            print(article['title'])
            print(article['link'])
            print('-' *30)
else:
    print("No results found.")


