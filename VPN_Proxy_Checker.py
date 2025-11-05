"""
This script checks if a given IP address is associated with a VPN or proxy service
using the ProxyCheck.io API. It prompts the user for an IP address, queries the API,
and then prints whether the IP is a proxy, its risk score, geographical location,
and the full API response.
"""
import proxycheck
import os
from dotenv import load_dotenv
import json

load_dotenv()

def check_ip_vpn_proxy(ip):
    """
    Checks whether the given IP address is associated with a VPN or Proxy using the ProxyCheck.io API.
    Fetches information about the IP address, including VPN/proxy status, risk score, and geographical location.
    Prints the results in a clean, readable format.
    """
    api_key = os.getenv('proxy_check_api_key')
    client = proxycheck.Blocking(key=api_key)

    try:
        ip_info = client.ip(ip)

        # Check VPN/Proxy status
        if ip_info.proxy():
            print(f"[+] The IP {ip} is associated with a VPN or Proxy.")
        else:
            print(f"[-] The IP {ip} is not associated with a VPN or Proxy.")

        # Extract core details
        risk_score = ip_info.risk()
        latitude, longitude = ip_info.geological()

        # Convert IpModel object to dictionary
        data = ip_info.get()
        if hasattr(data, "__dict__"):
            data = data.__dict__

        print(f"Risk Score: {risk_score}")
        print(f"Location: Latitude {latitude}, Longitude {longitude}")

        print("\nFull Data:")
        print(json.dumps(data, indent=4))

    except Exception as e:
        print(f"Error fetching data for IP {ip}: {e}")
    finally:
        client.close()


def main():
    ip = input("Enter an IP address to check: ").strip()
    check_ip_vpn_proxy(ip)


if __name__ == "__main__":
    main()
