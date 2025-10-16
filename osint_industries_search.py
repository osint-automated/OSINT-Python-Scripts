import requests

def email_search(email):
  url = f"https://api.osint.industries/v2/request?type=email&query={email}&timeout=60"
  headers = {
      "api-key": api_key,
      "accept": "application/json"
  }
  response = requests.get(url, headers=headers)
  print(response.text)

def phone_search():
  url = f"https://api.osint.industries/v2/request?type=phone&query={phone}&timeout=60"
  headers = {
      "api-key": api_key,
      "accept": "application/json"
  }
  response = requests.get(url, headers=headers)
  print(response.text)

def username_search(username):
  url = f"https://api.osint.industries/v2/request?type=username&query={username}&timeout=60"
  headers = {
      "api-key": api_key,
      "accept": "application/json"
  }
  response = requests.get(url, headers=headers)
  print(response.text)

def name_search(name):
  url = f"https://api.osint.industries/v2/request?type=name&query={name}&timeout=60"
  headers = {
      "api-key": api_key,
      "accept": "application/json"
  }
  response = requests.get(url, headers=headers)
  print(response.text)

def wallet_search(wallet):
  url = f"https://api.osint.industries/v2/request?type=wallet&query={wallet}&timeout=60"
  headers = {
      "api-key": api_key,
      "accept": "application/json"
  }
  response = requests.get(url, headers=headers)
  print(response.text)

api_key = 'XXX' #replace the XXX with your Osint Industries API key

'''
select which search you want to run and remove the comments to run it.
'''

#email = input('Enter email here: ')
#phone = input('Enter phone number here: ')
#username = input('Enter username here: ')
#name = input('Enter name here: ')
#wallet = input('Enter wallet address here: ')

#email_search(email)
#phone_search()
#username_search(username)
#name_search(name)
#wallet_search(wallet)