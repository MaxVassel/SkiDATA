import requests
from bs4 import BeautifulSoup as BS
import json

# Сборка ссылок для парсера

urls = ['http://www.skiresort.info/ski-resorts']
i = 2
while i < 33:
    u = 'https://www.skiresort.info/ski-resorts/page/'+str(i)
    urls.append(u)
    i += 1
print(urls)
links = []
names = []
continents = []
countries = []
resort_list = []
header = {"Accept": "*/*",
          "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
          }
counter = 1

for url in urls:
    site = requests.get(url, headers=header)
    soup = BS(site.content, 'lxml')
    resorts = soup.find_all(class_='col-sm-11 col-xs-10')

# collecting info (continent, country, name, link)
    for resort in resorts:
        a = resort.find('a')
        resort_link = a.get('href')
        links.append(resort_link)
        resort_name = a.text.strip()
        names.append(resort_name)
        c = resort.find(class_="sub-breadcrumb").find('a').text.strip()
        continents.append(c)
        try:
            b = resort.find(
                class_="sub-breadcrumb").find('a').next_sibling.next_element.text.strip()
        except Exception:
            b = 'NaN'
        resort_card = requests.get(resort_link)
        soup = BS(resort_card.content, 'lxml')
# ALTITUDE DATA (Getting max and diff between max and min)

        try:
            altitude_max = soup.find(id='selAlti').text.strip().split(' ')[-5]
        except Exception:
            altitude_max = 'NaN'

        try:
            altitude_up = soup.find(id='selAlti').text.strip().split(' ')[-2]
        except Exception:
            altitude_up = 'NaN'

# # SLOPES DATA

        try:
            blue_slopes = soup.find(
                class_="table-graph-first").find(id='selBeginner').text
        except Exception:
            blue_slopes = 'NaN'

        try:
            red_slopes = soup.find(
                class_="table-graph-first").find(id='selInter').text
        except Exception:
            red_slopes = 'NaN'

        try:
            black_slopes = soup.find(
                class_="table-graph-first").find(id='selAdv').text
        except Exception:
            black_slopes = 'NaN'

# Ticket prices

        try:
            adult_skipass = soup.find(id='selTicketA').text.replace(
                '\u20ac ', 'EUR ').replace(
                '\xa5 ', 'Yen ').replace(',-', '').strip()
        except Exception:
            adult_skipass = 'NaN'

        try:
            young_skipass = soup.find(id='selTicketY').text.replace(
                '\u20ac ', '').replace(',-', '').replace('SFr ', '').replace(
                '\xa5 ', '').strip()
        except Exception:
            young_skipass = 'NaN'

        try:
            child_skipass = soup.find(id='selTicketC').text.replace(
                '\u20ac ', '').replace(',-', '').replace('SFr ', '').replace(
                '\xa5 ', '').strip()
        except Exception:
            child_skipass = 'NaN'

# Lift info

        try:
            lift_Tram_ropeway = soup.find(
                title="Aerial tramway/reversible ropeway").find(class_="lift-amount").text
        except Exception:
            lift_Tram_ropeway = 'NaN'
        try:
            lift_gondola = soup.find(
                title="Circulating ropeway/gondola lift").find(class_="lift-amount").text
        except Exception:
            lift_gondola = 'NaN'
        try:
            lift_chair = soup.find(
                title="Chairlift").find(class_="lift-amount").text
        except Exception:
            lift_chair = 'NaN'
        try:
            lift_Tbar = soup.find(
                title="T-bar lift/platter/button lift").find(class_="lift-amount").text
        except Exception:
            lift_Tbar = 'NaN'
        try:
            lift_rope_babylift = soup.find(
                title="Rope tow/baby lift").find(class_="lift-amount").text
        except Exception:
            lift_rope_babylift = 'NaN'


# Creating dict for the resorts
        countries.append(b)
        resort_data = {
            'Region': c,
            'country': b,
            'resort_name': resort_name,
            'resort_link': resort_link,
            'altitude_max': altitude_max,
            'altitude_dif (minmax)': altitude_up,
            'blue_slopes': blue_slopes,
            'red_slopes': red_slopes,
            'black_slopes': black_slopes,
            'adult_skipass': adult_skipass,
            'young_skipass': young_skipass,
            'child_skipass': child_skipass,
            'lift_Tram_ropeway': lift_Tram_ropeway,
            'lift_gondola': lift_gondola,
            'lift_chair': lift_chair,
            'lift_Tbar': lift_Tbar,
            'lift_rope_babylift': lift_rope_babylift
        }
        resort_list.append(resort_data)
        print(counter)
        counter += 1
# Saving to JSON
with open('resorts_links.json', 'w') as json_file:
    json.dump(resort_list, json_file, indent=4)
