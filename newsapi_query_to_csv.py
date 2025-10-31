from newsapi import NewsApiClient
from datetime import datetime, timedelta
import pandas as pd

api_key = input("Enter your NewsAPI key: ")

newsapi = NewsApiClient(api_key=api_key)

query = input("Enter your search query: ")
domains = ''  # list desired domains here, e.g. 'bbc.co.uk,cnn.com'

all_articles = newsapi.get_everything(
    q=query,
    domains=domains,
    from_param=(datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'), #change date range as needed 30 => X days as long as X <= 30
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

print(df.head())

filename = f'newsapi_{query}_results.csv'
df.to_csv(filename, index=False)

print(f"\n✅ Saved {len(df)} results to '{filename}'")
