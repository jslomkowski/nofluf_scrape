import pandas as pd
import requests
from bs4 import BeautifulSoup

from config import *

NAME = "ai_2022-12-26"
urls = pd.read_csv(f'data/{NAME}_nofluffjobs_urls.csv')
urls = [f'https://nofluffjobs.com{x}' for x in urls['urls']]

df = pd.DataFrame()

for u in urls[:3]:
    print(u)

    response = requests.get(u)

    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    try:
        job_title = soup.find(
            'h1', {'class': 'font-weight-bold bigger'}).text.strip()
    except AttributeError:
        job_title = soup.find('h1', {'class': 'font-weight-bold'}).text.strip()

    company_name = soup.find('a', {'id': 'postingCompanyUrl'}).text.strip()
    experience_low = soup.find('li', {'id': 'posting-seniority'}).text.strip()
    try:
        experience_low = experience_low.split(', ')[0]
        experience_high = experience_low.split(', ')[1]
    except IndexError:
        experience_high = experience_low

    salaries = soup.find('common-posting-salaries-list')
    salaries = salaries.find_all('div', {'class': 'salary ng-star-inserted'})
    salaries = [x.text.strip().replace("\xa0", "") for x in salaries]
    for salary in salaries:
        if 'UoP' in salary:
            if "–" in salary:
                value_high = salary.split()[2]
            value_low = salary.split()[0]
            if "PLN" in salary:
            # ! todo continue
            currency = salary.split()[1]
            contract = 'UoP'


    try:
        is_remote = soup.find(
            'li', {'class': 'remote ng-star-inserted'}).text.strip()
    except AttributeError:
        is_remote = 'No'

    try:
        location = soup.find('div', {
                             'class': 'tw-flex tw-items-center cursor-pointer ng-star-inserted'}).text.strip()
    except AttributeError:
        location = 'No'

    when_published = soup.find(
        'div', {'class': 'posting-time-row ng-star-inserted'}).text.strip()

    primary_skils = soup.find('section', {'branch': 'musts'}).find('ul')
    primary_skils = list(filter(None, [x.text.strip() for x in primary_skils]))

    try:
        secondary_skils = soup.find(
            'section', {'id': 'posting-nice-to-have'}).find('ul')
        secondary_skils = list(
            filter(None, [x.text.strip() for x in secondary_skils]))
    except AttributeError:
        secondary_skils = 'No'

    requirements = soup.find(
        'section', {'data-cy-section': 'JobOffer_Requirements'})
    primary_requirements = list(
        filter(None, requirements.find_all('ul')[0].text.strip().split("\n")))
    try:
        secondary_requirements = list(
            filter(None, requirements.find_all('ul')[1].text.strip().split("\n")))
    except IndexError:
        secondary_requirements = 'No'

    offer_description = soup.find('section', {'id': 'posting-description'}).find(
        'div', {'class': 'tw-overflow-hidden ng-star-inserted'}).text.strip()

    try:
        tasks_list = soup.find('section', {'id': 'posting-tasks'})
        tasks_list = [x.text.strip()
                      for x in tasks_list.find('ol').find_all('li')]
    except AttributeError:
        tasks_list = 'No'

    offer_details = soup.find(
        'section', {'class': 'd-block p-20 border-top'}).find('ul')
    offer_details = [x.text.strip() for x in offer_details.find_all('li')]

    equipment = soup.find('section', {'id': 'posting-equipment'}).find('ul')
    equipment = [x.text.strip() for x in equipment.find_all('li')]

    try:
        metodology = soup.find(
            'section', {'id': 'posting-environment'}).find('ul')
        metodology = [x.text.strip() for x in metodology.find_all('li')]
    except AttributeError:
        metodology = 'No'

    try:
        benefits = soup.find(
            'div', {'id': 'posting-benefits'}).find_all('section')
        office_benefits = [x.text.strip() for x in benefits[0].find_all('li')]
        additional_benefits = [x.text.strip()
                               for x in benefits[1].find_all('li')]
    except IndexError:
        office_benefits = 'No'
        additional_benefits = 'No'

lst = {
    "job_title": job_title,
    "company_name": company_name,
    "experience_low": experience_low,
    "experience_high": experience_high,
    "salary": salary,
    "is_remote": is_remote,
    "location": location,
    "when_published": when_published,
    "primary_skils": primary_skils,
    "secondary_skils": secondary_skils,
    "primary_requirements": primary_requirements,
    "secondary_requirements": secondary_requirements,
    "offer_description": offer_description,
    "tasks_list": tasks_list,
    "offer_details": offer_details,
    "equipment": equipment,
    "metodology": metodology,
    "office_benefits": office_benefits,
    "additional_benefits": additional_benefits,
}

for k, v in lst.items():
    if isinstance(v, list):
        print(k, len(v))

    df_combine = pd.DataFrame({
        'job_title': job_title,
        'company_name': company_name,
        'experience_low': experience_low,
        'experience_high': experience_high,
        'salary': salary,
        'is_remote': is_remote,
        'location': location,
        'when_published': when_published,
        'primary_skils': primary_skils,
        'secondary_skils': secondary_skils,
        'primary_requirements': primary_requirements,
        'secondary_requirements': secondary_requirements,
        'offer_description': offer_description,
        'tasks_list': tasks_list,
        'offer_details': offer_details,
        'equipment': equipment,
        'metodology': metodology,
        'office_benefits': office_benefits,
        'additional_benefits': additional_benefits
    })

    df = df.append(df_combine)
