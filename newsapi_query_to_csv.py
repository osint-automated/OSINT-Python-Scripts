from newsapi import NewsApiClient
from datetime import datetime, timedelta
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

def news_search(query):
    api_key = os.getenv('newsapi_key')
    newsapi = NewsApiClient(api_key=api_key)
    domains = ''  # list desired domains here, e.g. 'bbc.co.uk,cnn.com'
    all_articles = newsapi.get_everything(
        q=query,
        domains=domains,
        from_param=(datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d'), #change date range as needed 30 => X days as long as X <= 30
        language='en',
    )
    results = all_articles.get('articles', [])
    data = []

    for result in results:
        data.append({
            'Source': result['source']['name'],
            'Title': result['title'],
            'Description': result['description'],
            'URL': result['url']
        })

    df = pd.DataFrame(data, columns=['Source', 'Title', 'Description', 'URL'])
    filename = f'newsapi_query_results.csv'
    df.to_csv(filename, index=False)
    print(df.head())
    print(f"\nSaved {len(df)} results to '{filename}'")


if __name__ == "__main__":
    query = input("Enter your search query: ")
    news_search(query)