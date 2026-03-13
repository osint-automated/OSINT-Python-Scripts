from scholarly import scholarly

def google_scholar_search(search):
    search_query = scholarly.search_pubs(search)
    for article in search_query:
        year = article['pub_year']

        if year == 'NA':
            continue

        if int(article['bib']['pub_year']) >= int(date):
            print(f'Author: {article["bib"]["author"][0]}')
            print(f'Title: {article["bib"]["title"]}')
            print(f'Publication Year: {article["bib"]["pub_year"]}')
            print(f'Abstract: {article["bib"]["abstract"]}')
            print(f'Source: {article["pub_url"]}')
            print('-' *30)

if __name__ == '__main__':
    search = input('Enter your search query: ')
    date = input('Enter the oldest publication year to filter results: (e.g. 2025) ')
    google_scholar_search(search)