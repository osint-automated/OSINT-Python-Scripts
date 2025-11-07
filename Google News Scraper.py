"""
This script scrapes Google News for articles on a user-provided topic from the last 30 days.
It uses the pygooglenews library to fetch the news, cleans the article descriptions,
and then saves the results to a CSV file. A preview of the results is also printed to the console.
"""
# --- Compatibility fix for Python 3.10+ and pygooglenews / feedparser ---
import collections
if not hasattr(collections, 'Callable'):
    import collections.abc
    collections.Callable = collections.abc.Callable
# ------------------------------------------------------------------------

from pygooglenews import GoogleNews
from datetime import datetime, timedelta
import pandas as pd
from bs4 import BeautifulSoup

def clean_html(raw_html):
    """Remove HTML tags and trim extra whitespace."""
    if not raw_html:
        return ""
    soup = BeautifulSoup(raw_html, "html.parser")
    return soup.get_text().strip()

def search_recent_news(topic):
    """
    Searches Google News for a given topic within the last 30 days,
    cleans descriptions, saves results to CSV, and prints to console.
    """
    print(f"\nSearching for articles on '{topic}' from the last 30 days...")

    gn = GoogleNews(lang='en', country='US')

    try:
        search_results = gn.search(topic, when='30d')

        if not search_results or not search_results.get('entries'):
            print("No articles found for this topic in the last 30 days.")
            return

        articles = []
        for item in search_results['entries'][:30]:
            source = None
            if hasattr(item, "source") and item.source:
                if isinstance(item.source, dict):
                    source = item.source.get("title", "")
                else:
                    source = str(item.source)

            description = getattr(item, "summary", "") or getattr(item, "description", "")
            clean_description = clean_html(description)

            articles.append({
                "Source": source,
                "Date": getattr(item, "published", ""),
                "Title": getattr(item, "title", ""),
                "Description": clean_description,
                "Link": getattr(item, "link", "")
            })

        # Convert to DataFrame
        df = pd.DataFrame(articles)

        # Sort by date (if possible)
        if "Date" in df.columns:
            try:
                df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
                df = df.sort_values("Date", ascending=False)
            except Exception:
                pass

        # Export to CSV
        csv_filename = f"news_results_{topic.replace(' ', '_')}.csv"
        df.to_csv(csv_filename, index=False, encoding='utf-8-sig')

        print(f"\nSaved {len(df)} articles to '{csv_filename}'")

        # Preview results
        print("\n--- Results ---")
        for _, row in df.iterrows():
            print(f"Source: {row['Source']}")
            print(f"Date: {row['Date']}")
            print(f"Title: {row['Title']}")
            print(f"Description: {row['Description'][:200]}...")
            print(f"Link: {row['Link']}")
            print("-" * 20)

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    search_topic = input("Enter a topic to research: ").strip()
    if search_topic:
        search_recent_news(search_topic)
    else:
        print("No topic entered. Exiting.")
