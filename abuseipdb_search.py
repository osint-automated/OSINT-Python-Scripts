import requests
import os
from dotenv import load_dotenv
import json
"""
This script queries the AbuseIPDB API to check the reputation of a given IP address.

Prompts the user for an IP address and an API key, then sends a GET request to the AbuseIPDB API.
Displays the JSON response containing information about the IP address, such as abuse reports and reputation.

Requirements:
    - requests
    - json

Usage:
    Run the script and follow the prompts to enter the IP address and API key.

API Reference:
    https://www.abuseipdb.com/api

Inputs:
    - IP address to check
    - AbuseIPDB API key

Outputs:
    - Pretty-printed JSON response from the API
"""


url = 'https://api.abuseipdb.com/api/v2/check'
ip_addr = input("Enter IP Address: ")
API_KEY = os.getenv('abuseipdb_api_key')

querystring = {
    'ipAddress': f'{ip_addr}',
    'maxAgeInDays': '90'
}

headers = {
    'Accept': 'application/json',
    'Key': f'{API_KEY}'
}

response = requests.request(method='GET', url=url, headers=headers, params=querystring)

decodedResponse = json.loads(response.text)
results = json.dumps(decodedResponse, sort_keys=True, indent=4)
print(results)