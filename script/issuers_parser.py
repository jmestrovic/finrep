import os
import sys
from bs4 import BeautifulSoup
from urllib.request import urlopen
from django.core.wsgi import get_wsgi_application
import logging
from datetime import datetime
from urllib.parse import urlparse, parse_qs


# dry_run - Set this parameter to False to actually enter data to DB
dry_run = True
django_project_path = '..\\web'



def get_company_id(abbrev):
    company = Companies.objects.filter(abbreviation=abbrev)
    no_items = len(company)
    if no_items >= 1:
        id = company[0].id
    else:
        id = -1

    return id


def get_abbrev_from_papers(papers_list):
    return(list(papers_list.keys())[0])[:4]


def create_papers_for_company(company, company_papers_dict):
    for paper, zse_mark in company_papers_dict.items():
        security = Securities(company=company, mark=paper, zse_mark=zse_mark, nominal_value=0)
        security.save()


def insert_or_update_company(issuer):
    logging.info("Adding {0}".format(issuer))
    comp_name = issuer[0]
    comp_papers = issuer[1]
    comp_city = issuer[2]
    comp_short_name = issuer[3]
    comp_papers_dict = issuer[4]
    comp_abbrev = get_abbrev_from_papers(comp_papers_dict)

    comp = Companies(name=comp_name, short_name=comp_short_name, abbreviation=comp_abbrev, city=comp_city, securities_list=comp_papers)
    comp.save()
    create_papers_for_company(comp, comp_papers_dict)

    # id = get_company_id(abbrev)
    # if id == -1:
    #     logging.info("Abbreviation {0} do not exist. Inserting {0} - {1} - {2}".format(abbrev, name, city))
    #     short_name = name[:50]
    #     comp = Companies(name=name, short_name=short_name, abbreviation=abbrev, city=city)
    #     comp.save()
    #     id = comp.id
    # else:
    #     logging.info("Abbreviation {0} exists".format(abbrev))
    #     comp = Companies.objects.filter(id=id).first()
    #     if (comp.abbreviation != abbrev) or (comp.name != name) or (comp.city != city):
    #         logging.info("\tUpdating {0} -> {3}, {1} -> {4}, {2} -> {5}".format(comp.abbreviation, comp.name, comp.city, abbrev, name, city))
    #         comp.abbreviation = abbrev
    #         comp.name = name
    #         comp.city = city
    #         comp.save()
    #     else:
    #         logging.info("\tMatching records. No need to update.")
    # return id


soup = BeautifulSoup(urlopen('http://zse.hr/default.aspx?id=36769'), 'html.parser')
table = soup.find('table', id='dnevna_trgovanja')
rows = table.find_all('tr')
issuers_list = []
for row in rows[1:]:
    cols = row.find_all('td')
    cols_stripped = [ele.text.strip() for ele in cols]

    # get short name
    short_name = cols[0].find('b').text
    cols_stripped.append(short_name)

    # create dictionary of all stocks/bonds with ZSE cipher
    links = cols[1].find_all('a', href=True)
    links_dict = {}
    for link_full in links:
        link_name = link_full.contents[0]
        link = link_full['href']
        parser_url = urlparse(link)
        url_params = parse_qs(parser_url.query)
        link_cipher = url_params['dionica'][0]
        links_dict[link_name] = link_cipher
    cols_stripped.append(links_dict)

    issuers_list.append(cols_stripped)


if dry_run:
    for idx, issuer in enumerate(issuers_list[1:]):
        print("{: >3}. {}".format(idx+1, issuer))
else:
    # logging configuration
    logging.basicConfig(filename='issuers.log', level=logging.DEBUG)

    # This is so Django knows where to find stuff.
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "finrep.settings")
    sys.path.append(django_project_path)

    # This is so my local_settings.py gets loaded.
    os.chdir(django_project_path)

    # This is so models get loaded.
    application = get_wsgi_application()

    # import models
    from gfi.models import *

    for issuer in issuers_list[1:]:
        insert_or_update_company(issuer)