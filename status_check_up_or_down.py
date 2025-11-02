import requests
"""
Checks the status of each URL in the 'links' list using HTTP GET requests.
If a URL returns a status code of 200 (OK), it is added to 'new_link_list'.
Any exceptions during the request are caught and printed with the corresponding URL.
Finally, prints the list of URLs that are up (status code 200).
"""

links = []

new_link_list = []

for link in links:
    try:
        status = requests.get(link).status_code
        if status == 200:
            new_link_list.append(link)
    except requests.exceptions.RequestException as e:
        print(f"Error occurred with {link}: {e}")

print(new_link_list)
