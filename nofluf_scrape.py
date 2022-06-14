
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

locations = soup.find('div', {'class': 'additional-info-row'}).get_text()
location.get_text()
