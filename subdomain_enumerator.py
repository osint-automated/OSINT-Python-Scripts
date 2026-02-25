import requests
import json
import sys

def get_subdomains(domain):
    url = f"https://crt.sh/?q=%25.{domain}&output=json"

    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"[!] Error fetching data: {e}")
        sys.exit(1)

    try:
        data = response.json()
    except json.JSONDecodeError:
        print("[!] Failed to decode JSON response")
        sys.exit(1)

    subdomains = set()

    for entry in data:
        name_value = entry.get("name_value", "")
        # crt.sh sometimes returns multiple domains separated by newline
        for sub in name_value.split("\n"):
            if sub.endswith(domain):
                subdomains.add(sub.strip())

    return sorted(subdomains)


def main():
    domain = input("Enter target domain (example.com): ").strip()

    if not domain:
        print("[!] Please enter a valid domain.")
        return

    print(f"\n[+] Enumerating subdomains for: {domain}\n")

    subdomains = get_subdomains(domain)

    if subdomains:
        for sub in subdomains:
            print(sub)

        with open(f"{domain}_subdomains.txt", "w") as f:
            for sub in subdomains:
                f.write(sub + "\n")

    else:
        print("[-] No subdomains found.")


if __name__ == "__main__":
    main()