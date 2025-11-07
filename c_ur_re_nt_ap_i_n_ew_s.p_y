"""
This script fetches news articles from the Currents API based on a user-provided query.
It prompts the user for a search term, retrieves the news from the API, and then
prints the title, description, link, author, and published date for each article.
"""
import requests
import os
from dotenv import load_dotenv

load_dotenv()

def main(query):
    """
    Fetches news articles from the Currents API based on the provided query.
    Prompts the user to enter their API key, sends a GET request to the Currents API
    with the specified query and parameters, and returns a formatted string containing
    the details of each news article found.
    Args:
        query (str): The search keywords to filter news articles.
    Returns:
        str: A formatted string with news article details, or a message indicating
             no articles were found.
    """
    api_key = os.getenv('current_news_api_key')
    url = 'https://api.currentsapi.services/v1/search'
    params = {
        'apiKey': api_key,
        'language': 'en',
        'page_size': 50,
        'keywords': query
    }

    response = requests.get(url, params=params)
    data = response.json()
    news = data.get('news', [])

    if not news:
        return "No news articles found for your query."

    result_str = ''
    for article in news:
        title = article.get('title', 'unknown')
        description = article.get('description', 'unknown')
        article_url = article.get('url', 'unknown')
        author = article.get('author', 'unknown')
        date = article.get('published', 'unknown')

        result_str += f'Title: {title}\n'
        result_str += f'Description: {description}\n'
        result_str += f'Link: {article_url}\n'
        result_str += f'Author: {author}\n'
        result_str += f'Published Date: {date}\n'
        result_str += '-' * 40 + '\n'

    return result_str

if __name__ == '__main__':
    query = input('Enter search term here: ')
    results = main(query)
    print(results)
