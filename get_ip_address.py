import subprocess
"""
This script prompts the user to enter a domain name (excluding protocol prefixes),
pings the domain for 5 seconds, and extracts the IP address from the ping output.
Steps:
1. Prompts user for a domain name.
2. Executes a ping command to the specified domain.
3. Waits for 5 seconds before terminating the ping process.
4. Captures and decodes the output from the ping command.
5. Uses a regular expression to extract the IP address from the output.
6. Prints the extracted IP address or an error message if not found.
Note:
- The script assumes the ping output contains the IP address in square brackets (e.g., [192.168.1.1]).
- Works on systems where the ping command outputs the IP address in this format.
"""
import time
import re

domain = input('Enter domain name here (exclude http://, https://): ')

ping_process = subprocess.Popen(['ping', domain], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

time.sleep(5)

ping_process.terminate()

output, error = ping_process.communicate()

output_str = output.decode()

ip_match = re.search(r'\[([^\]]+)\]', output_str)

if ip_match:
    ip_address = ip_match.group(1)
    print(ip_address)
else:
    print("IP address not found in the ping output.")
