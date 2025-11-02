import requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup

def fetch_robots_txt(domain):
    try:
        response = requests.get(urljoin(domain, '/robots.txt'))
        response.raise_for_status()
        print(f"Robots.txt for {domain}:")
        return response.text.splitlines()
    except requests.RequestException as e:
        print(f"Error fetching robots.txt: {e}")
        return []

def parse_robots_txt(lines):
    disallowed_paths = []
    for line in lines:
        line = line.strip()
        if line.startswith('Disallow:'):
            path = line.split(':')[1].strip()
            disallowed_paths.append(path)
    return disallowed_paths

def fetch_sitemap(domain):
    try:
        response = requests.get(urljoin(domain, '/sitemap.xml'))
        response.raise_for_status()
        print(f"Sitemap for {domain}:")
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching sitemap.xml: {e}")
        return None

def parse_sitemap(xml_content):
    soup = BeautifulSoup(xml_content, 'xml')
    urls = [url.loc.text for url in soup.find_all('url')]
    return urls

def main():
    """
    Main function to scan a given domain for disallowed paths in robots.txt and URLs listed in sitemap.xml.
    Prompts the user to enter a domain, then:
    1. Fetches and parses the robots.txt file to extract disallowed paths and prints them.
    2. Fetches and parses the sitemap.xml file to extract URLs and prints them.
    Functions used:
    - fetch_robots_txt(domain): Fetches the robots.txt file from the domain.
    - parse_robots_txt(robots_lines): Parses the robots.txt lines to find disallowed paths.
    - fetch_sitemap(domain): Fetches the sitemap.xml file from the domain.
    - parse_sitemap(sitemap_content): Parses the sitemap.xml content to extract URLs.
    Prints results to the console.
    """
    domain = input("Enter the domain to scan (e.g., https://example.com): ")
    
    # Fetch and parse robots.txt
    robots_lines = fetch_robots_txt(domain)
    disallowed_paths = parse_robots_txt(robots_lines)
    
    if disallowed_paths:
        print("\nDisallowed paths from robots.txt:")
        for path in disallowed_paths:
            print(f"- {urljoin(domain, path)}")
    else:
        print("No disallowed paths found in robots.txt.")
    
    # Fetch and parse sitemap.xml
    sitemap_content = fetch_sitemap(domain)
    
    if sitemap_content:
        sitemap_urls = parse_sitemap(sitemap_content)
        print("\nURLs found in sitemap.xml:")
        for url in sitemap_urls:
            print(url)
    else:
        print("No sitemap.xml found or could not be fetched.")

if __name__ == '__main__':
    main()
