from newsdataapi import NewsDataApiClient
"""
This script allows users to search for news articles using the NewsData API.
Workflow:
1. Prompts the user to enter their NewsData API key.
2. Initializes the NewsDataApiClient with the provided API key.
3. Prompts the user to enter a search term.
4. Fetches the latest news articles matching the search term using the API.
5. If results are found, prints the title and link of each article.
6. If no results are found, notifies the user.
Requirements:
- newsdataapi Python package must be installed.
- A valid NewsData API key.
Usage:
Run the script and follow the prompts to enter your API key and search term.
"""

api_key = input('Enter your NewsData API key here: ')

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