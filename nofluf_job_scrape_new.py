import pandas as pd
import requests
from bs4 import BeautifulSoup

from config import *

urls = pd.read_csv(f'data/{NAME}_nofluffjobs_urls.csv')
urls = [f'https://nofluffjobs.com{x}' for x in urls['urls']]

for u in [urls[6]]:
    print(u)

    response = requests.get(u)

    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    try:
        job_title = soup.find('h1', {'class': 'font-weight-bold bigger'}).text.strip()
    except AttributeError:
        job_title = soup.find('h1', {'class': 'font-weight-bold'}).text.strip()

    company_name = soup.find('a', {'id': 'postingCompanyUrl'}).text.strip()
    experience_low = soup.find('li', {'id': 'posting-seniority'}).text.strip()
    try:
        experience_low = experience_low.split(', ')[0]
        experience_high = experience_low.split(', ')[1]
    except IndexError:
        experience_high = experience_low

    salary = soup.find('common-posting-salaries-list')
    salary = salary.find_all('div', {'class': 'salary ng-star-inserted'})
    salary = [x.text.strip() for x in salary]

    try:
        is_remote = soup.find('li', {'class': 'remote ng-star-inserted'}).text.strip()
    except AttributeError:
        is_remote = 'No'

    try:
        location = soup.find('div', {'class': 'tw-flex tw-items-center cursor-pointer ng-star-inserted'}).text.strip()
    except AttributeError:
        location = 'No'

    when_published = soup.find('div', {'class': 'posting-time-row ng-star-inserted'}).text.strip()

    primary_skils = soup.find('section', {'branch': 'musts'}).find('ul')
    primary_skils = list(filter(None, [x.text.strip() for x in primary_skils]))

    try:
        secondary_skils = soup.find('section', {'id': 'posting-nice-to-have'}).find('ul')
        secondary_skils = list(filter(None, [x.text.strip() for x in secondary_skils]))
    except AttributeError:
        secondary_skils = 'No'

    requirements = soup.find('section', {'data-cy-section': 'JobOffer_Requirements'})
    primary_requirements = list(filter(None, requirements.find_all('ul')[0].text.strip().split("\n")))
    try:
        secondary_requirements = list(filter(None, requirements.find_all('ul')[1].text.strip().split("\n")))
    except IndexError:
        secondary_requirements = 'No'

    offer_description = soup.find('section', {'id': 'posting-description'}).find('div', {'class': 'tw-overflow-hidden ng-star-inserted'}).text.strip()

    try:
        tasks_list = soup.find('section', {'id': 'posting-tasks'})
        tasks_list = [x.text.strip() for x in tasks_list.find('ol').find_all('li')]
    except AttributeError:
        tasks_list = 'No'

    offer_details = soup.find('section', {'class': 'd-block p-20 border-top'}).find('ul')
    offer_details = [x.text.strip() for x in offer_details.find_all('li')]

    equipment = soup.find('section', {'id': 'posting-equipment'}).find('ul')
    equipment = [x.text.strip() for x in equipment.find_all('li')]

    try:
        metodology = soup.find('section', {'id': 'posting-environment'}).find('ul')
        metodology = [x.text.strip() for x in metodology.find_all('li')]
    except AttributeError:
        metodology = 'No'

    try:
        benefits = soup.find('div', {'id': 'posting-benefits'}).find_all('section')
        office_benefits = [x.text.strip() for x in benefits[0].find_all('li')]
        additional_benefits = [x.text.strip() for x in benefits[1].find_all('li')]
    except IndexError:
        office_benefits = 'No'
        additional_benefits = 'No'
