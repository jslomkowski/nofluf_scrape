import contextlib
import csv
import datetime
import re

import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup

from config import *

urls = pd.read_csv(f'data/{NAME}_nofluffjobs_urls.csv')
urls = [f'https://nofluffjobs.com{x}' for x in urls['urls']]

for u in [urls[0]]:
    print(u)

    response = requests.get(u)

    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    job_title = soup.find('h1', {'class': 'font-weight-bold bigger'}).text.strip()
    company_name = soup.find('a', {'id': 'postingCompanyUrl'}).text.strip()
    experience = soup.find('span', {'class': 'mr-10 font-weight-medium'}).text.strip()
    salary = soup.find('h4', {'class': 'tw-mb-0'}).text.strip()
    contract_type = soup.find('div', {'class': 'paragraph tw-text-sm tw-flex tw-items-center tw-flex-wrap type tw-relative'}).text.strip()
    is_remote = soup.find('li', {'class': 'remote ng-star-inserted'}).text.strip()
    location = soup.find('span', {'class': 'tw-overflow-hidden tw-overflow-ellipsis tw-whitespace-nowrap'}).text.strip()
    when_published = soup.find('div', {'class': 'posting-time-row ng-star-inserted'}).text.strip()

    primary_skils = soup.find('section', {'branch': 'musts'}).find('ul')
    primary_skils = [x.text.strip() for x in primary_skils]

    secondary_skils = soup.find('section', {'id': 'posting-nice-to-have'}).find('ul')
    secondary_skils = [x.text.strip() for x in secondary_skils]

    requirements = soup.find('section', {'data-cy-section': 'JobOffer_Requirements'})
    primary_requirements = requirements.find_all('ul')[0].text.strip().split("\n")
    secondary_requirements = requirements.find_all('ul')[1].text.strip().split("\n")

    offer_description = soup.find('section', {'id': 'posting-description'}).find('div', {'class': 'tw-overflow-hidden ng-star-inserted'}).text.strip()

    tasks_list = soup.find('section', {'id': 'posting-tasks'})
    tasks_list = [x.text.strip() for x in tasks_list.find('ol').find_all('li')]

    offer_details = soup.find('section', {'class': 'd-block p-20 border-top'}).find('ul')
    offer_details = [x.text.strip() for x in offer_details.find_all('li')]

    equipment = soup.find('section', {'id': 'posting-equipment'}).find('ul')
    equipment = [x.text.strip() for x in equipment.find_all('li')]

    metodology = soup.find('section', {'id': 'posting-environment'}).find('ul')
    metodology = [x.text.strip() for x in metodology.find_all('li')]

    benefits = soup.find('div', {'id': 'posting-benefits'}).find_all('section')
    office_benefits = [x.text.strip() for x in benefits[0].find_all('li')]
    additional_benefits = [x.text.strip() for x in benefits[1].find_all('li')]
