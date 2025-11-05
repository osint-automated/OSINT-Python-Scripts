"""
This script scrapes a webpage for all unique hyperlinks.
It prompts the user for a URL, fetches the HTML content, and then extracts
and prints all unique 'href' attributes from 'a' tags found on the page.
"""
import requests
from bs4 import BeautifulSoup

def simple_scraper(url):
    """
    Fetches all unique hyperlinks from the given URL.

    Args:
        url (str): The URL of the webpage to scrape.

    Returns:
        set: A set of unique hyperlink strings found in the page's <a> tags.

    Raises:
        requests.exceptions.RequestException: If the HTTP request fails.

    Note:
        Requires 'requests' and 'BeautifulSoup' (from 'bs4') libraries.
    """
    text = requests.get(url).text
    soup = BeautifulSoup(text, 'html.parser')
    tags = soup.find_all('a')
    links = set()
    for tag in tags:
        link = tag.get('href')
        if link:
         links.add(link)
    return links

 
url = input('Enter URL here: ')
results = simple_scraper(url)
for result in results:
    print(result)