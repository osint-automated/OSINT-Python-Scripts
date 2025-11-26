"""
This script fetches news articles based on a user-provided query using the Currents API,
and then generates a concise summary of the articles using the Anthropic Claude AI model.
It prompts the user for a search term, retrieves relevant news, and prints the AI-generated summary.
"""
import requests
import anthropic
import os
from dotenv import load_dotenv

load_dotenv()

def get_news(query):
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
        print("No news articles found for your query.")
        return []

    results = []
    for article in news:
        title = article.get('title', 'unknown')
        description = article.get('description', 'unknown')
        article_url = article.get('url', 'unknown')
        author = article.get('author', 'unknown')
        date = article.get('published', 'unknown')

        results.append(f"Title: {title}\nDescription: {description}\nLink: {article_url}\nAuthor: {author}\nPublished Date: {date}\n")

    return results

def ai_summary(results):
    client = anthropic.Anthropic(
        api_key=os.getenv('anthropic_api_key'),
    )

    results_string = "\n".join(results)

    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1000,
        temperature=0,
        messages=[
            {
                "role": "user",
                "content": f"Summarize the following information into a concise paragraph using active voice only and no markdown at all. Dates structured as day month, i.e. 1 November: {results_string}"
            }
        ]
    )
    print(message.content[0].text)


if __name__ == '__main__':
    query = input('Enter search term here: ')
    results = get_news(query)
    if results:
        ai_summary(results)
