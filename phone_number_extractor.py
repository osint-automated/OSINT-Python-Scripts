"""
This script extracts phone numbers from a given URL.
It prompts the user for a URL, fetches the content of the webpage,
and uses a regular expression to find and print all unique phone numbers.
"""
import requests
import re

def extract_phone_numbers(url):
    """
    Extracts phone numbers from the content of a given URL.
    Args:
        url (str): The URL of the webpage to extract phone numbers from.
    Returns:
        set: A set of unique phone numbers found in the webpage content. If an error occurs during the request, returns an empty set.
    Raises:
        None: All exceptions are handled internally.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()

        phone_pattern = r'\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b'
        phones = re.findall(phone_pattern, response.text)

        return set(phones)
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return set()

if __name__ == "__main__":
    url = input("Enter the URL of the webpage: ")
    phones = extract_phone_numbers(url)
    print("Extracted phone numbers:")
    for phone in phones:
        print(phone)
