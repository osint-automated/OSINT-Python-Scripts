import requests

def get_headers(url):
    """
    Fetches the HTTP headers from the specified URL.

    Args:
        url (str): The URL to send the GET request to.

    Returns:
        dict or None: A dictionary of HTTP response headers if the request is successful,
        otherwise None if an exception occurs.
    """
    try:
        # Ensure URL has a scheme
        if not url.startswith(("http://", "https://")):
            url = "https://" + url
        
        response = requests.get(url, timeout=10)
        print(f"Status Code: {response.status_code}")
        return response.headers

    except requests.exceptions.MissingSchema:
        print("Invalid URL. Please include a valid domain or protocol.")
    except requests.exceptions.Timeout:
        print("Request timed out.")
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
    
    return None


def analyze_headers(headers):
    """
    Extracts key security-related and server-related HTTP headers.

    Args:
        headers (dict): The HTTP response headers.

    Returns:
        dict: Analysis results of relevant headers.
    """
    analysis = {
        'Server': headers.get('Server', 'Unknown'),
        'X-Powered-By': headers.get('X-Powered-By', 'Unknown'),
        'Content-Type': headers.get('Content-Type', 'Unknown'),
        'Strict-Transport-Security': headers.get('Strict-Transport-Security', 'Not Set'),
        'X-Frame-Options': headers.get('X-Frame-Options', 'Not Set'),
        'X-Content-Type-Options': headers.get('X-Content-Type-Options', 'Not Set'),
        'Referrer-Policy': headers.get('Referrer-Policy', 'Not Set'),
        'Content-Security-Policy': headers.get('Content-Security-Policy', 'Not Set'),
        'Permissions-Policy': headers.get('Permissions-Policy', 'Not Set')
    }
    return analysis


if __name__ == "__main__":
    url = input('Enter URL here: ').strip()
    headers = get_headers(url)
    if headers:
        analysis = analyze_headers(headers)
        print("\n--- HTTP Header Analysis ---")
        for key, value in analysis.items():
            print(f"{key}: {value}")
