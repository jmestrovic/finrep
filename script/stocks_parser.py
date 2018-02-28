import os
import sys
from bs4 import BeautifulSoup
from urllib.request import urlopen
from django.core.wsgi import get_wsgi_application
import logging
import datetime
from decimal import Decimal

# dry_run - Set this parameter to False to actually enter data to DB
dry_run = True
django_project_path = '..\\web'


def get_stock_by_abbreviation(abbrev):
    stock_list = Securities.objects.filter(mark=abbrev)
    no_items = len(stock_list)
    if no_items >= 1:
        stock = stock_list[0]
    else:
        stock = None

    return stock


def split_number_and_currency(input):
    arr = input.split(" ")
    if len(arr) == 2:
        return (Decimal(arr[0].replace('.', '').replace(',', '.')), arr[1])
    else:
        return(0, '')


def update_stock(stock_arr):
    logging.info("Updating stock: {0}".format(stock_arr))
    stock = get_stock_by_abbreviation(stock_arr[0])
    if stock:
        stock.isin = stock_arr[2]
        stock.issued_number = stock_arr[3].replace('.', '')
        (num, curr) = split_number_and_currency(stock_arr[4])
        stock.nominal_value = num
        stock.currency = curr
        stock.enlistment_date = datetime.datetime.strptime(stock_arr[5], '%d.%m.%Y')
        stock.security_type = 'D'
        stock.save()
        logging.info("Update finished: {0}".format(stock_arr[0]))
    else:
        logging.error("\tCannot find stock: {0}".format(stock_arr[0]))


soup = BeautifulSoup(urlopen('http://zse.hr/default.aspx?id=26474'), 'html.parser')
table = soup.find('table', id='dnevna_trgovanja')
rows = table.find_all('tr')
stocks_list = []
for row in rows:
    cols = row.find_all('td')
    cols_stripped = [ele.text.strip() for ele in cols]
    stocks_list.append(cols_stripped)


if dry_run:
    for idx, stock in enumerate(stocks_list[1:]):
        print("{: >3}. {}".format(idx + 1, stock))
else:
    # logging configuration
    logging.basicConfig(filename='stocks.log', level=logging.DEBUG)

    # This is so Django knows where to find stuff.
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "finrep.settings")
    sys.path.append(django_project_path)

    # This is so my local_settings.py gets loaded.
    os.chdir(django_project_path)

    # This is so models get loaded.
    application = get_wsgi_application()

    # import models
    from gfi.models import *

    for stock in stocks_list[1:]:
        update_stock(stock)
