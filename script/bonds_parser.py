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


def get_bond_by_abbreviation(abbrev):
    bond_list = Securities.objects.filter(mark=abbrev)
    no_items = len(bond_list)
    if no_items >= 1:
        bond = bond_list[0]
    else:
        bond = None

    return bond


def split_number_and_currency(input):
    arr = input.split(" ")
    return (Decimal(arr[0].replace('.', '').replace(',', '.')), arr[1])


def update_bond(bond_arr):
    logging.info("Updating bond: {0}".format(bond_arr))
    bond = get_bond_by_abbreviation(bond_arr[0])
    if bond:
        bond.isin = bond_arr[2]
        bond.issued_number = bond_arr[3].replace('.', '')
        (num, curr) = split_number_and_currency(bond_arr[4])
        bond.nominal_value = num
        bond.currency = curr
        bond.enlistment_date = datetime.datetime.strptime(bond_arr[5], '%d.%m.%Y')
        bond.security_type = 'O'
        bond.save()
        logging.info("Update finished: {0}".format(bond_arr[0]))
    else:
        logging.error("\tCannot find bond: {0}".format(bond_arr[0]))


soup = BeautifulSoup(urlopen('http://zse.hr/default.aspx?id=26476'), 'html.parser')
table = soup.find('table', id='dnevna_trgovanja')
rows = table.find_all('tr')
bonds_list = []
for row in rows:
    cols = row.find_all('td')
    cols_stripped = [ele.text.strip() for ele in cols]
    bonds_list.append(cols_stripped)


if dry_run:
    for idx, bond in enumerate(bonds_list[1:]):
        print("{: >3}. {}".format(idx + 1, bond))
else:
    # logging configuration
    logging.basicConfig(filename='bonds.log', level=logging.DEBUG)

    # This is so Django knows where to find stuff.
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "finrep.settings")
    sys.path.append(django_project_path)

    # This is so my local_settings.py gets loaded.
    os.chdir(django_project_path)

    # This is so models get loaded.
    application = get_wsgi_application()

    # import models
    from gfi.models import *

    for bond in bonds_list[1:]:
        update_bond(bond)
