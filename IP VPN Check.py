import requests
"""
This script reads a list of IP addresses from a user-specified CSV file, checks each IP for VPN or proxy usage using the ip-api.com service, 
and writes the results to a new CSV file named 'results.csv'.
Features:
- Prompts the user for the input CSV filename.
- For each IP address, queries the ip-api.com API to determine if it is associated with a VPN, proxy, or hosting provider.
- Handles API errors and invalid IPs gracefully.
- Outputs results in a CSV file with columns: 'IP', 'VPN/Proxy'.
- Includes basic error handling for file operations and network requests.
Usage:
Run the script and enter the name of the CSV file containing IP addresses when prompted.
"""
import time
import csv

input_file = input('Enter csv file name here: ')
output_file = "results.csv"

try:
    with open(input_file, 'r', encoding='utf-8') as f_in, \
         open(output_file, 'w', newline='', encoding='utf-8') as f_out:

        reader = csv.reader(f_in)
        writer = csv.writer(f_out)
        
        writer.writerow(['IP', 'VPN/Proxy'])

        for row in reader:
            if not row or not row[0].strip():
                continue

            ip = row[0].strip()
            time.sleep(1.4)
            
            status = f"Failed: Could not connect"
            try:
                api_url = f"http://ip-api.com/json/{ip}?fields=status,message,proxy,hosting,query"
                response = requests.get(api_url, timeout=5)
                response.raise_for_status()
                data = response.json()

                if data.get("status") == "success":
                    is_proxy = data.get("proxy") or data.get("hosting")
                    status = "Yes" if is_proxy else "No"
                else:
                    status = f"Failed: {data.get('message', 'invalid IP')}"

            except requests.exceptions.RequestException as e:
                status = f"Failed: {e}"

            writer.writerow([ip, status])

    print(f"Processing complete. Results saved to '{output_file}'.")

except FileNotFoundError:
    print(f"Error: Input file '{input_file}' not found.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

