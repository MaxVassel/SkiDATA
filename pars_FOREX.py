import requests
from bs4 import BeautifulSoup as BS
import json

header = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'

}

url = 'http://www.x-rates.com/table/?from=EUR&amount=1'
src = requests.get(url, headers=header)
soup = BS(src.content, 'lxml')
pairs = soup.find(class_='tablesorter ratesTable').find('tbody').find_all('tr')
rates = []
for pair in pairs:
    currency = pair.find('td').text
    rate = pair.find('td').next_sibling.next_sibling.text
    Rates = {'Currency': currency, 'Rate': rate}
    rates.append(Rates)


with open('forex.json', 'w') as json_file:
    json.dump(rates, json_file, indent=4)
