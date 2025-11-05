"""
This script checks a list of IP addresses for VPN or proxy usage
using the proxycheck.io API. It reads a list of IPs from the `ip_list`
variable, queries the API for each IP, and prints whether it is a proxy or not.
"""
import proxycheck
import os
from dotenv import load_dotenv

load_dotenv()

def check_ip_vpn_proxy(ip):
    api_key = os.getenv("proxycheck_api_key")
    client = proxycheck.Blocking(key=api_key)

    try:
        ip_info = client.ip(ip)

        if ip_info.proxy():
            print(f"{ip} ----> Yes")
        else:
            print(f"{ip} ----> No")
            
    except Exception as e:
        print(f"Error fetching data for IP {ip}: {e}")
    finally:
        client.close()
        
def main():
    ip_list = [] #enter list of IPs here
    for ip in ip_list:
        check_ip_vpn_proxy(ip)

if __name__ == "__main__":
    main()