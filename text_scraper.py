import requests
from bs4 import BeautifulSoup

def scrape_all_text(url):
    """
    Fetches all visible text from a webpage, ignoring scripts, styles, and metadata.
    Returns text as a single string.
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

        # Remove non-content elements
        for tag in soup(["script", "style", "header", "footer", "nav", "aside", "form", "noscript"]):
            tag.decompose()

        # Grab all visible text
        texts = []
        for element in soup.find_all(text=True):
            text = element.strip()
            if text:
                texts.append(text)

        # Join text with newlines for readability
        full_text = "\n".join(texts)
        return full_text

    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
        return None

if __name__ == "__main__":
    url = input("Enter article URL: ").strip()
    if url:
        content = scrape_all_text(url)
        if content:
            print("\n--- Page Text Preview ---\n")
            print(content[:2000])  # Preview first 2000 chars
            print("\n[Text truncated for preview]")

            # Save full text
            with open("full_scraped_text.txt", "w", encoding="utf-8") as f:
                f.write(content)
            print("\nSaved full text to 'full_scraped_text.txt'")
        else:
            print("No text could be extracted.")
    else:
        print("No URL provided.")
