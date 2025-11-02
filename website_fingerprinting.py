import requests

def get_headers(url):
    """
    Fetches the HTTP headers from the specified URL.

    Args:
        url (str): The URL to send the GET request to.

    Returns:
        dict or None: A dictionary of HTTP response headers if the request is successful,
        otherwise None if an exception occurs.

    Raises:
        None: All exceptions are handled internally.
    """
    try:
        response = requests.get(url)
        return response.headers
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def analyze_headers(headers):
    server = headers.get('Server', 'Unknown')
    powered_by = headers.get('X-Powered-By', 'Unknown')
    return {'Server': server, 'X-Powered-By': powered_by}

if __name__ == "__main__":
    url = input('Enter URL here: ')
    headers = get_headers(url)
    if headers:
        analysis = analyze_headers(headers)
        print(f"Analysis for {url}: {analysis}")
