"""
This script searches globally for news articles about APT (Advanced Persistent Threat)
campaigns from the last 90 days. It uses the pygooglenews library to query Google News
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
import feedparser
import dateparser

# Register dateparser as a date handler for feedparser
def dateparser_tuple(date_string):
    dt_object = dateparser.parse(date_string)
    if dt_object:
        return dt_object.utctimetuple()
    return None

feedparser.registerDateHandler(dateparser_tuple)


def clean_html(raw_html):
    """Remove HTML tags and trim extra whitespace."""
    if not raw_html:
        return ""
    soup = BeautifulSoup(raw_html, "html.parser")
    return soup.get_text().strip()


def build_apt_query(sector):
    """Build a safe APT-related query without outer parentheses to avoid regex errors."""
    keywords = [
        "APT campaign",
        "advanced persistent threat",
        "cyber espionage campaign",
        "nation-state cyber attack",
        "state-sponsored hacking",
        "cyber operation",
        "espionage operation",
    ]
    # Join with OR and keep quotes around each phrase
    keyword_query = " OR ".join(f'"{kw}"' for kw in keywords)
    return f"{keyword_query} {sector}"  # No outer parentheses


def search_recent_news(sector):
    """Search Google News globally for APT campaigns in the last 90 days."""
    query = build_apt_query(sector)
    all_articles = []

    print(f"\nSearching globally for '{query}'...")
    gn = GoogleNews(lang='en')

    try:
        search_results = gn.search(query)
        entries = search_results.get('entries', [])

        if not entries:
            print("No direct matches, retrying with broader 'APT' query...")
            fallback_query = f'"APT" {sector}'
            search_results = gn.search(fallback_query)
            entries = search_results.get('entries', [])

        if not entries:
            print("No articles found globally.")
            return

        ninety_days_ago = datetime.utcnow() - timedelta(days=90)

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
                published_date = dateparser.parse(getattr(item, "published", "") or getattr(item, "updated", ""))

            # Skip items without a valid date or older than 90 days
            if not published_date or published_date < ninety_days_ago:
                continue

            all_articles.append({
                "Source": source,
                "Date": published_date,
                "Title": getattr(item, "title", ""),
                "Description": clean_description,
                "Link": getattr(item, "link", "")
            })

        if not all_articles:
            print("No recent APT campaign articles in the last 90 days.")
            return

        print(f"Fetched {len(all_articles)} recent articles globally.")

    except Exception as e:
        print(f"An error occurred during global search: {e}")
        return

    # Build DataFrame and export
    df = pd.DataFrame(all_articles)
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce", utc=True)
    df = df.sort_values("Date", ascending=False)
    df = df.drop_duplicates(subset=["Title", "Link"], keep="first")

    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    csv_filename = f"apt_global_news_{sector.replace(' ', '_')}_{timestamp}.csv"
    df.to_csv(csv_filename, index=False, encoding='utf-8-sig')

    print(f"\nSaved {len(df)} unique articles to '{csv_filename}'")

    # Preview results
    print("\n--- Results Preview ---")
    for _, row in df.head(10).iterrows():
        print(f"Date: {row['Date']}")
        print(f"Source: {row['Source']}")
        print(f"Title: {row['Title']}")
        print(f"Description: {row['Description'][:200]}...")
        print(f"Link: {row['Link']}")
        print("-" * 20)


if __name__ == "__main__":
    sector_input = input("Enter the sector to monitor APT campaigns (e.g., energy, government, finance): ").strip()
    if sector_input:
        search_recent_news(sector_input)
    else:
        print("No sector entered. Exiting.")
