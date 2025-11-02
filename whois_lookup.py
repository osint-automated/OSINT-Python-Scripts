import whois
import socket
import re

def is_valid_ip(ip):
    ip_pattern = re.compile(r'^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$')
    return re.match(ip_pattern, ip) is not None

def get_whois_info(identifier):
    """
    Retrieves and displays WHOIS information for a given identifier, which can be either an IP address or a domain name.
    Parameters:
        identifier (str): The IP address or domain name to look up.
    Behavior:
        - If the identifier is a valid IP address, prints WHOIS information related to the IP.
        - If the identifier is a domain name, prints WHOIS information related to the domain.
        - Handles and prints errors if WHOIS information cannot be retrieved.
    Printed Information:
        For IP addresses:
            - IP Address
            - Domain (if available)
            - Registrar (if available)
            - Name Servers (if available)
            - Status (if available)
        For domain names:
            - Domain
            - Registrar
            - Creation Date
            - Expiration Date
            - Updated Date
            - Name Servers
            - Status
            - Email
    Exceptions:
        Prints an error message if WHOIS information retrieval fails.
    """
    try:
        if is_valid_ip(identifier):
            ip_info = whois.whois(identifier)
            print(f"IP Address: {identifier}")
            print(f"Domain: {ip_info.domain if ip_info.domain else 'N/A'}")
            print(f"Registrar: {ip_info.registrar if ip_info.registrar else 'N/A'}")
            print(f"Name Servers: {', '.join(ip_info.name_servers) if ip_info.name_servers else 'N/A'}")
            print(f"Status: {', '.join(ip_info.status) if ip_info.status else 'N/A'}")
        else:
            domain_info = whois.whois(identifier)
            print(f"Domain: {domain_info.domain if domain_info.domain else 'N/A'}")
            print(f"Registrar: {domain_info.registrar if domain_info.registrar else 'N/A'}")
            print(f"Creation Date: {domain_info.creation_date if domain_info.creation_date else 'N/A'}")
            print(f"Expiration Date: {domain_info.expiration_date if domain_info.expiration_date else 'N/A'}")
            print(f"Updated Date: {domain_info.updated_date if domain_info.updated_date else 'N/A'}")
            print(f"Name Servers: {', '.join(domain_info.name_servers) if domain_info.name_servers else 'N/A'}")
            print(f"Status: {', '.join(domain_info.status) if domain_info.status else 'N/A'}")
            print(f"Email: {domain_info.emails if domain_info.emails else 'N/A'}")

    except Exception as e:
        print(f"Error retrieving WHOIS information for {identifier}: {e}")

if __name__ == "__main__":
    identifier = input("Enter a domain name or IP address (e.g., example.com or 192.168.1.1): ")
    get_whois_info(identifier)
