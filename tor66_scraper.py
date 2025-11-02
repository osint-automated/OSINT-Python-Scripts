import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse

def tor66_scraper(url):
    """
    Scrapes a given URL for .onion links and prints the unique onion URLs found.
    Args:
        url (str): The URL of the page to scrape for .onion links.
    Returns:
        None
    Raises:
        Prints an error message if the URL cannot be fetched due to a requests exception.
    Notes:
        - Only .onion links with 'http' or 'https' schemes are considered.
        - The function prints each unique onion link found on the page.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a')

        onion_links = set()
        for link in links:
            href = link.get('href')
            if href:
                if '.onion' in href:
                    parsed_url = urlparse(href)
                    if parsed_url.scheme == 'http' or parsed_url.scheme == 'https':
                        onion_url = parsed_url.netloc.split('/')[0]
                        onion_links.add('http://' + onion_url)
        
        for onion_link in onion_links:
            print(onion_link)

    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")

if __name__ == '__main__':
    base_url = 'https://tor66.org/search?q='
    search = input('Enter search string here: ')
    search = search.replace(' ', '+')
    url = base_url + search
    tor66_scraper(url)
