import requests
import anthropic

'''
This Python script automates web research by:

Performing a Google Custom Search for a given keyword.

Collecting the textual content (titles, snippets, and descriptions) from the results.

Sending the collected text to Anthropics Claude API to generate a factual and concise summary of recent events related to that keyword.
'''

GOOGLE_API_KEY = input('Enter your Google API key here: ')
SEARCH_ENGINE_ID = input('Enter your Custom Search Engine ID here: ')
CLAUDE_API_KEY = input('Enter your Claude API key here: ')

def google_search(query, date_restrict='d1', max_pages=2, results_per_page=10):
    """Search Google Custom Search API and return collected text content."""
    collected_texts = []
    for page in range(1, max_pages + 1):
        start = (page - 1) * results_per_page + 1
        url = (
            f"https://www.googleapis.com/customsearch/v1"
            f"?key={GOOGLE_API_KEY}&cx={SEARCH_ENGINE_ID}"
            f"&q={query}&start={start}&dateRestrict={date_restrict}"
        )
        response = requests.get(url)
        data = response.json()

        search_items = data.get("items", [])
        if not search_items:
            print("No results found.")
            continue

        for i, item in enumerate(search_items, start=1):
            title = item.get("title", "")
            snippet = item.get("snippet", "")
            try:
                long_desc = item["pagemap"]["metatags"][0].get("og:description", "")
            except (KeyError, IndexError, TypeError):
                long_desc = ""

            text_piece = f"{title}. {snippet}. {long_desc}"
            collected_texts.append(text_piece)

            print("-" * 10, f"Result #{(page-1)*results_per_page + i}", "-" * 10)
            print("Title:", title)
            print("Snippet:", snippet)
            print("Long description:", long_desc)
            print("URL:", item.get("link", ""), "\n")

    return "\n".join(collected_texts)

def summarize_with_claude(text):
    """Send collected text to Claude and return a concise factual summary."""
    client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)
    message = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=1000,
        temperature=0,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"Take the following information and provide an informative summary paragraph, highlighting each individual event based on relevance to {keyword} and excluding anything not related to {keyword}, and describing them with facts only, no fluffy language, active voice only:\n\n{text}"
                    }
                ]
            }
        ]
    )
    return message.content[0].text if message.content else "[No summary returned]"

if __name__ == "__main__":
        keyword = input('enter search term here: ')
        collected_text = google_search(keyword)

        if collected_text.strip():
            summary = summarize_with_claude(collected_text)
            print("SUMMARY RESULT:\n")
            print(summary)
        else:
            print("No text collected for summarization.")