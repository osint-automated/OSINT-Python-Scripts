"""
Global Influence Operations (excl. hacktivism) monitor
Searches Google News for influence / information operation / disinformation stories
from the last 30 days. Excludes hacktivism-related coverage. Exports to CSV.
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


LANG = "en"  # only English results; remove/change if you want multilingual

# Terms to search for (broad influence / IO / disinfo vocabulary)
INFLUENCE_KEYWORDS = [
    "influence operation",
    "information operation",
    "disinformation",
    "propaganda",
    "social media manipulation",
    "foreign influence",
    "state-sponsored"
]

# Words that indicate hacktivism — results containing these will be filtered out
HACKTIVIST_TERMS = [
    "hacktivist", "hacktivism", "anonymous", "website defacement", "website defaced",
    "do x", "dox", "doxing", "doxxed", "doxed", "defacement"
]

# Platforms to detect in article text
PLATFORM_KEYWORDS = ["Twitter", "X", "Facebook", "Instagram", "TikTok", "Telegram", "Reddit", "YouTube"]

def clean_html(raw_html):
    """Remove HTML tags and trim extra whitespace."""
    if not raw_html:
        return ""
    soup = BeautifulSoup(raw_html, "html.parser")
    return soup.get_text().strip()

def build_influence_query():
    """Combine keywords into an OR query string for Google News."""
    # wrap each phrase in quotes (already quoted above) and join with OR
    return " OR ".join(INFLUENCE_KEYWORDS)

def detect_platforms(text):
    """Return comma-separated platform names found in text (case-insensitive)."""
    found = []
    if not text:
        return ""
    for p in PLATFORM_KEYWORDS:
        # match whole word-ish, case-insensitive
        if re.search(r"\b" + re.escape(p) + r"\b", text, flags=re.IGNORECASE):
            found.append(p)
    return ", ".join(found)

def contains_hacktivist_terms(text):
    """Return True if text contains hacktivist indicators (case-insensitive)."""
    if not text:
        return False
    for term in HACKTIVIST_TERMS:
        if re.search(re.escape(term), text, flags=re.IGNORECASE):
            return True
    return False

def is_state_sponsored(text):
    """Lightweight detection if an article mentions state-sponsored language."""
    if not text:
        return False
    return bool(re.search(r"\b(state[- ]?sponsored|nation[- ]?state|state[- ]?linked|state actor|government[- ]?linked)\b", text, flags=re.IGNORECASE))

def search_recent_influence_ops():
    """Main function: global search for influence operations in the last WINDOW_DAYS."""
    query = build_influence_query()
    all_articles = []

    print(f"\nSearching globally for influence operations...")
    gn = GoogleNews(lang=LANG)

    try:
        search_results = gn.search(query)
        entries = search_results.get("entries", [])

        # fallback if OR list returns nothing
        if not entries:
            print("No direct matches found, retrying with broader 'disinformation' query...")
            search_results = gn.search('"disinformation"')
            entries = search_results.get("entries", [])

        if not entries:
            print("No influence-operation articles found globally in the time window.")
            return

        for item in entries:
            title = getattr(item, "title", "") or ""
            description = getattr(item, "summary", "") or getattr(item, "description", "") or ""
            combined_text = " ".join([title, description])
            clean_description = clean_html(description)

            # filter out hacktivism-related results
            if contains_hacktivist_terms(combined_text):
                # skip entries that look like hacktivist coverage
                continue

            # Robust date parsing
            published_date = None
            if hasattr(item, "published_parsed") and item.published_parsed:
                published_date = datetime(*item.published_parsed[:6])
            elif hasattr(item, "updated_parsed") and item.updated_parsed:
                published_date = datetime(*item.updated_parsed[:6])
            else:
                published_date = getattr(item, "published", "") or getattr(item, "updated", "")

            platforms = detect_platforms(combined_text)
            state_flag = is_state_sponsored(combined_text)

            all_articles.append({
                "Source": (item.source.get("title") if isinstance(getattr(item, "source", None), dict) else str(getattr(item, "source", "") or "")),
                "Date": published_date,
                "Title": title,
                "Description": clean_description,
                "Platforms_Mentioned": platforms,
                "State_Sponsored_Flag": state_flag,
                "Link": getattr(item, "link", "")
            })

        print(f"Fetched {len(all_articles)} candidate articles (after excluding hacktivism).")

    except Exception as e:
        print(f"An error occurred during global search: {e}")
        return

    if not all_articles:
        print("\nNo articles passed filtering for influence operations in the last {WINDOW_DAYS} days.")
        return

    # Convert to DataFrame and clean up
    df = pd.DataFrame(all_articles)
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce", utc=True)
    df = df.sort_values("Date", ascending=False)
    df = df.drop_duplicates(subset=["Title", "Link"], keep="first")

    # Export to CSV
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    csv_filename = f"influence_global_news_{timestamp}.csv"
    df.to_csv(csv_filename, index=False, encoding="utf-8-sig")
    print(f"\nSaved {len(df)} unique articles to '{csv_filename}'")

    # Print a short preview
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
