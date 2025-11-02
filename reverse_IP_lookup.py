import ipaddress
import socket
import requests

API_KEY = input("Enter your ViewDNS API key: ").strip()

def is_valid_ip(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

def reverse_lookup(ip):
    try:
        domain = socket.gethostbyaddr(ip)[0]
        return domain
    except socket.herror:
        return None

def get_websites_on_server(ip):
    url = f"https://api.viewdns.info/reverseip/?host={ip}&apikey={API_KEY}&output=json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if "response" in data and "domains" in data["response"]:
            websites = data["response"]["domains"]
            return websites
    return []

def main():
    """
    Main function for reverse IP lookup tool.
    Prompts the user to enter an IP address, validates the input, and performs a reverse DNS lookup to find the associated domain.
    If a domain is found, optionally displays all websites hosted on the same server as the provided IP address.
    Workflow:
    - Prompts for IP address input.
    - Validates the IP address format.
    - Performs reverse DNS lookup to find the domain.
    - If a domain is found, asks the user if they want to see all websites on the same server.
    - Displays the list of websites if requested.
    Returns:
        None
    """
    ip = input("Enter an IP address: ").strip()
    if not is_valid_ip(ip):
        print(f"[-] Invalid IP address: {ip}")
        return

    domain = reverse_lookup(ip)
    if domain:
        print(f"[+] IP: {ip}, Domain: {domain}")
        show_all = input("Do you want to see all websites on the same server? (yes/no): ").strip().lower() == 'yes'
        
        if show_all:
            websites = get_websites_on_server(ip)
            if websites:
                print("\nOther websites on the same server:")
                for website in websites:
                    print(f"[+] {website}")
                print('\n')
            else:
                print("[-] No other websites found on the same server.")
    else:
        print(f"[-] No domain found for IP: {ip}")

if __name__ == "__main__":
    main()
