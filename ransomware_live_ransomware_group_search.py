import requests
import pandas as pd

def ransomware_group_search(ransomware_group):
    base_url = 'https://api.ransomware.live/v2'
    url = f'{base_url}/group/{ransomware_group}'
    response = requests.get(url).json()

    # --- Extract: Name ---
    name = response.get("name")

    # --- Extract: Description ---
    description = response.get("description")

    # --- Extract: Active .onion URLs ---
    active_onions = [
        loc.get("fqdn")
        for loc in response.get("locations", [])
        if loc.get("available") is True and loc.get("fqdn", "").endswith(".onion")
    ]

    # --- Extract: Tools Used ---
    tools_section = response.get("tools", [])
    tools_used = tools_section[0] if tools_section else {}

    # Flatten for DataFrame (convert lists/dicts to strings)
    return {
        "name": name,
        "description": description,
        "active_onions": ", ".join(active_onions),
        "tools_used": ", ".join(
            f"{category}: {', '.join(tools)}" for category, tools in tools_used.items()
        )
    }


if __name__ == '__main__':
    ransomware_group = input('Enter ransomware group here: ')
    data = ransomware_group_search(ransomware_group)
    df = pd.DataFrame([data])
    df.to_csv(f'{ransomware_group}.csv', index=False)
    print(f'CSV File created for {ransomware_group}')
