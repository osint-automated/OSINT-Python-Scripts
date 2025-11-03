import feedparser
import csv
import os

"""
This script searches for a user-provided term in the titles of news articles from a list of RSS feeds.
Modules:
    feedparser: Used to parse RSS feeds.
Variables:
    links (list): A list of RSS feed URLs to search.
    query (str): The search term entered by the user, converted to lowercase.
Workflow:
    1. Prompts the user to enter a search term.
    2. Iterates through each RSS feed URL in 'links'.
    3. Parses the RSS feed and iterates through its entries.
    4. Checks if the search term is present in the entry's title (case-insensitive).
    5. If a match is found, prints the article's title, link, and description.
Usage:
    Run the script and enter a search term when prompted. The script will display matching articles from the provided RSS feeds.
"""
links = [
    'http://feeds.bbci.co.uk/news/world/rss.xml',        # BBC World News
    'http://rss.cnn.com/rss/edition_world.rss',         # CNN World
    'https://www.aljazeera.com/xml/rss/all.xml',        # Al Jazeera
    'https://moxie.foxnews.com/google-publisher/latest.xml',  # Fox News
    'http://feeds.skynews.com/feeds/rss/world.xml',     # Sky News
    'https://www.cnbc.com/id/100727362/device/rss/rss.html',  # CNBC
    'http://www.mirror.co.uk/news/world-news/rss.xml',  # Mirror World
    'https://rss.csmonitor.com/feeds/world',           # Christian Science Monitor
    'https://feeds.feedburner.com/ndtvnews-world-news',# NDTV World
]

# Prompt for search term
query = input("Enter search term here: ").lower()

# Prepare CSV output
csv_file = "rss_search_results.csv"
fieldnames = ["title", "link", "description"]

matches = []

for rss_link in links:  # iterate over the actual feed URLs
    try:
        feed = feedparser.parse(rss_link)
        if feed.bozo:
            print(f"[!] Warning: malformed feed {rss_link}")
        for entry in feed.entries:
            title = entry.get("title", "")
            description = entry.get("description", "")
            link = entry.get("link", "")
            if query in title.lower():
                print(f"Title: {title}")
                print(f"Link: {link}")
                print(f"Description: {description[:300]}...\n{'-'*60}")
                matches.append({"title": title, "link": link, "description": description})
    except Exception as e:
        print(f"[!] Failed to fetch {rss_link}: {e}")

# Export to CSV
if matches:
    try:
        with open(csv_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(matches)
        print(f"\n[*] {len(matches)} matching articles saved to '{os.path.abspath(csv_file)}'")
    except Exception as e:
        print(f"[!] Failed to write CSV: {e}")
else:
    print("No matching articles found.")
