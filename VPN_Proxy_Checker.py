import proxycheck
import os
from dotenv import load_dotenv

load_dotenv()

def check_ip_vpn_proxy(ip):
    """
    Checks whether the given IP address is associated with a VPN or Proxy using the ProxyCheck.io API.
    Prompts the user for a ProxyCheck.io API key (optional; free tier available).
    Fetches information about the IP address, including VPN/proxy status, risk score, and geographical location.
    Prints the results to the console.
    Args:
        ip (str): The IP address to check.
    Raises:
        Exception: If there is an error fetching data from the API.
    Note:
        Requires the 'proxycheck' library.
    """
    api_key = os.getenv('proxy_check_api_key')
    client = proxycheck.Blocking(key=api_key)

    try:
        ip_info = client.ip(ip)
        if ip_info.proxy():
            print(f"[+] The IP {ip} is associated with a VPN or Proxy.")
        else:
            print(f"[-] The IP {ip} is not associated with a VPN or Proxy.")
        
        risk_score = ip_info.risk()
        latitude, longitude = ip_info.geological()
        data = ip_info.get()

        print(f"Risk Score: {risk_score}")
        print(f"Location: Latitude {latitude}, Longitude {longitude}")
        print(f"Full Data: {data}")
    
    except Exception as e:
        print(f"Error fetching data for IP {ip}: {e}")
    finally:
        client.close()

def main():
    ip = input("Enter an IP address to check: ").strip()
    check_ip_vpn_proxy(ip)

if __name__ == "__main__":
    main()
