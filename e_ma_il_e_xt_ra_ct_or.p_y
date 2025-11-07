"""
This script extracts email addresses from a given URL.
It prompts the user for a URL, fetches the content of the webpage,
and uses a regular expression to find and print all unique email addresses.
"""
import requests
import re

def extract_emails(url):
    """
    Extracts email addresses from the content of a given URL.
    Args:
        url (str): The URL of the webpage to extract emails from.
    Returns:
        set: A set of unique email addresses found in the webpage content.
        If an error occurs during the request, returns an empty list.
    Raises:
        None. Exceptions are caught and handled internally.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()

        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        emails = re.findall(email_pattern, response.text)

        return set(emails)
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return []

if __name__ == "__main__":
    url = input("Enter the URL of the webpage: ")
    emails = extract_emails(url)
    print("Extracted email addresses:")
    for email in emails:
        print(email)
