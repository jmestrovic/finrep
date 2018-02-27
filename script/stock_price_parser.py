from bs4 import BeautifulSoup
from urllib.request import urlopen
import urllib.request

'''
Skripta sa stranica zse.hr dohvaća podatke o trgovanju dionicama na dan (ili live podatke)
Adrese za dohvat podataka:
    1. http://zse.hr/default.aspx?id=17991 - LIVE trgovanje (odmak od min. 15 minuta)
    2. http://zse.hr/default.aspx?id=26521 - podaci iz arhive. Može se pozvati na dva načina:
        a) GET metodom - dohvaća podatke za prethodni (završeni) dan
        b) POST metodom - ukoliko su parametri ispravni, dohvaća podatke za neki prethodni datum. U suprotnom radi isto što i GET metoda
'''

GET_LIVE_DATA = True
GET_DATE = '19.2.2018'
values = {
    'selDatum': GET_DATE,
    'btnSave': 'Prikaži',
    'IsItPregledPovijest': 'yes',
    'rbScope': 'svi'
}


if GET_LIVE_DATA:
    req = urllib.request.Request('http://zse.hr/default.aspx?id=17991')
else:
    data = urllib.parse.urlencode(values).encode('utf-8')
    req = urllib.request.Request('http://zse.hr/default.aspx?id=26521', data)


soup = BeautifulSoup(urlopen(req), 'html.parser')

title = soup.find('td', class_='pageTitle').text.strip()
print(title)

table = soup.find('table', id='dnevna_trgovanja')
rows = table.find_all('tr')
for row in rows:
    cols = row.find_all('td')
    cols = [ele.text.strip() for ele in cols]
    print("{0} - {1} ({2})".format(cols[0], cols[3], cols[4]))
