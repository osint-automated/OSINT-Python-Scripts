"""
Global Influence Operations (excl. hacktivism) monitor
Searches Google News for influence / information operation / disinformation stories
from the last 30 days. Excludes hacktivism-related coverage. Exports to CSV.
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
import feedparser
import dateparser
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


LANG = "en"  # English results only
WINDOW_DAYS = 30

INFLUENCE_KEYWORDS = [
    "influence operation",
    "information operation",
    "disinformation",
    "propaganda",
    "social media manipulation",
    "foreign influence",
    "state-sponsored",
]

HACKTIVIST_TERMS = [
    "hacktivist", "hacktivism", "anonymous", "website defacement", "website defaced",
    "dox", "doxing", "doxxed", "doxed", "defacement",
]

PLATFORM_KEYWORDS = ["Twitter", "X", "Facebook", "Instagram", "TikTok", "Telegram", "Reddit", "YouTube"]


def clean_html(raw_html):
    if not raw_html:
        return ""
    soup = BeautifulSoup(raw_html, "html.parser")
    return soup.get_text().strip()


def build_influence_query():
    return " OR ".join([f'"{kw}"' if not kw.startswith('"') else kw for kw in INFLUENCE_KEYWORDS])


def detect_platforms(text):
    if not text:
        return ""
    found = [p for p in PLATFORM_KEYWORDS if re.search(r"\b" + re.escape(p) + r"\b", text, re.IGNORECASE)]
    return ", ".join(found)


def contains_hacktivist_terms(text):
    if not text:
        return False
    for term in HACKTIVIST_TERMS:
        if re.search(re.escape(term), text, re.IGNORECASE):
            return True
    return False


def is_state_sponsored(text):
    if not text:
        return False
    return bool(
        re.search(
            r"\b(state[- ]?sponsored|nation[- ]?state|state[- ]?linked|state actor|government[- ]?linked)\b",
            text,
            re.IGNORECASE,
        )
    )


def search_recent_influence_ops():
    """Global search for influence operations in the last 30 days."""
    query = build_influence_query()
    all_articles = []

    print(f"\nSearching globally for influence operation news...")
    gn = GoogleNews(lang=LANG)

    try:
        # Remove from_/to_ arguments to avoid date parsing issues
        search_results = gn.search(query)
        entries = search_results.get("entries", [])

        if not entries:
            print("No direct matches found, retrying with fallback 'disinformation' query...")
            search_results = gn.search('"disinformation"')
            entries = search_results.get("entries", [])

        if not entries:
            print("No influence-operation articles found globally.")
            return

        cutoff_date = datetime.utcnow() - timedelta(days=WINDOW_DAYS)

        for item in entries:
            title = getattr(item, "title", "") or ""
            description = getattr(item, "summary", "") or getattr(item, "description", "") or ""
            combined_text = " ".join([title, description])
            clean_description = clean_html(description)

            # Skip hacktivist-related articles
            if contains_hacktivist_terms(combined_text):
                continue

            published_date = None
            if hasattr(item, "published_parsed") and item.published_parsed:
                published_date = datetime(*item.published_parsed[:6])
            elif hasattr(item, "updated_parsed") and item.updated_parsed:
                published_date = datetime(*item.updated_parsed[:6])

            # Skip articles older than 30 days
            if published_date and published_date < cutoff_date:
                continue

            platforms = detect_platforms(combined_text)
            state_flag = is_state_sponsored(combined_text)

            source = ""
            if hasattr(item, "source") and item.source:
                if isinstance(item.source, dict):
                    source = item.source.get("title", "")
                else:
                    source = str(item.source)

            all_articles.append({
                "Source": source,
                "Date": published_date,
                "Title": title,
                "Description": clean_description,
                "Platforms_Mentioned": platforms,
                "State_Sponsored_Flag": state_flag,
                "Link": getattr(item, "link", "")
            })

        print(f"Fetched {len(all_articles)} recent articles (after filtering hacktivism, within {WINDOW_DAYS} days).")

    except Exception as e:
        print(f"An error occurred during global search: {e}")
        return

    if not all_articles:
        print("\nNo recent influence-operation articles found after filtering.")
        return

    # DataFrame cleanup
    df = pd.DataFrame(all_articles)
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce", utc=True)
    df = df.sort_values("Date", ascending=False)
    df = df.drop_duplicates(subset=["Title", "Link"], keep="first")

    # Export to CSV
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    csv_filename = f"influence_global_news_{timestamp}.csv"
    df.to_csv(csv_filename, index=False, encoding="utf-8-sig")
    print(f"\nSaved {len(df)} unique articles to '{csv_filename}'")

    # Preview output
    print("\n--- Results Preview ---")
    for _, row in df.iterrows():
        print(f"Date: {row['Date']}")
        print(f"Source: {row['Source']}")
        print(f"Title: {row['Title']}")
        if row["Platforms_Mentioned"]:
            print(f"Platforms: {row['Platforms_Mentioned']}")
        if row["State_Sponsored_Flag"]:
            print("State-Sponsored Indicator: True")
        print(f"Description: {row['Description'][:300]}...")
        print(f"Link: {row['Link']}")
        print("-" * 80)


if __name__ == "__main__":
    search_recent_influence_ops()
