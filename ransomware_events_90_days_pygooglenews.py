"""
Ransomware Attack Monitor
Searches for news articles about ransomware attacks in the US and UK
from the last 90 days based on a user-provided sector.
Uses the pygooglenews library to search Google News and saves results to a CSV file.
"""

# --- Compatibility fix for Python 3.10+ and pygooglenews / feedparser ---
import collections
if not hasattr(collections, "Callable"):
    import collections.abc
    collections.Callable = collections.abc.Callable
# ------------------------------------------------------------------------

from pygooglenews import GoogleNews
from datetime import datetime, timedelta
import pandas as pd
from bs4 import BeautifulSoup
import dateparser

WINDOW_DAYS = 90
COUNTRIES = {"US": "us", "UK": "gb"}


def clean_html(raw_html):
    """Remove HTML tags and trim extra whitespace."""
    if not raw_html:
        return ""
    soup = BeautifulSoup(raw_html, "html.parser")
    return soup.get_text().strip()


def build_query(sector):
    """Builds a search query for ransomware-related articles in a given sector."""
    keywords = [
        'intitle:"ransomware attack"',
        '"ransomware incident"',
        '"ransomware group"',
        '"ransomware campaign"',
        '"ransomware outbreak"',
        '"cyber extortion"',
    ]
    keyword_query = " OR ".join(keywords)
    return f"({keyword_query}) {sector}"


def parse_date(item):
    """Robustly parse published/updated dates using multiple fallbacks."""
    published_date = None
    try:
        if hasattr(item, "published_parsed") and item.published_parsed:
            published_date = datetime(*item.published_parsed[:6])
        elif hasattr(item, "updated_parsed") and item.updated_parsed:
            published_date = datetime(*item.updated_parsed[:6])
        elif hasattr(item, "published") and item.published:
            dt = dateparser.parse(item.published)
            if dt:
                published_date = dt
        elif hasattr(item, "updated") and item.updated:
            dt = dateparser.parse(item.updated)
            if dt:
                published_date = dt
    except Exception:
        published_date = None
    return published_date


def search_recent_news(sector):
    """Searches Google News for ransomware attacks by sector in the last 90 days (US + UK)."""
    query = build_query(sector)
    all_articles = []
    cutoff_date = datetime.utcnow() - timedelta(days=WINDOW_DAYS)

    for country_name, country_code in COUNTRIES.items():
        print(f"\nSearching for '{query}' in {country_name}...")
        gn = GoogleNews(lang="en", country=country_code)

        try:
            search_results = gn.search(query)
            entries = search_results.get("entries", [])

            if not entries:
                print(f"No direct matches in {country_name}, retrying with broader 'ransomware {sector}' query...")
                fallback_query = f'"ransomware" {sector}'
                search_results = gn.search(fallback_query)
                entries = search_results.get("entries", [])

            if not entries:
                print(f"No articles found in {country_name}.")
                continue

            for item in entries:
                title = getattr(item, "title", "") or ""
                description = getattr(item, "summary", "") or getattr(item, "description", "") or ""
                clean_description = clean_html(description)

                published_date = parse_date(item)

                # Skip old articles
                if published_date and published_date < cutoff_date:
                    continue

                source = ""
                if hasattr(item, "source") and item.source:
                    if isinstance(item.source, dict):
                        source = item.source.get("title", "")
                    else:
                        source = str(item.source)

                all_articles.append({
                    "Country": country_name,
                    "Source": source,
                    "Date": published_date,
                    "Title": title,
                    "Description": clean_description,
                    "Link": getattr(item, "link", "")
                })

            print(f"Fetched {len(entries)} total; retained {len(all_articles)} after 90-day filtering for {country_name}.")

        except Exception as e:
            print(f"Error searching {country_name}: {e}")

    if not all_articles:
        print("\nNo recent ransomware articles found for the specified sector.")
        return

    # Convert to DataFrame
    df = pd.DataFrame(all_articles)
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce", utc=True)
    df = df.sort_values("Date", ascending=False)
    df = df.drop_duplicates(subset=["Title", "Link"], keep="first")

    # Export results
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    csv_filename = f"ransomware_news_{sector.replace(' ', '_')}_{timestamp}.csv"
    df.to_csv(csv_filename, index=False, encoding="utf-8-sig")
    print(f"\nSaved {len(df)} unique articles to '{csv_filename}'")

    # Preview results
    print("\n--- Results Preview ---")
    for _, row in df.iterrows():
        print(f"Country: {row['Country']}")
        print(f"Date: {row['Date']}")
        print(f"Source: {row['Source']}")
        print(f"Title: {row['Title']}")
        print(f"Description: {row['Description'][:200]}...")
        print(f"Link: {row['Link']}")
        print("-" * 80)


if __name__ == "__main__":
    sector_input = input("Enter the sector to monitor ransomware attacks (e.g., healthcare, finance): ").strip()
    if sector_input:
        search_recent_news(sector_input)
    else:
        print("No sector entered. Exiting.")
