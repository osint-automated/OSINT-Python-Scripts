import feedparser
import pandas as pd

NITTER_URLS = [
    "https://nitter.net/sentdefender/rss",
    "https://nitter.net/Faytuks/rss",
    "https://nitter.net/wartranslated/rss",
    "https://nitter.net/WarMonitors/rss",
    # Add more URLs here as needed
]

CSV_FILE = "tweets.csv"

def get_tweets():
    tweets = []
    for url in NITTER_URLS:
        feed = feedparser.parse(url)

        if feed.bozo:
            print(f"Error parsing feed: {feed.bozo_exception}")
            continue

        for entry in feed.entries:
            tweets.append({
                "date": entry.get("published", "N/A"),
                "title": entry.get("title", "N/A"),
                "link": entry.get("link", "N/A"),
            })
    return tweets

if __name__ == "__main__":
    tweets = get_tweets()
    df_new = pd.DataFrame(tweets, columns=['date', 'title', 'link'])
    df_new['date'] = pd.to_datetime(df_new['date'], errors='coerce')

    try:
        df_existing = pd.read_csv(CSV_FILE, encoding='utf-8')
        df_existing['date'] = pd.to_datetime(df_existing['date'], errors='coerce')
        df_combined = pd.concat([df_existing, df_new], ignore_index=True)
    except FileNotFoundError:
        df_combined = df_new

    df_combined.drop_duplicates(subset=['link'], keep='first', inplace=True)
    df_combined.sort_values(by='date', ascending=False, inplace=True)
    df_combined.to_csv(CSV_FILE, index=False, mode='w', encoding='utf-8')