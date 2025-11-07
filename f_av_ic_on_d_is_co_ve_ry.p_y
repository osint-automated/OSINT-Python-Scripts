"""
This script discovers domains that share the same favicon hash.
It takes a favicon hash as input, queries the Shodan API to find matching domains,
and then prints the list of related domains found. It can also resolve IP addresses
to domain names if direct hostnames are not available.
"""
import requests
import mmh3
import shodan
import sys
import socket
import os
from dotenv import load_dotenv

load_dotenv()

def resolve_ip_to_domain(ip_address):
    try:
        hostname, _, _ = socket.gethostbyaddr(ip_address)
        return hostname
    except socket.herror:
        return ip_address
    except Exception as e:
        print(f"Error resolving IP {ip_address}: {e}")
        return ip_address


def search_domains_by_favicon_hash(favicon_hash, api_key):
    if favicon_hash is None:
        return None

    try:
        api = shodan.Shodan(api_key)
        query = f'http.favicon.hash:{favicon_hash}'
        results = api.search(query)

        domains = []
        for result in results['matches']:
            if 'hostnames' in result and result['hostnames']:
                domains.extend(result['hostnames'])
            elif 'ip_str' in result:
                resolved_domain = resolve_ip_to_domain(result['ip_str'])
                domains.append(resolved_domain)

        return domains

    except shodan.APIError as e:
        print(f"Shodan API Error: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

def display_domains(domains):
    if domains and len(domains) > 0:
        print("Related domains found:")
        for domain in domains:
            print(domain)
    else:
        print("No related domains found.")

def main():
    shodan_api_key = os.getenv('shodan_api_key')

    predefined_favicon_hash = input('Enter favicon hash here: ') #get favicon hash from https://favicon-hash.kmsec.uk/

    print(f"Searching for domains with favicon hash: {predefined_favicon_hash}...")
    related_domains = search_domains_by_favicon_hash(predefined_favicon_hash, shodan_api_key)

    if related_domains is not None:
        display_domains(related_domains)
    else:
        print("Failed to search for related domains.")

if __name__ == "__main__":
    main()


