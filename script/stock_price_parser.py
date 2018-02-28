'''
Skripta sa stranica zse.hr dohvaća podatke o trgovanju dionicama na dan (ili live podatke)
Adrese za dohvat podataka:
    1. http://zse.hr/default.aspx?id=17991 - LIVE trgovanje (odmak od min. 15 minuta)
    2. http://zse.hr/default.aspx?id=26521 - podaci iz arhive. Može se pozvati na dva načina:
        a) GET metodom - dohvaća podatke za prethodni (završeni) dan
        b) POST metodom - ukoliko su parametri ispravni, dohvaća podatke za neki prethodni datum. U suprotnom radi isto što i GET metoda
'''
import os
import sys
from bs4 import BeautifulSoup
import urllib.request
from urllib.request import urlopen
from django.core.wsgi import get_wsgi_application
import logging
import datetime
from decimal import Decimal
from finrep_utils import text_to_number, is_number, return_num_if_text_present


# dry_run - Set this parameter to False to actually enter data to DB
dry_run = False
django_project_path = '..\\web'

GET_LIVE_DATA = True
GET_YESTERDAY_DATA = True

today = datetime.datetime.now()
offset = -12
GET_DATE = (today + datetime.timedelta(days=offset)).strftime('%d.%m.%Y')
# GET_DATE = '19.2.2018'  # expected format for GET_DATE
values = {
    'selDatum': GET_DATE,
    'btnSave': 'Prikaži',
    'IsItPregledPovijest': 'yes',
    'rbScope': 'svi'
}


def get_security_value_on_date(security, current_date):
    sec_val_list = SecurityPrices.objects.filter(security=security, date=current_date)
    no_items = len(sec_val_list)
    if no_items >= 1:
        sec_val = sec_val_list[0]
    else:
        sec_val = None

    return sec_val


def update_stock_price(sec_val, current_date):
    logging.info("Updating stock price: {0} ({1})".format(sec_val[0], current_date))
    securities_list = Securities.objects.filter(mark=sec_val[0])
    if len(securities_list) != 1:
        logging.error("\tError while fetching security {0} ({1} records found)".format(sec_val[0], len(security)))
    else:
        security = securities_list[0]
        record = get_security_value_on_date(security, current_date)
        if record:
            logging.error("\tStock price for {0} on {1} already entered: ".format(security, current_date))
        else:
            record = SecurityPrices(
                date=current_date,
                security=security,
                last_price=return_num_if_text_present(sec_val[3]),
                change_pct=sec_val[4],
                open_price=return_num_if_text_present(sec_val[5]),
                high_price=return_num_if_text_present(sec_val[6]),
                low_price=return_num_if_text_present(sec_val[7]),
                average_price=return_num_if_text_present(sec_val[8]),
                volume=return_num_if_text_present(sec_val[9]),
                turnover=return_num_if_text_present(sec_val[10]),
            )
            print(record)
            # record.save()
            logging.info("\tUpdate finished for {0} on {1}: ".format(security, current_date))


if GET_LIVE_DATA:
    req = urllib.request.Request('http://zse.hr/default.aspx?id=17991')
    fetch_date = datetime.date.today()
elif GET_YESTERDAY_DATA:
    req = urllib.request.Request('http://zse.hr/default.aspx?id=26521')
    fetch_date = datetime.date.today() + datetime.timedelta(days=-1)
else:
    data = urllib.parse.urlencode(values).encode('utf-8')
    req = urllib.request.Request('http://zse.hr/default.aspx?id=26521', data)
    fetch_date = GET_DATE


soup = BeautifulSoup(urlopen(req), 'html.parser')

page_title = soup.find('td', class_='pageTitle').text.strip()
expected_title = "Pregled trgovine na Uređenom tržištu za {0}".format(GET_DATE)

if (not GET_LIVE_DATA) and (not GET_YESTERDAY_DATA) and (expected_title != page_title):
    print("ERROR while fetching data.\n\tExpected page title: {0}\n\tActual page tite: {1}".format(expected_title, page_title))

table = soup.find('table', id='dnevna_trgovanja')
rows = table.find_all('tr')
security_values_list = []
for row in rows[1:]:
    cols = row.find_all('td')
    cols = [ele.text.strip() for ele in cols]
    security_values_list.append(cols)
    # U slučaju da dohvaćamo "live data", u gridu nedostaje kolona "Zaključna"
    # pa ju ubacujemo kako bi podaci bili u identičnom formatu za ostatak skripte
    # if GET_LIVE_DATA:
    #     cols.insert(2, None)  # izleda da ne treba, sustav sam ubacuje opraznu vrijednost na poziciju 1 ??
    # print("{0} - {1} ({2})".format(cols[0], cols[3], cols[4]))


if dry_run:
    for idx, st_val in enumerate(security_values_list):
        print("{: >3}. {}".format(idx + 1, st_val))
else:
    # logging configuration
    logging.basicConfig(filename='stock_prices.log', level=logging.DEBUG)

    # This is so Django knows where to find stuff.
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "finrep.settings")
    sys.path.append(django_project_path)

    # This is so my local_settings.py gets loaded.
    os.chdir(django_project_path)

    # This is so models get loaded.
    application = get_wsgi_application()

    # import models
    from gfi.models import *

    for sec_val in security_values_list:
        update_stock_price(sec_val, fetch_date)
