from bs4 import BeautifulSoup
from urllib.request import urlopen

soup = BeautifulSoup(urlopen('http://zse.hr/default.aspx?id=26521'), 'html.parser')
table = soup.find('table', id='dnevna_trgovanja')
rows = table.find_all('tr')
for row in rows:
    print(row)
    cols = row.find_all('td')
    cols = [ele.text.strip() for ele in cols]
    print("{0} - {1} ({2})".format(cols[0], cols[3], cols[4]))
