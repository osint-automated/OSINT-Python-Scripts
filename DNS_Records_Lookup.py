import dns.resolver
import sys

def get_dns_records(domain):
    """
    Retrieves DNS records for a given domain.
    Args:
        domain (str): The domain name to query DNS records for.
    Returns:
        dict: A dictionary containing DNS records with the following keys:
            - 'A': List of IPv4 addresses (or None if not found).
            - 'MX': List of tuples (preference, exchange) for mail servers (or None if not found).
            - 'NS': List of name server hostnames (or None if not found).
            - 'TXT': List of TXT record strings (or None if not found).
    Exceptions:
        Handles dns.resolver.NoAnswer and dns.resolver.NXDOMAIN exceptions for each record type,
        setting the corresponding value to None if the record is not found.
    """
    records = {}
    try:
        # A Records
        records['A'] = [r.address for r in dns.resolver.resolve(domain, 'A')]
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
        records['A'] = None

    try:
        # MX Records
        records['MX'] = [(r.preference, r.exchange.to_text()) for r in dns.resolver.resolve(domain, 'MX')]
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
        records['MX'] = None

    try:
        # NS Records
        records['NS'] = [r.to_text() for r in dns.resolver.resolve(domain, 'NS')]
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
        records['NS'] = None

    try:
        # TXT Records
        records['TXT'] = [r.to_text() for r in dns.resolver.resolve(domain, 'TXT')]
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
        records['TXT'] = None

    return records

def display_records(domain, records):
    print(f"DNS Records for {domain}:")
    for record_type, values in records.items():
        if values:
            print(f"{record_type} Records:")
            for value in values:
                print(f"  - {value}")
        else:
            print(f"{record_type} Records: No records found.")

def main():
    domain = input("Enter a domain name: ").strip()
    records = get_dns_records(domain)
    display_records(domain, records)

if __name__ == "__main__":
    main()
