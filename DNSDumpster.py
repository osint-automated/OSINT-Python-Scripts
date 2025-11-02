import subprocess
import json
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('dnsdumpster_api_key')
domain = input('Enter target domain here: ')

response = subprocess.check_output(
    f'curl -s -H "X-API-Key: {api_key}" https://api.dnsdumpster.com/domain/{domain}',
    shell=True
)

data = json.loads(response.decode('utf-8'))

def extract_ips(d):
    """
    Recursively extracts all IP addresses from a nested dictionary or list structure.

    Args:
        d (dict or list): The input data structure containing IP addresses. It can be a dictionary or a list,
            potentially nested, where dictionaries may contain a key 'ips' with a list of dictionaries
            each having an 'ip' key.

    Returns:
        list: A list of all IP addresses (as strings) found within the input structure.
    """
    ips = []
    if isinstance(d, dict):
        if 'ips' in d:
            ips.extend(ip['ip'] for ip in d['ips'] if 'ip' in ip)
        for value in d.values():
            ips.extend(extract_ips(value))
    elif isinstance(d, list):
        for item in d:
            ips.extend(extract_ips(item))
    return ips

ips = list(set(extract_ips(data)))

for ip in ips:
    print(ip)
