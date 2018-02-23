from bs4 import BeautifulSoup
from urllib.request import urlopen

soup = BeautifulSoup(urlopen('http://zse.hr/default.aspx?id=26476'), 'html.parser')
table = soup.find('table', id='dnevna_trgovanja')
rows = table.find_all('tr')
bonds_list = []
for row in rows:
    cols = row.find_all('td')
    cols_stripped = [ele.text.strip() for ele in cols]
    bonds_list.append(cols_stripped)

i = 0
for issuer in bonds_list:
    i += 1
    print(i, ". ", issuer)
