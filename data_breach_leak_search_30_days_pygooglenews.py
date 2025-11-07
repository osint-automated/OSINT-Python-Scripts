"""
This script searches globally for news articles about data breaches and leaks
from the last 30 days. It uses the pygooglenews library to query Google News
and saves the results to a CSV file.
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
import feedparser # Import feedparser
import dateparser # Import the dateparser library
import re

# Register dateparser as a date handler for feedparser
try:
    def dateparser_tuple(date_string):
        dt_object = dateparser.parse(date_string)
        if dt_object:
            return dt_object.utctimetuple()
        return None
    feedparser.registerDateHandler(dateparser_tuple)
except ImportError:
    print("dateparser not installed. Install it with 'pip install dateparser' for better date parsing.")

def clean_html(raw_html):
    """Remove HTML tags and trim extra whitespace."""
    if not raw_html:
        return ""
    soup = BeautifulSoup(raw_html, "html.parser")
    return soup.get_text().strip()

def extract_cves(text):
    """Extract CVE identifiers if present."""
    return ", ".join(re.findall(r"CVE-\d{4}-\d{4,7}", text, re.IGNORECASE))

def build_breach_query():
    """
    Builds a broad global query for data breaches and leaks.
    """
    keywords = [
        '"data breach"',
        '"database leak"',
        "'data leak'",
        '"information leak"',
        '"data exposure"',
        '"cyber leak"',
        '"customer data stolen"',
        '"credential leak"',
        '"data compromise"',
        '"breach of data"',
        '"data theft"',
        '"records exposed"',
        '"leaked database"',
        '"data dump"'
    ]
    query = " OR ".join(keywords)
    return query

def search_recent_news():
    """
    Searches Google News globally for data breaches and leaks in the last 30 days.
    """
    query = build_breach_query()
    all_articles = []

    print(f"\nSearching globally for '{query}'...")
    gn = GoogleNews(lang='en')
    try:
        search_results = gn.search(query)
        entries = search_results.get('entries', [])
        if not entries:
            print("No direct matches found, retrying with fallback 'data breach' query...")
            fallback_query = '"data breach"'
            search_results = gn.search(fallback_query)
            entries = search_results.get('entries', [])

        if not entries:
            print("No articles found globally for the last 30 days.")
            return

        for item in entries:
            source = None
            if hasattr(item, "source") and item.source:
                if isinstance(item.source, dict):
                    source = item.source.get("title", "")
                else:
                    source = str(item.source)

            description = getattr(item, "summary", "") or getattr(item, "description", "")
            clean_description = clean_html(description)

            published_date = None
            if hasattr(item, "published_parsed") and item.published_parsed:
                published_date = datetime(*item.published_parsed[:6])
            elif hasattr(item, "updated_parsed") and item.updated_parsed:
                published_date = datetime(*item.updated_parsed[:6])
            else:
                published_date = getattr(item, "published", "") or getattr(item, "updated", "")

            cves = extract_cves(clean_description)

            all_articles.append({
                "Source": source,
                "Date": published_date,
                "Title": getattr(item, "title", ""),
                "Description": clean_description,
                "CVE_References": cves,
                "Link": getattr(item, "link", "")
            })

        print(f"Fetched {len(entries)} articles globally.")

    except Exception as e:
        print(f"An error occurred during global search: {e}")
        return

    if not all_articles:
        print("\nNo articles found in the last 30 days.")
        return

    # Convert to DataFrame
    df = pd.DataFrame(all_articles)
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce", utc=True)
    df = df.sort_values("Date", ascending=False)
    df = df.drop_duplicates(subset=["Title", "Link"], keep="first")

    # Export to CSV
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    csv_filename = f"data_breach_global_news_{timestamp}.csv"
    df.to_csv(csv_filename, index=False, encoding='utf-8-sig')
    print(f"\nSaved {len(df)} unique articles to '{csv_filename}'")

    # Preview results
    print("\n--- Results Preview ---")
    for _, row in df.iterrows():
        print(f"Date: {row['Date']}")
        print(f"Source: {row['Source']}")
        print(f"Title: {row['Title']}")
        if row['CVE_References']:
            print(f"CVE References: {row['CVE_References']}")
        print(f"Description: {row['Description'][:200]}...")
        print(f"Link: {row['Link']}")
        print("-" * 20)

if __name__ == "__main__":
    search_recent_news()
