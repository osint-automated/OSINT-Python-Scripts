from shodan import Shodan
import os
from dotenv import load_dotenv

load_dotenv()

"""
This script allows the user to search for information about a specific IP address using the Shodan API.

Steps:
1. Prompts the user to enter their Shodan API key.
2. Initializes the Shodan API client with the provided key.
3. Prompts the user to enter an IP address.
4. Retrieves and prints information about the specified IP address from Shodan.

Requirements:
- The 'shodan' Python package must be installed.
- A valid Shodan API key is required.

Usage:
Run the script and follow the prompts to enter your API key and the IP address you wish to search.
"""

api_key = os.getenv('shodan_api_key')

api = Shodan(api_key)
ip_addr = input('Enter IP Adrress here: ')
print(api.host(f'{ip_addr}'))