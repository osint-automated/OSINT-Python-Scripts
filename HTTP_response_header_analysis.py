import requests

def analyze_headers(url):
    """
    Fetches and analyzes HTTP response headers from the specified URL.
    Makes a GET request to the provided URL, prints all response headers,
    and provides additional analysis for specific security-related headers:
    'Server', 'X-Frame-Options', and 'Content-Security-Policy'.
    Args:
        url (str): The URL to fetch and analyze headers from.
    Raises:
        requests.exceptions.RequestException: If there is an error fetching the URL.
    Prints:
        - All HTTP response headers.
        - Values for 'Server', 'X-Frame-Options', and 'Content-Security-Policy' headers.
        - Error message if the request fails.
    """
    try:
        response = requests.get(url)
        headers = response.headers

        print(f"HTTP Response Headers for {url}:\n")
        for header, value in headers.items():
            print(f"{header}: {value}")
        
        # Additional Analysis
        print("\nAnalysis:")
        server_type = headers.get('Server', 'Not specified')
        x_frame_options = headers.get('X-Frame-Options', 'Not specified')
        content_security_policy = headers.get('Content-Security-Policy', 'Not specified')
        
        print(f"\nServer Type: {server_type}")
        print(f"X-Frame-Options: {x_frame_options}")
        print(f"Content Security Policy: {content_security_policy}")
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")

def main():
    url = input("Enter a URL (including http:// or https://): ").strip()
    analyze_headers(url)

if __name__ == "__main__":
    main()
