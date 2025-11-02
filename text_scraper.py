import requests
from bs4 import BeautifulSoup

def extract_main_text(url):
    """
    Fetches the main article text from a webpage, ignoring menus, footers, and ads.
    Returns cleaned text suitable for summarization or analysis.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/123.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Remove obvious non-article elements
        for tag in soup(["script", "style", "header", "footer", "nav", "aside", "form", "noscript"]):
            tag.decompose()

        # Find candidate containers (divs or articles)
        candidates = soup.find_all(["article", "div", "section"], recursive=True)

        max_text = ""
        max_len = 0

        for candidate in candidates:
            text = " ".join(p.get_text(strip=True) for p in candidate.find_all("p"))
            # Score by text length
            if len(text) > max_len:
                max_len = len(text)
                max_text = text

        # Fallback: all page text
        if not max_text:
            max_text = " ".join(p.get_text(strip=True) for p in soup.find_all("p"))

        return max_text.strip()

    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
        return None

if __name__ == "__main__":
    url = input("Enter article URL: ").strip()
    if url:
        content = extract_main_text(url)
        if content:
            print("\n--- Extracted Article Text Preview ---\n")
            print(content[:2000])  # Preview first 2000 characters
            print("\n[Text truncated for preview]")

            # Save to file
            with open("main_article_text.txt", "w", encoding="utf-8") as f:
                f.write(content)
            print("\nSaved main article text to 'main_article_text.txt'")
        else:
            print("No main article text could be extracted.")
    else:
        print("No URL provided.")
