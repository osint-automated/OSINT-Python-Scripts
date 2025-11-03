import whois
import ipaddress

def is_valid_ip(ip: str) -> bool:
    """Check if the input is a valid IPv4 or IPv6 address."""
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

def safe_join(value):
    """Convert a list or string to a single readable string."""
    if isinstance(value, list):
        return ', '.join(str(v) for v in value)
    elif isinstance(value, str):
        return value
    return 'N/A'

def format_date(value):
    """Safely format creation/expiration/updated dates from WHOIS."""
    if isinstance(value, list):
        return str(value[0]) if value else 'N/A'
    return str(value) if value else 'N/A'

def get_whois_info(identifier: str):
    """
    Retrieves and displays WHOIS information for a domain or IP.
    For IPs, queries WHOIS, though results may be limited.
    """
    try:
        data = whois.whois(identifier)
        if is_valid_ip(identifier):
            print(f"IP Address: {identifier}")
            print(f"Domain: {safe_join(getattr(data, 'domain', 'N/A'))}")
            print(f"Registrar: {getattr(data, 'registrar', 'N/A')}")
            print(f"Name Servers: {safe_join(getattr(data, 'name_servers', 'N/A'))}")
            print(f"Status: {safe_join(getattr(data, 'status', 'N/A'))}")
        else:
            print(f"Domain: {safe_join(getattr(data, 'domain', 'N/A'))}")
            print(f"Registrar: {getattr(data, 'registrar', 'N/A')}")
            print(f"Creation Date: {format_date(getattr(data, 'creation_date', 'N/A'))}")
            print(f"Expiration Date: {format_date(getattr(data, 'expiration_date', 'N/A'))}")
            print(f"Updated Date: {format_date(getattr(data, 'updated_date', 'N/A'))}")
            print(f"Name Servers: {safe_join(getattr(data, 'name_servers', 'N/A'))}")
            print(f"Status: {safe_join(getattr(data, 'status', 'N/A'))}")
            print(f"Emails: {safe_join(getattr(data, 'emails', 'N/A'))}")
    except Exception as e:
        print(f"Error retrieving WHOIS information for {identifier}: {e}")

if __name__ == "__main__":
    identifier = input("Enter a domain name or IP address (e.g., example.com or 8.8.8.8): ").strip()
    get_whois_info(identifier)
