import pandas as pd
import requests

def victim_search_by_group(ransomware_group):
    base_url = 'https://api.ransomware.live/v2'
    search_url = f'/groupvictims/{ransomware_group}'
    url = base_url + search_url
    response = requests.get(url).json()
    return response


if __name__ == '__main__':
    ransomware_group = input('Enter ransomware group here: ')
    victim_search_by_group(ransomware_group)
    df = pd.DataFrame(victim_search_by_group(ransomware_group))
    df.to_csv(f'{ransomware_group}_victims.csv', index=False)
    print(f'CSV File created for {ransomware_group}')