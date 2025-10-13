import requests
"""
This script queries the VirusTotal API for information about a specified IP address.

Prompts the user for:
    - VirusTotal API key
    - IP address to look up

Sends a GET request to the VirusTotal API and prints the JSON response.

Requirements:
    - requests library
    - Valid VirusTotal API key

Usage:
    Run the script and follow the prompts to enter your API key and the IP address.

Note:
    The response is printed as raw JSON text.
"""

api_key = input("Enter your VirusTotal API key: ")
ip_addr = input('Enter IP address here: ')

url = f"https://www.virustotal.com/api/v3/ip_addresses/{ip_addr}"

headers = {
    "accept": "application/json",
    "x-apikey": api_key
}

response = requests.get(url, headers=headers)
data = response.text
print(data)

