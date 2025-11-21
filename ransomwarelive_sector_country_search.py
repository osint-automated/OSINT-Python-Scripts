import requests
import pandas as pd

class RasomwareLiveAPI():
    def __init__(self):
        self.name = 'RansomwareLive'

    def ransomware_attack_sector_gb(self, sector):
        #this is the ransomware live call for sectors in United Kingdom
        base_url = 'https://api.ransomware.live/v2'
        search_url = f'/sectorvictims/{sector}/gb'
        url = base_url + search_url
        response = requests.get(url).json()
        for item in response:
            sector = item['activity']
            victim = item['victim']
            date = item['attackdate']
            claim_url = item['claim_url']
            country = item['country']
            description = item['description']
            rasomware_group = item['group']

            #user can print to console if they wish

            #print(f'Sector: {sector}')
            #print(f'Victim: {victim}')
            #print(f'Date: {date}')
            #print(f'Claim URL: {claim_url}')
            #print(f'Country: {country}')
            #print(f'Description: {description}')
            #print(f'Ransomware Group: {rasomware_group}\n')

        return response
    
    def ransomware_attack_sector_us(self, sector):
        #this is the ransomware live call for sectors in United States
        base_url = 'https://api.ransomware.live/v2'
        search_url = f'/sectorvictims/{sector}/us'
        url = base_url + search_url
        response = requests.get(url).json()
        for item in response:
            sector = item['activity']
            victim = item['victim']
            date = item['attackdate']
            claim_url = item['claim_url']
            country = item['country']
            description = item['description']
            rasomware_group = item['group']

            #user can print to console if they wish

            #print(f'Sector: {sector}')
            #print(f'Victim: {victim}')
            #print(f'Date: {date}')
            #print(f'Claim URL: {claim_url}')
            #print(f'Country: {country}')
            #print(f'Description: {description}')
            #print(f'Ransomware Group: {rasomware_group}\n')

        return response
    
    def ransomware_attack_sector_au(self, sector):
        #this is the ransomware live call for sectors in Australia
        base_url = 'https://api.ransomware.live/v2'
        search_url = f'/sectorvictims/{sector}/au'
        url = base_url + search_url
        response = requests.get(url).json()
        for item in response:
            sector = item['activity']
            victim = item['victim']
            date = item['attackdate']
            claim_url = item['claim_url']
            country = item['country']
            description = item['description']
            rasomware_group = item['group']

            #user can print to console if they wish

            #print(f'Sector: {sector}')
            #print(f'Victim: {victim}')
            #print(f'Date: {date}')
            #print(f'Claim URL: {claim_url}')
            #print(f'Country: {country}')
            #print(f'Description: {description}')
            #print(f'Ransomware Group: {rasomware_group}\n')

        return response

if __name__ == '__main__':
    sector = 'healthcare'
    ransomware = RasomwareLiveAPI()

    uk_results = ransomware.ransomware_attack_sector_gb(sector=sector)
    uk_df = pd.DataFrame(uk_results)
    uk_df.to_csv(f'{sector}_uk.csv', index=False)
    print(f'CSV File created for UK {sector}')

    us_results = ransomware.ransomware_attack_sector_us(sector=sector)
    us_df = pd.DataFrame(us_results)
    us_df.to_csv(f'{sector}_us.csv', index=False)
    print(f'CSV File created for US {sector}')

    au_results = ransomware.ransomware_attack_sector_au(sector=sector)
    au_df = pd.DataFrame(au_results)
    au_df.to_csv(f'{sector}_au.csv', index=False)
    print(f'CSV File created for AU {sector}')