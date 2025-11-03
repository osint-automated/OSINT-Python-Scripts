import asyncio
import aiohttp
import feedparser
from datetime import datetime
from colorama import Fore, Style, init
import json
import os
import csv

# Initialize colorama for color support
init(autoreset=True)

# -------------------------------
# CONFIGURATION
# -------------------------------

SHOW_WARNINGS = False
EXPORT_JSON = True
EXPORT_CSV = True
EXPORT_JSON_PATH = "rss_results_china.json"
EXPORT_CSV_PATH = "rss_results_china.csv"

RSS_LINKS = [
    "https://www.scmp.com/rss/91/feed",                      # South China Morning Post
    "https://www.chinadaily.com.cn/rss/91feed.xml",         # China Daily (English)
    "https://www.globaltimes.cn/rss/china.xml",             # Global Times
    "https://en.people.cn/rss/90001/90776/90785/index.xml", # People's Daily (English)
    "https://www.caixin.com/rss/feed.xml",                  # Caixin Global
    "https://www.ecns.cn/rss/rss.xml",                      # ECNS.cn (may occasionally block bots)
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; AsyncNewsBot/2.0; +https://github.com/newsbot)"
}

# -------------------------------
# CORE FUNCTIONS
# -------------------------------

def log(message, color=Fore.RESET, force=False):
    if SHOW_WARNINGS or force:
        print(f"{color}{message}{Style.RESET_ALL}")


async def fetch_feed(session, url):
    try:
        async with session.get(url, timeout=10) as response:
            if response.status != 200:
                log(f"Skipping {url} (HTTP {response.status})", Fore.YELLOW)
                return []
            data = await response.read()
            feed = feedparser.parse(data)
            if feed.bozo:
                log(f"Malformed feed: {url}", Fore.YELLOW)
            return feed.entries
    except Exception as e:
        log(f"Error fetching {url}: {e}", Fore.YELLOW)
        return []


async def gather_feeds():
    async with aiohttp.ClientSession(headers=HEADERS) as session:
        tasks = [fetch_feed(session, url) for url in RSS_LINKS]
        results = await asyncio.gather(*tasks)
        return [entry for feed in results for entry in feed]


def parse_date(entry):
    for key in ("published_parsed", "updated_parsed"):
        if key in entry and entry[key]:
            return datetime(*entry[key][:6])
    return None


def search_entries(entries, query):
    query = query.lower()
    matches = []
    for e in entries:
        title = e.get("title", "").lower()
        desc = e.get("summary", "").lower()
        if query in title or query in desc:
            matches.append(e)
    return matches


def display_results(matches):
    if not matches:
        print(f"{Fore.RED}No matching articles found.{Style.RESET_ALL}")
        return

    matches.sort(key=lambda e: parse_date(e) or datetime.min, reverse=True)
    print(f"\n{Fore.CYAN}Found {len(matches)} matching articles:")
    print(f"{'=' * 70}{Style.RESET_ALL}")

    for e in matches:
        title = e.get("title", "Untitled")
        link = e.get("link", "No link")
        desc = e.get("summary", "No description")
        pub_date = parse_date(e)
        date_str = pub_date.strftime("%Y-%m-%d %H:%M") if pub_date else "Unknown date"

        print(f"{Fore.GREEN}{title}{Style.RESET_ALL}")
        print(f"Date: {date_str}")
        print(f"Link: {Fore.BLUE}{link}{Style.RESET_ALL}")
        print(f"Description: {desc[:250].strip()}...\n{'-' * 70}")


def export_to_json(matches):
    if not EXPORT_JSON or not matches:
        return

    results = []
    for e in matches:
        results.append({
            "title": e.get("title", ""),
            "link": e.get("link", ""),
            "description": e.get("summary", ""),
            "published": str(parse_date(e))
        })

    with open(EXPORT_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"\nResults exported to JSON: {os.path.abspath(EXPORT_JSON_PATH)}")


def export_to_csv(matches):
    if not EXPORT_CSV or not matches:
        return

    fieldnames = ["title", "link", "description", "published"]

    with open(EXPORT_CSV_PATH, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for e in matches:
            writer.writerow({
                "title": e.get("title", ""),
                "link": e.get("link", ""),
                "description": e.get("summary", ""),
                "published": str(parse_date(e))
            })

    print(f"Results exported to CSV: {os.path.abspath(EXPORT_CSV_PATH)}")


# -------------------------------
# MAIN PROGRAM
# -------------------------------

async def main():
    query = input("Enter search term here: ").strip()
    if not query:
        print("No search term entered. Exiting.")
        return

    print("\nFetching RSS feeds, please wait...\n")
    entries = await gather_feeds()
    matches = search_entries(entries, query)
    display_results(matches)
    #export_to_json(matches) #optional export to json
    export_to_csv(matches)


if __name__ == "__main__":
    asyncio.run(main())
