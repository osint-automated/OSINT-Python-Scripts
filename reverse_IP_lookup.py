import ipaddress
import socket
import requests
import os
import csv
from dotenv import load_dotenv
from datetime import datetime, timezone

# Load environment variables from .env if present
load_dotenv()

# Configuration
API_KEY = os.getenv("viewdns_api_key")  # set this in your .env file (optional)
REQUEST_TIMEOUT = 10  # seconds for API requests
MAX_RESULTS = 50      # maximum number of domains to return/display per IP
EXPORT_CSV = True
EXPORT_CSV_PATH = "reverse_ip_results.csv"


def is_valid_ip(ip: str) -> bool:
    """Return True if ip is a valid IPv4 or IPv6 address."""
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False


def reverse_lookup(ip: str) -> str | None:
    """Perform reverse DNS lookup. Return hostname or None."""
    try:
        hostname, _, _ = socket.gethostbyaddr(ip)
        return hostname
    except (socket.herror, socket.gaierror, OSError):
        return None
    except Exception:
        return None


def get_websites_on_server(ip: str, api_key: str | None = None) -> list:
    """Query the ViewDNS reverseip API and return list of domains."""
    if not api_key:
        return []

    url = f"https://api.viewdns.info/reverseip/?host={ip}&apikey={api_key}&output=json"
    try:
        resp = requests.get(url, timeout=REQUEST_TIMEOUT)
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"  [!] Network/API error while querying ViewDNS for {ip}: {e}")
        return []

    try:
        data = resp.json()
    except ValueError:
        print(f"  [!] Failed to parse JSON response from ViewDNS for {ip}.")
        return []

    domains = []
    response_obj = data.get("response") if isinstance(data, dict) else None
    if isinstance(response_obj, dict):
        domains = response_obj.get("domains") or []

    if not isinstance(domains, list):
        return []

    return domains


def process_single_ip(ip: str, api_key: str | None = None) -> dict:
    """Process a single IP: validate, reverse DNS, optionally query ViewDNS."""
    result = {
        "ip": ip,
        "valid": False,
        "reverse_hostname": None,
        "other_domains": [],
        "error": None,
        "timestamp": datetime.now(timezone.utc).isoformat()  # timezone-aware UTC
    }

    if not is_valid_ip(ip):
        result["error"] = "Invalid IP"
        return result

    result["valid"] = True

    hostname = reverse_lookup(ip)
    if hostname:
        result["reverse_hostname"] = hostname

    if api_key:
        domains = get_websites_on_server(ip, api_key)
        if domains:
            result["other_domains"] = domains[:MAX_RESULTS]
        else:
            result["other_domains"] = []

    return result


def read_input_entries(user_input: str) -> list:
    """Return list of IPs from file or a single IP."""
    candidate = user_input.strip().strip('"').strip("'")
    if os.path.isfile(candidate):
        try:
            with open(candidate, "r", encoding="utf-8") as fh:
                lines = [line.strip() for line in fh if line.strip()]
                return lines
        except Exception as e:
            print(f"[!] Failed to read file {candidate}: {e}")
            return []
    return [candidate]


def export_results_to_csv(results: list, path: str) -> None:
    """Export results to CSV."""
    if not results:
        print("[*] No results to export.")
        return

    fieldnames = ["ip", "valid", "reverse_hostname", "other_domains", "error", "timestamp"]
    try:
        with open(path, "w", encoding="utf-8", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for r in results:
                writer.writerow({
                    "ip": r.get("ip", ""),
                    "valid": r.get("valid", False),
                    "reverse_hostname": r.get("reverse_hostname") or "",
                    "other_domains": ";".join(r.get("other_domains", [])),
                    "error": r.get("error") or "",
                    "timestamp": r.get("timestamp", "")
                })
        print(f"[*] Results exported to CSV: {os.path.abspath(path)}")
    except Exception as e:
        print(f"[!] Failed to write CSV to {path}: {e}")


def main():
    print("Reverse IP lookup tool")
    print("----------------------")
    print("You can enter a single IP address, or a path to a text file containing one IP per line.")
    user_input = input("Enter IP or path to file: ").strip()
    if not user_input:
        print("No input provided. Exiting.")
        return

    entries = read_input_entries(user_input)
    if not entries:
        print("No valid entries to process. Exiting.")
        return

    if not API_KEY:
        print("Note: ViewDNS API key not found. ViewDNS queries will be skipped.")
        print("Set 'viewdns_api_key' in a .env file or environment to enable ViewDNS.")

    results = []
    for idx, entry in enumerate(entries, start=1):
        print(f"\nProcessing {idx}/{len(entries)}: {entry}")
        res = process_single_ip(entry, API_KEY)
        results.append(res)

        if not res["valid"]:
            print(f"  [-] '{entry}' is not a valid IP address.")
            continue

        if res["reverse_hostname"]:
            print(f"  [+] Reverse DNS: {res['reverse_hostname']}")
        else:
            print(f"  [-] No reverse DNS hostname found for {entry}")

        if API_KEY:
            if res["other_domains"]:
                print(f"  [+] Other domains on the same server (showing up to {MAX_RESULTS}):")
                for d in res["other_domains"]:
                    print(f"    - {d}")
            else:
                print("  [-] No other domains found (or ViewDNS returned none).")

    if EXPORT_CSV:
        export_results_to_csv(results, EXPORT_CSV_PATH)

    print("\nDone.")


if __name__ == "__main__":
    main()