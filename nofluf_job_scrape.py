
import datetime
import re

import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup


def find_req(req):
    req_list = []
    for k, v in find_dict.items():
        rows = req.find_all(k, {'class': v})
        req_list.extend(r.get_text().strip() for r in rows)
    return req_list


now = datetime.datetime.now()
now = now.strftime("%Y-%m-%d %H:%M:%S")

find_dict = {'object': 'btn btn-outline-success btn-sm text-truncate',
             'button': 'btn btn-outline-success btn-sm no-cursor text-truncate'}

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36", "Accept-Encoding": "gzip, deflate",
           "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT": "1", "Connection": "close", "Upgrade-Insecure-Requests": "1"}

urls = pd.read_csv('nofluffjobs_urls.csv')
urls = [f'https://nofluffjobs.com{x}' for x in urls['urls']]
urls = urls[10:15]

data = []
for u in urls:
    print(u)
    page = requests.get(u, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")
    soup = BeautifulSoup(soup.prettify(), "html.parser")

    try:
        title = soup.find(
            'h1', {'class': 'font-weight-bold bigger'}).get_text().strip()
    except AttributeError:
        title = soup.find(
            'h1', {'class': 'font-weight-bold'}).get_text().strip()

    company = soup.find(id='postingCompanyUrl').get_text().strip()

    level = soup.find(
        'span', {'class': 'mr-10 font-weight-medium'}).get_text().strip()

    req = soup.find_all('h3', {'class': 'mb-0'})
    primary_req_list = find_req(req[0])
    secondary_req_list = find_req(req[1]) if len(req) > 1 else []

    cash_values = []
    cash_list = soup.find_all('div', {'class': 'salary'})
    for cash in cash_list:
        value = cash.find('h4', {'class': 'mb-0'}).get_text()
        value = re.sub(r'\s(?=\s)', '', re.sub(r'\s', ' ', value))
        contract = cash.find('div', {
            'class': 'paragraph font-size-14 d-flex align-items-center flex-wrap type position-relative'}).get_text()
        contract = re.sub(r'\s(?=\s)', '', re.sub(r'\s', ' ', contract))
        cash_values.append([value, contract])

    try:
        locations = soup.find('ul', {'class': 'list-unstyled m-0'}).get_text()
        locations = re.sub(r'\s(?=\s)', '', re.sub(r'\s', ' ', locations))
        locations = re.sub(r'Zdalnie • ', '', locations)
        locations = re.findall(r'•(.*?),', locations)
        locations = [x.strip() for x in locations]
    except AttributeError:
        locations = np.nan
    try:
        remote = soup.find('li', {'class': 'remote'}).get_text()
        remote = re.sub(r'\s(?=\s)', '', re.sub(r'\s', ' ', remote))
        if remote == ' Zdalnie ':
            remote = True
    except AttributeError:
        remote = np.nan

    posting_time = soup.find('div', {'class': 'posting-time-row'}).get_text()
    posting_time = re.sub(r'\s(?=\s)', '', re.sub(r'\s', ' ', posting_time))

    tasks = soup.find(id='posting-tasks').get_text().split('\n')
    tasks = [task.strip() for task in tasks if task.strip() != '']
    tasks = [task for task in tasks if not task.isdigit()]

    specs = soup.find(id='posting-specs').get_text().split('\n')
    specs = [spec.strip() for spec in specs if spec.strip() != '']
    specs = [spec for spec in specs if spec != '•']

    gears = soup.find(
        'section', {'class': 'd-flex align-items-start'}).get_text().split('\n')
    gears = [gear.strip() for gear in gears if gear.strip() != '']

    try:
        envs = soup.find(id='posting-environment').get_text().split('\n')
        envs = [env.strip() for env in envs if env.strip() != '']
        envs = [env.replace('\xa0', ' ') for env in envs]
    except AttributeError:
        envs = np.nan

    benfs = soup.find(id='posting-benefits').get_text().split('\n')
    benfs = [benf.strip() for benf in benfs if benf.strip() != '']

    scrape_dict = {'key': u.split('-')[-1]}
    scrape_dict['timestamp'] = now
    scrape_dict['link'] = u
    scrape_dict['title'] = title
    scrape_dict['company'] = company
    scrape_dict['level'] = level
    scrape_dict['primary_req_list'] = primary_req_list
    scrape_dict['secondary_req_list'] = secondary_req_list
    scrape_dict['cash_values'] = cash_values
    scrape_dict['locations'] = locations
    scrape_dict['remote'] = remote
    scrape_dict['posting_time'] = posting_time
    scrape_dict['tasks'] = tasks
    scrape_dict['specs'] = specs
    scrape_dict['gears'] = gears
    scrape_dict['envs'] = envs
    scrape_dict['benfs'] = benfs
    data.append(scrape_dict)

df_data = pd.DataFrame(data)

final_list = []
for i in range(len(df_data)):
    final_list = final_list + df_data['primary_req_list'][i]
final_list = [x.lower() for x in final_list]

final_list = pd.Series(final_list)
final_list.value_counts().sort_index()
