
import re

import requests
from bs4 import BeautifulSoup


def find_req(req):
    req_list = []
    for k, v in find_dict.items():
        rows = req.find_all(k, {'class': v})
        req_list.extend(r.get_text().strip() for r in rows)
    return req_list


URL = 'https://nofluffjobs.com/pl/job/data-engineer-avanade-poland-remote-1kev44ih'

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36", "Accept-Encoding": "gzip, deflate",
           "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT": "1", "Connection": "close", "Upgrade-Insecure-Requests": "1"}
page = requests.get(URL, headers=headers)
soup = BeautifulSoup(page.content, "html.parser")
soup = BeautifulSoup(soup.prettify(), "html.parser")

title = soup.find(
    'h1', {'class': 'font-weight-bold bigger'}).get_text().strip()
company = soup.find(id='postingCompanyUrl').get_text().strip()
level = soup.find(
    'span', {'class': 'mr-10 font-weight-medium'}).get_text().strip()

req = soup.find_all('h3', {'class': 'mb-0'})
primary_req = req[0]
secondary_req = req[1]

find_dict = {'object': 'btn btn-outline-success btn-sm text-truncate',
             'button': 'btn btn-outline-success btn-sm no-cursor text-truncate'}

primary_req_list = find_req(primary_req)
secondary_req_list = find_req(secondary_req)

cash_values = []
cash_list = soup.find_all('div', {'class': 'salary'})
for cash in cash_list:
    value = cash.find('h4', {'class': 'mb-0'}).get_text()
    value = re.sub(r'\s(?=\s)', '', re.sub(r'\s', ' ', value))
    contract = cash.find('div', {
                         'class': 'paragraph font-size-14 d-flex align-items-center flex-wrap type position-relative'}).get_text()
    contract = re.sub(r'\s(?=\s)', '', re.sub(r'\s', ' ', contract))
    cash_values.append([value, contract])

locations = soup.find('ul', {'class': 'list-unstyled m-0'}).get_text()
locations = re.sub(r'\s(?=\s)', '', re.sub(r'\s', ' ', locations))

posting_time = soup.find('div', {'class': 'posting-time-row'}).get_text()
posting_time = re.sub(r'\s(?=\s)', '', re.sub(r'\s', ' ', posting_time))

tasks = soup.find(id='posting-tasks').get_text().split('\n')
tasks = [task.strip() for task in tasks if task.strip() != '']
tasks = [task for task in tasks if not task.isdigit()]

specs = soup.find(id='posting-specs').get_text().split('\n')
specs = [spec.strip() for spec in specs if spec.strip() != '']
specs = [spec for spec in specs if spec != '•'][1:]

gears = soup.find(
    'section', {'class': 'd-flex align-items-start'}).get_text().split('\n')
gears = [gear.strip() for gear in gears if gear.strip() != '']

envs = soup.find(id='posting-environment').get_text().split('\n')
envs = [env.strip() for env in envs if env.strip() != ''][1:]
envs = [env.replace('\xa0', ' ') for env in envs]

benfs = soup.find(id='posting-benefits').get_text().split('\n')
benfs = [benf.strip() for benf in benfs if benf.strip() != ''][1:]
