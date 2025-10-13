import requests

def get_geolocation(ip):
    access_token = input('Enter your ipinfo.io access token: ')
    url = f'https://ipinfo.io/{ip}/json?token={access_token}'

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.RequestException as e:
        print(f"Error fetching data for IP {ip}: {e}")
        return None

def display_results(data):
    """
    Displays geolocation information from a provided data dictionary.

    Args:
        data (dict): A dictionary containing geolocation details such as IP, city, region, country, location, postal code, and ISP.
                     If None or empty, a message indicating no data found will be printed.

    Returns:
        None
    """
    if data:
        print("Geolocation Information:")
        print(f"IP: {data.get('ip', 'N/A')}")
        print(f"City: {data.get('city', 'N/A')}")
        print(f"Region: {data.get('region', 'N/A')}")
        print(f"Country: {data.get('country', 'N/A')}")
        print(f"Location: {data.get('loc', 'N/A')}")
        print(f"Postal Code: {data.get('postal', 'N/A')}")
        print(f"ISP: {data.get('org', 'N/A')}")
    else:
        print("No data found.")

if __name__ == "__main__":
    ip_address = input("Enter an IP address: ")
    geolocation_data = get_geolocation(ip_address)
    display_results(geolocation_data)
