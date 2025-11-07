"""
This script queries the AlienVault OTX API to retrieve information about a given IP address.
It fetches both direct indicator pulses and search pulses related to the IP,
then prints the pulse count and details for each unique pulse.
"""
import os
import requests
from dotenv import load_dotenv

load_dotenv()

OTX_KEY = os.getenv("alienvault_api_key")

def get_otx(ip):
    pulses = []

    # 1️⃣ Get direct indicator pulses
    try:
        url = f"https://otx.alienvault.com/api/v1/indicators/IPv4/{ip}/general"
        headers = {"X-OTX-API-KEY": OTX_KEY}
        r = requests.get(url, headers=headers, timeout=10)
        r.raise_for_status()
        data = r.json()
        for p in data.get("pulse_info", {}).get("pulses", []):
            pulses.append({
                "name": p.get("name"),
                "description": p.get("description"),
                "adversary": p.get("adversary"),
                "tags": p.get("tags"),
                "created": p.get("created"),
                "link": p.get("references")[0] if p.get("references") else None
            })
    except Exception as e:
        print(f"Error fetching general indicator pulses: {e}")

    # 2️⃣ Search pulses (first page only)
    try:
        url = "https://otx.alienvault.com/api/v1/search/pulses"
        params = {"q": ip, "limit": 10, "page": 1}
        headers = {"X-OTX-API-KEY": OTX_KEY}
        r = requests.get(url, headers=headers, params=params, timeout=10)
        r.raise_for_status()
        data = r.json()
        for p in data.get("results", []):
            pulses.append({
                "name": p.get("name"),
                "description": p.get("description"),
                "adversary": p.get("adversary"),
                "tags": p.get("tags"),
                "created": p.get("created"),
                "link": p.get("references")[0] if p.get("references") else None
            })
    except Exception as e:
        print(f"Error fetching search pulses: {e}")

    # Remove duplicates by pulse name
    unique_pulses = {p['name']: p for p in pulses}.values()
    return {"pulse_count": len(unique_pulses), "pulses": list(unique_pulses)}

if __name__ == "__main__":
    test_ip = input("Enter an IP address to check OTX data: ").strip()
    result = get_otx(test_ip)
    print(f"OTX Data for {test_ip}:")
    print(f"Pulse Count: {result.get('pulse_count')}")
    for pulse in result.get("pulses", []):
        print(f"- {pulse['name']} | Adversary: {pulse['adversary']} | Tags: {', '.join(pulse['tags'] or [])} | Created: {pulse['created']} | Link: {pulse['link']}")
