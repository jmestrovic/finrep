from bs4 import BeautifulSoup
from urllib.request import urlopen

soup = BeautifulSoup(urlopen('http://zse.hr/default.aspx?id=26474'), 'html.parser')
table = soup.find('table', id='dnevna_trgovanja')
rows = table.find_all('tr')
stocks_list = []
for row in rows:
    cols = row.find_all('td')
    cols_stripped = [ele.text.strip() for ele in cols]
    # print("{0} - {1} - {2}".format(cols[0], cols[1], cols[2]))
    # print(cols)
    stocks_list.append(cols_stripped)

i = 0
for issuer in stocks_list:
    i += 1
    print(i, ". ", issuer)