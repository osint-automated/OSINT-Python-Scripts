import requests
import os
import json
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()

"""
VirusTotal IP Lookup Script
---------------------------
Fetches and parses VirusTotal IP information and displays key details in a readable format.
"""

# Get API key and IP input
api_key = os.getenv('virus_total_api_key')
ip_addr = input('Enter IP address here: ').strip()

if not api_key:
    print("Missing VirusTotal API key. Please set 'virus_total_api_key' in your .env file.")
    exit(1)

url = f"https://www.virustotal.com/api/v3/ip_addresses/{ip_addr}"

headers = {
    "accept": "application/json",
    "x-apikey": api_key
}

# Send request
response = requests.get(url, headers=headers)

if response.status_code != 200:
    print(f"API request failed with status code {response.status_code}")
    print(response.text)
    exit(1)

data = response.json()
attrs = data.get("data", {}).get("attributes", {})

# Extract key fields
ip_id = data.get("data", {}).get("id")
country = attrs.get("country", "N/A")
asn = attrs.get("asn", "N/A")
owner = attrs.get("as_owner", "N/A")
reputation = attrs.get("reputation", "N/A")
network = attrs.get("network", "N/A")
registry = attrs.get("regional_internet_registry", "N/A")
votes = attrs.get("total_votes", {})
harmless = votes.get("harmless", 0)
malicious = votes.get("malicious", 0)

# HTTPS certificate info (if exists)
cert_info = attrs.get("last_https_certificate", {})
cert_subject = cert_info.get("subject", {}).get("CN", "N/A")
cert_issuer = cert_info.get("issuer", {}).get("CN", "N/A")
cert_validity = cert_info.get("validity", {})

# Crowd-sourced context
context = attrs.get("crowdsourced_context", [])
threats = []
for c in context:
    threats.append(f"- {c.get('title', 'Unknown')} ({c.get('severity', 'N/A')}): {c.get('details', '')}")

# Print formatted output
print("\n==================== VirusTotal IP Report ====================\n")
print(f"IP Address:         {ip_id}")
print(f"ASN Owner:          {owner}")
print(f"ASN:                {asn}")
print(f"Country:            {country}")
print(f"Network:            {network}")
print(f"Registry:           {registry}")
print(f"Reputation Score:   {reputation}")
print(f"Harmless Votes:     {harmless}")
print(f"Malicious Votes:    {malicious}")

if threats:
    print("\nThreat Intelligence:")
    for t in threats:
        print(t)
else:
    print("\nThreat Intelligence: None reported")

print("\nHTTPS Certificate Info:")
print(f"   Subject CN:      {cert_subject}")
print(f"   Issuer CN:       {cert_issuer}")
print(f"   Valid From:      {cert_validity.get('not_before', 'N/A')}")
print(f"   Valid Until:     {cert_validity.get('not_after', 'N/A')}")

print("\n==============================================================\n")
