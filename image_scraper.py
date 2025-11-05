"""
This script scrapes a webpage for all image tags and extracts their alt text and source links.
It prompts the user for a URL, fetches the HTML content, and then prints the details
for each image found.
"""
import requests
from bs4 import BeautifulSoup

def scraper(url):
    """
    Scrapes all <img> tags from the given URL and prints their alt text and source link.

    Args:
        url (str): The URL of the webpage to scrape.

    Returns:
        None

    Prints:
        For each <img> tag found, prints a separator line, the alt text (or a default message if not available),
        and the image source link (or a default message if not available).

    Exceptions:
        Prints an error message if the HTTP request fails or if no <img> tags are found.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        tags = soup.find_all('img')
        if not tags:
            print("No <img> tags found.")
            return
        for tag in tags:
            print('-' * 45)
            alt_text = tag.get('alt', 'No alt text available')
            img_link = tag.get('src', 'No source available')
            print('Image Text: ' + alt_text)
            print('Image Link: ' + img_link)
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    url = input('Enter URL here: ')
    scraper(url)
