"""
This script searches for news articles about ransomware attacks in the US and UK
from the last 90 days based on a user-provided sector. It uses the pygooglenews
library to search Google News and saves the results to a CSV file.
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
from dateutil import parser as dateparser

def clean_html(raw_html):
    """Remove HTML tags and trim extra whitespace."""
    if not raw_html:
        return ""
    soup = BeautifulSoup(raw_html, "html.parser")
    return soup.get_text().strip()

def search_recent_news(sector):
    """
    Searches Google News for ransomware attacks in the US and UK
    related to a specific sector in the last 90 days using intitle:"ransomware attack".
    Each run generates a new CSV file with a timestamp.
    Duplicate articles (based on Title and Link) are removed.
    """
    countries = {"US": "us", "UK": "gb"}
    topic = f'intitle:"ransomware attack" {sector}'
    all_articles = []

    to_date = datetime.now()
    from_date = to_date - timedelta(days=90)
    from_str = from_date.strftime("%Y-%m-%d")
    to_str = to_date.strftime("%Y-%m-%d")

    for country_name, country_code in countries.items():
        print(f"\nSearching for '{topic}' in {country_name} (last 90 days)...")
        gn = GoogleNews(lang='en', country=country_code)
        try:
            search_results = gn.search(topic, from_=from_str, to_=to_str)
            entries = search_results.get('entries', [])
            if not entries:
                print(f"No articles found for {country_name}.")
                continue

            for item in entries:
                # Source extraction
                source = None
                if hasattr(item, "source") and item.source:
                    if isinstance(item.source, dict):
                        source = item.source.get("title", "")
                    else:
                        source = str(item.source)

                # Description cleanup
                description = getattr(item, "summary", "") or getattr(item, "description", "")
                clean_description = clean_html(description)

                # Robust date parsing
                published_date = None
                if hasattr(item, "published_parsed") and item.published_parsed:
                    published_date = datetime(*item.published_parsed[:6])
                elif hasattr(item, "updated_parsed") and item.updated_parsed:
                    published_date = datetime(*item.updated_parsed[:6])
                else:
                    date_str = getattr(item, "published", "") or getattr(item, "updated", "")
                    try:
                        published_date = dateparser.parse(date_str)
                    except Exception:
                        published_date = None

                all_articles.append({
                    "Country": country_name,
                    "Source": source,
                    "Date": published_date,
                    "Title": getattr(item, "title", ""),
                    "Description": clean_description,
                    "Link": getattr(item, "link", "")
                })

            print(f"Fetched {len(entries)} articles from {country_name}.")

        except Exception as e:
            print(f"An error occurred while searching {country_name}: {e}")

    if not all_articles:
        print("\nNo articles found for the specified sector in the last 90 days.")
        return

    # Convert to DataFrame
    df = pd.DataFrame(all_articles)

    # Sort by date safely
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce", utc=True)
    df = df.sort_values("Date", ascending=False)

    # Remove duplicates based on Title and Link
    df = df.drop_duplicates(subset=["Title", "Link"], keep="first")

    # Export to CSV with timestamp
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    csv_filename = f"ransomware_news_{sector.replace(' ', '_')}_{timestamp}.csv"
    df.to_csv(csv_filename, index=False, encoding='utf-8-sig')
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
        print("-" * 20)

if __name__ == "__main__":
    sector_input = input("Enter the sector to monitor ransomware attacks (e.g., healthcare, finance): ").strip()
    if sector_input:
        search_recent_news(sector_input)
    else:
        print("No sector entered. Exiting.")
