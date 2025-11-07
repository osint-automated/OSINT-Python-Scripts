"""
Global Data Breach & Leak News Monitor
Searches Google News for data breaches and leaks globally
from the last 30 days and saves results to a CSV file.
"""

# --- Compatibility fix for Python 3.10+ ---
import collections
if not hasattr(collections, 'Callable'):
    import collections.abc
    collections.Callable = collections.abc.Callable
# ------------------------------------------------------------------------

from pygooglenews import GoogleNews
from datetime import datetime, timedelta
import pandas as pd
from bs4 import BeautifulSoup
import dateparser
import re


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
    """Build a broad global query for data breaches and leaks."""
    keywords = [
        "data breach",
        "database leak",
        "data leak",
        "information leak",
        "data exposure",
        "cyber leak",
        "customer data stolen",
        "credential leak",
        "data compromise",
        "breach of data",
        "data theft",
        "records exposed",
        "leaked database",
        "data dump"
    ]
    # Keep quotes around each phrase for exact match
    return " OR ".join(f'"{kw}"' for kw in keywords)


def parse_date(item):
    """Safely parse dates from feed items without feedparser.registerDateHandler."""
    try:
        if hasattr(item, "published_parsed") and item.published_parsed:
            return datetime(*item.published_parsed[:6])
        if hasattr(item, "updated_parsed") and item.updated_parsed:
            return datetime(*item.updated_parsed[:6])
        return dateparser.parse(getattr(item, "published", "") or getattr(item, "updated", ""))
    except Exception:
        return None


def search_recent_news():
    """Search Google News globally for data breaches and leaks in the last 30 days."""
    query = build_breach_query()
    all_articles = []

    print(f"\nSearching globally for '{query}'...")
    gn = GoogleNews(lang='en')

    try:
        search_results = gn.search(query)
        entries = search_results.get('entries', [])

        if not entries:
            print("No direct matches found, retrying with fallback 'data breach' query...")
            search_results = gn.search('"data breach"')
            entries = search_results.get('entries', [])

        if not entries:
            print("No articles found globally.")
            return

        thirty_days_ago = datetime.utcnow() - timedelta(days=30)

        for item in entries:
            source = ""
            if hasattr(item, "source") and item.source:
                if isinstance(item.source, dict):
                    source = item.source.get("title", "")
                else:
                    source = str(item.source)

            description = getattr(item, "summary", "") or getattr(item, "description", "")
            clean_description = clean_html(description)

            published_date = parse_date(item)
            if not published_date or published_date < thirty_days_ago:
                continue

            cves = extract_cves(clean_description)

            all_articles.append({
                "Source": source,
                "Date": published_date,
                "Title": getattr(item, "title", ""),
                "Description": clean_description,
                "CVE_References": cves,
                "Link": getattr(item, "link", "")
            })

        if not all_articles:
            print("No recent articles found in the last 30 days.")
            return

        print(f"Fetched {len(all_articles)} recent articles globally.")

    except Exception as e:
        print(f"An error occurred during global search: {e}")
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
    for _, row in df.head(10).iterrows():
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
