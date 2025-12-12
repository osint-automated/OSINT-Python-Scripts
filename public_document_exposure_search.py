import requests
from bs4 import BeautifulSoup
import urllib.parse
import re
import time

USER_AGENT = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

FILETYPES = ["pdf", "docx", "xlsx", "pptx"]

SENSITIVE_KEYWORDS = [
    "confidential",
    "internal use",
    "restricted",
    "proprietary",
    "secret",
    "classified",
    "password",
    "creds",
    "login"
]


def duckduckgo_search(query):
    """Scrape DuckDuckGo HTML search results."""
    url = "https://html.duckduckgo.com/html/"
    payload = {"q": query}

    try:
        r = requests.post(url, data=payload, headers=USER_AGENT, timeout=15)
        soup = BeautifulSoup(r.text, "html.parser")
        links = []

        for a in soup.select("a.result__a"):
            link = a.get("href")
            if link:
                links.append(link)

        return links

    except Exception as e:
        return []


def search_documents(keyword):
    """Perform multi-filetype search."""
    results = {}

    for ftype in FILETYPES:
        print(f"Searching for *{ftype}* documents...")
        query = f'{keyword} filetype:{ftype}'
        links = duckduckgo_search(query)
        time.sleep(1)  # polite delay
        results[ftype] = links

    return results


def assess_leak_risk(url):
    """Basic leak scoring based on keywords inside the URL."""
    url_lower = url.lower()
    for word in SENSITIVE_KEYWORDS:
        if word in url_lower:
            return True
    return False


def generate_report(keyword, results):
    print("\n======================================================")
    print("          PUBLIC DOCUMENT EXPOSURE OSINT REPORT")
    print("======================================================\n")

    print(f"Search Keyword: {keyword}\n")

    any_found = False

    for ftype, urls in results.items():
        print(f"Filetype: {ftype.upper()}")
        print("-" * 60)

        if not urls:
            print("No documents found.\n")
            continue

        any_found = True

        for url in urls:
            filename = urllib.parse.unquote(url.split("/")[-1])
            risky = assess_leak_risk(url)
            flag = "Potential Leak Risk" if risky else "Low Risk"

            print(f"Filename: {filename}")
            print(f"URL: {url}")
            print(f"Risk Assessment: {flag}")
            print()

    if not any_found:
        print("No publicly accessible documents found.")

    print("======================================================\n")


def main():
    keyword = input("Enter keyword, company, or domain to search for: ").strip()
    results = search_documents(keyword)
    generate_report(keyword, results)


if __name__ == "__main__":
    main()
