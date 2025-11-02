import requests
"""
Scrapes unique 'cite' elements from Ahmia.fi search results for a given search term.
Prompts the user to enter a search term, constructs the Ahmia.fi search URL,
fetches the page, parses the HTML, and prints all unique 'cite' texts found in the results.
Dependencies:
    - requests
    - bs4 (BeautifulSoup)
Raises:
    requests.RequestException: If there is an error fetching the URL.
"""
from bs4 import BeautifulSoup

search_term = input('Enter search term here: ')
url = f'https://ahmia.fi/search/?q={search_term.replace(" ", "+")}'

try:
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, 'html.parser')

    unique_cite_texts = set()
    cite_elements = soup.find_all('cite')

    for cite in cite_elements:
        cite_text = cite.get_text()
        unique_cite_texts.add(cite_text)

    for text in unique_cite_texts:
        print(text)

except requests.RequestException as e:
    print(f'Error fetching the URL: {e}')
