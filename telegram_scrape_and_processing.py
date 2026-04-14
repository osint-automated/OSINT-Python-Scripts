"""
Telegram Scrape + Processing Pipeline
====================================

What this tool does
-------------------
This script combines two steps into one workflow:

1) Scrape public Telegram channels via rss-bridge (TelegramBridge in Plaintext mode).
2) Save only new posts into `telegram_posts.csv` (deduplicated by post URL).
3) Filter posts by keyword + recent time window.
4) Write filtered results to `telegram_posts_filtered.csv`, merging with older filtered output
   and keeping one newest row per URL.

In short: one run updates your raw post archive and your curated filtered dataset.

How data flows
--------------
- Input source:
  - Public Telegram channel posts fetched through `rss-bridge.org`.
- Raw archive output:
  - `telegram_posts.csv`
  - Contains all scraped posts over time (no duplicate URLs).
- Filtered output:
  - `telegram_posts_filtered.csv`
  - Contains only rows matching your keyword and date-window criteria.
  - If the file already exists, this script merges new matches and rewrites the file
    with deduplication by URL (newest record wins).

Requirements
------------
- Python 3.10+ recommended
- Packages:
  - requests
  - beautifulsoup4

Install dependencies:
    pip install requests beautifulsoup4

Configuration
-------------
Edit these values in this file:

- `CHANNELS`
  - Telegram channel usernames to monitor.
- `KEYWORDS`
  - Case-insensitive keyword list used to match `title` + `text`.
  - If left empty, all posts within the date window pass the filter.
- `DAYS_WINDOW`
  - Keep only rows newer than N days in the filtering step.
- `RSS_BRIDGE_BASE`
  - RSS-Bridge endpoint. If one instance is down, switch bridge index.

How to run
----------
From this script's folder:
    python telegram_scrape_and_processing.py

What happens on each run:
- Creates `telegram_posts.csv` if missing.
- Scrapes all channels and appends only unseen post URLs.
- Filters rows from raw CSV using your keyword + date settings.
- Creates/updates `telegram_posts_filtered.csv`.
- Prints a concise processing summary.

Notes and limitations
---------------------
- This script only works for public channels accessible through RSS-Bridge.
- RSS-Bridge availability can vary; network failures are logged and skipped.
- URL is used as the unique key for deduplication.
- Timestamp in raw CSV is Unix epoch (UTC); timestamp_human is UTC text.
- A small delay between channel requests is included to be polite to the bridge.
"""

from __future__ import annotations

import csv
import logging
import os
import re
import sys
import time
from datetime import datetime, timedelta, timezone

import requests
from bs4 import BeautifulSoup

# ─── SCRAPER CONFIG ───────────────────────────────────────────────────────────

# this is a curated list of channels that are tailored towards geopolitics and military event tracking
# replace with usernames of the channels you want to scrape from the sector you are monitoring

CHANNELS = [
    "intelslava",
    "osintdefender",
    "UkraineNow",
    "ClashReport",
    "militarysummary",
    "war_monitor",
    "BellumActaNews",
    "geopolitics_prime",
    "GeneralMCNews",
    "englishabuali",
    "rybar_in_english",
    "noel_reports",
    "AMK_Mapping",
    "itarmyofukraine2022",
    "mod_russia_en",
    "news_kremlin_eng",
    "liveukraine_media",
    "beholdisraelchannel",
    "slavyangrad",
    "DDGeopolitics",
    "eurasianchoice",
    "thediplomatmagazine",
    "bioclandestine",
    "OsintDefender",
    "TerrorAlarm",
    "MilitantWire",
    "ThePrintIndia",
    "orftg",
    "RepublicLive",
    "DIUkraine",
    "ourwarstoday",
    "AFUStratCom",
    "astrapress",
    "rybar",
    "wargonzo",
    "readovkanews",
    "mod_russia",
    "ODKB_CSTO",
    "Ukraine_MFA",
    "nytimes",
    "uniannet",
    "vysokygovorit",
    "NEWSWORLD_23",
    "Pravda_Gerashchenko",
    "mykolaivskaODA",
    "vanek_nikolaev",
    "nexta_live",
    "milinfolive",
    "doninside",
    "SolovievLive",
    "stranaua",
    "bneintellinews",
    "RocketAlert",
]

RSS_BRIDGE_BASE = "https://rss-bridge.org/bridge01/"
REQUEST_TIMEOUT = 30

# ─── PROCESSING CONFIG ────────────────────────────────────────────────────────

# this is a list of keywords that are used to filter the posts
# update with keywords of the sector you are monitoring

KEYWORDS = [
    "china",
    "taiwan",
    "iran",
    "ukraine",
    "russia",
    "north korea",
]

DAYS_WINDOW = 30

# ─── PATHS / CSV SCHEMAS ──────────────────────────────────────────────────────

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

RAW_CSV_FILE = os.path.join(SCRIPT_DIR, "telegram_posts.csv")
FILTERED_CSV_FILE = os.path.join(SCRIPT_DIR, "telegram_posts_filtered.csv")

RAW_CSV_HEADERS = [
    "channel",
    "post_id",
    "url",
    "title",
    "timestamp",
    "timestamp_human",
    "text",
]
FILTERED_CSV_HEADERS = ["channel", "url", "title", "timestamp_human", "text"]

# ─── LOGGING ──────────────────────────────────────────────────────────────────

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger(__name__)


# ─── SCRAPER HELPERS ──────────────────────────────────────────────────────────

def ensure_raw_csv_exists() -> None:
    """Create raw output CSV with headers if it does not exist."""
    if os.path.exists(RAW_CSV_FILE):
        log.info("Found existing raw CSV; new posts will be appended.")
        return
    with open(RAW_CSV_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=RAW_CSV_HEADERS)
        writer.writeheader()
    log.info("Created raw CSV: %s", RAW_CSV_FILE)


def load_seen_urls() -> set[str]:
    """Load all URLs in raw CSV for deduplication while appending new posts."""
    seen: set[str] = set()
    if not os.path.exists(RAW_CSV_FILE):
        return seen
    with open(RAW_CSV_FILE, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            seen.add((row.get("url") or "").strip())
    seen.discard("")
    return seen


def append_raw_posts(posts: list[dict]) -> None:
    """Append rows to raw CSV (file must already include headers)."""
    with open(RAW_CSV_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=RAW_CSV_HEADERS)
        writer.writerows(posts)


def build_rssbridge_url(channel: str) -> str:
    return (
        f"{RSS_BRIDGE_BASE}?action=display"
        f"&username={channel}"
        f"&bridge=TelegramBridge"
        f"&format=Plaintext"
    )


def fetch_plaintext(channel: str) -> str | None:
    """Fetch plaintext print_r payload from RSS-Bridge for one channel."""
    url = build_rssbridge_url(channel)
    try:
        response = requests.get(
            url,
            timeout=REQUEST_TIMEOUT,
            headers={"User-Agent": "Mozilla/5.0"},
        )
        response.raise_for_status()
        return response.text
    except requests.RequestException as exc:
        log.error("Failed to fetch %s: %s", channel, exc)
        return None


def clean_html(raw: str) -> str:
    """Strip HTML tags and normalize spacing."""
    return BeautifulSoup(raw, "html.parser").get_text(separator=" ", strip=True)


def parse_print_r_payload(text: str) -> list[dict]:
    """
    Parse RSS-Bridge plaintext print_r format into normalized post dictionaries.
    """
    posts: list[dict] = []
    item_blocks = re.split(r"\[\d+\] => Array\s*\(", text)

    for block in item_blocks[1:]:
        post: dict[str, str | int] = {}

        uri_match = re.search(r"\[uri\] => (https?://\S+)", block)
        post["url"] = uri_match.group(1).strip() if uri_match else ""

        title_match = re.search(r"\[title\] => (.+?)(?=\n\s*\[)", block, re.DOTALL)
        post["title"] = title_match.group(1).strip() if title_match else ""

        ts_match = re.search(r"\[timestamp\] => (\d+)", block)
        if ts_match:
            ts = int(ts_match.group(1))
            post["timestamp"] = ts
            post["timestamp_human"] = datetime.utcfromtimestamp(ts).strftime(
                "%Y-%m-%d %H:%M:%S UTC"
            )
        else:
            post["timestamp"] = ""
            post["timestamp_human"] = ""

        content_match = re.search(
            r"\[content\] => (.+?)(?=\n\s*\[enclosures\])",
            block,
            re.DOTALL,
        )
        if content_match:
            post["text"] = clean_html(content_match.group(1).strip())
        else:
            post["text"] = ""

        if post["url"]:
            post["post_id"] = str(post["url"]).rstrip("/").split("/")[-1]
            posts.append(post)

    return posts


def scrape_all_channels() -> int:
    """Scrape all configured channels and append only unseen URLs to raw CSV."""
    log.info("Starting scrape run.")
    seen_urls = load_seen_urls()
    new_total = 0

    for channel in CHANNELS:
        log.info("Fetching channel: %s", channel)
        raw_text = fetch_plaintext(channel)
        if not raw_text:
            continue

        parsed = parse_print_r_payload(raw_text)
        log.info("Parsed %s posts from %s", len(parsed), channel)

        new_posts: list[dict] = []
        for post in parsed:
            url = (post.get("url") or "").strip()
            if url and url not in seen_urls:
                post["channel"] = channel
                new_posts.append(post)
                seen_urls.add(url)

        if new_posts:
            append_raw_posts(new_posts)
            log.info("Saved %s new posts for %s", len(new_posts), channel)
            new_total += len(new_posts)
        else:
            log.info("No new posts for %s", channel)

        time.sleep(2)

    log.info("Scrape complete. Total new posts saved: %s", new_total)
    return new_total


# ─── PROCESSING HELPERS ───────────────────────────────────────────────────────

def normalize_newlines_to_spaces(value: str) -> str:
    """Replace newlines/tabs with spaces and collapse repeated whitespace."""
    if not value:
        return ""
    t = value.replace("\r\n", "\n").replace("\r", "\n")
    t = t.replace("\n", " ").replace("\t", " ")
    return " ".join(t.split())


def row_unix_ts(row: dict) -> int | None:
    raw = (row.get("timestamp") or "").strip()
    if not raw:
        return None
    try:
        return int(raw)
    except ValueError:
        return None


def row_matches_keywords(row: dict, keywords_lower: list[str]) -> bool:
    if not keywords_lower:
        return True
    haystack = f"{row.get('title', '')} {row.get('text', '')}".lower()
    return any(keyword in haystack for keyword in keywords_lower)


def timestamp_human_to_ts(value: str) -> int:
    """Parse output timestamp text into Unix epoch for sorting."""
    value = (value or "").strip()
    if not value:
        return 0
    if value.endswith(" UTC"):
        value = value[:-4].strip()
    try:
        dt = datetime.strptime(value, "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc)
        return int(dt.timestamp())
    except ValueError:
        return 0


def load_existing_filtered_rows() -> tuple[list[tuple[int, dict]], set[str]]:
    """Load existing filtered output if present."""
    if not os.path.isfile(FILTERED_CSV_FILE):
        return [], set()

    loaded: list[tuple[int, dict]] = []
    urls: set[str] = set()

    with open(FILTERED_CSV_FILE, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            return [], set()
        for row in reader:
            out = {header: row.get(header, "") for header in FILTERED_CSV_HEADERS}
            url = (out.get("url") or "").strip()
            if not url:
                continue
            ts = timestamp_human_to_ts(out.get("timestamp_human", ""))
            loaded.append((ts, out))
            urls.add(url)
    return loaded, urls


def merge_and_dedupe_rows(
    existing: list[tuple[int, dict]],
    fresh: list[tuple[int, dict]],
) -> list[dict]:
    """Sort newest first, and keep only first occurrence of each URL."""
    combined = existing + fresh
    combined.sort(key=lambda item: item[0], reverse=True)

    seen: set[str] = set()
    result: list[dict] = []
    for _, row in combined:
        url = (row.get("url") or "").strip()
        if not url or url in seen:
            continue
        seen.add(url)
        result.append(row)
    return result


def process_filtered_output() -> int:
    """Filter recent keyword-matched rows from raw CSV into filtered CSV output."""
    if not os.path.isfile(RAW_CSV_FILE):
        print(f"Input not found: {RAW_CSV_FILE}", file=sys.stderr)
        return 1

    cutoff = int((datetime.now(timezone.utc) - timedelta(days=DAYS_WINDOW)).timestamp())
    keywords_lower = [k.strip().lower() for k in KEYWORDS if k.strip()]

    existing_rows, existing_urls = load_existing_filtered_rows()
    if existing_rows:
        print("Found existing filtered CSV; merging new matches.")

    fresh: list[tuple[int, dict]] = []
    with open(RAW_CSV_FILE, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            print("Raw CSV has no header row.", file=sys.stderr)
            return 1

        for row in reader:
            ts = row_unix_ts(row)
            if ts is None or ts < cutoff:
                continue
            if not row_matches_keywords(row, keywords_lower):
                continue

            out = {header: row.get(header, "") for header in FILTERED_CSV_HEADERS}
            out["title"] = normalize_newlines_to_spaces(out.get("title", ""))
            out["text"] = normalize_newlines_to_spaces(out.get("text", ""))
            fresh.append((ts, out))

    added_by_url = sum(
        1 for _, row in fresh if (row.get("url") or "").strip() not in existing_urls
    )
    final_rows = merge_and_dedupe_rows(existing_rows, fresh)

    with open(FILTERED_CSV_FILE, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FILTERED_CSV_HEADERS)
        writer.writeheader()
        writer.writerows(final_rows)

    if existing_rows:
        print(
            f"Wrote {len(final_rows)} rows to {FILTERED_CSV_FILE} "
            f"({added_by_url} new URL(s) from this run)."
        )
    else:
        print(f"Created {FILTERED_CSV_FILE} with {len(final_rows)} row(s).")

    return 0


def main() -> int:
    ensure_raw_csv_exists()
    new_scraped = scrape_all_channels()
    process_exit = process_filtered_output()
    print(f"Done. Newly scraped posts this run: {new_scraped}")
    return process_exit


if __name__ == "__main__":
    raise SystemExit(main())
