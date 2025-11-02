import requests
import os
from dotenv import load_dotenv

load_dotenv()

def greynoise_ip_lookup(ip_addr):
  """
  Queries the GreyNoise Community API for information about a given IP address.

  Args:
    ip_addr (str): The IP address to look up.

  Returns:
    None. Prints the API response text to the console.

  Note:
    Requires a valid GreyNoise API key assigned to the variable `api_key`.
    The `requests` library must be imported.
  """
  url = f"https://api.greynoise.io/v3/community/{ip_addr}"
  headers = {
  'key': api_key
  }
  response = requests.request("GET", url, headers=headers)
  print(response.text)

if __name__ == '__main__':
  api_key = os.getenv('greynoise_api_key')
  ip_addr = input('Enter IP address here: ')
  results = greynoise_ip_lookup(ip_addr)
  print(results)