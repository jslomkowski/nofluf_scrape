
import contextlib
import datetime
import re

import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup

from config import headers


def get_title(soup):
    try:
        title = soup.find(
            'h1', {'class': 'font-weight-bold bigger'}).get_text().strip()
    except AttributeError:
        title = soup.find(
            'h1', {'class': 'font-weight-bold'}).get_text().strip()
    return title


def get_company(soup):
    return soup.find(id='postingCompanyUrl').get_text().strip()


def get_level_low(soup):
    level = soup.find(
        'span', {'class': 'mr-10 font-weight-medium'}).get_text().strip()
    return [str(s).strip() for s in level.split(',')][0]


def get_level_high(soup):
    try:
        level = soup.find(
            'span', {'class': 'mr-10 font-weight-medium'}).get_text().strip()
        level = [str(s).strip() for s in level.split(',')][1]
    except IndexError:
        level = []
    return level


def get_pri_req(soup):
    def find_req(req):
        req_list = []
        for k, v in find_dict.items():
            rows = req.find_all(k, {'class': v})
            req_list.extend(r.get_text().strip() for r in rows)
        return req_list
    find_dict = {'object': 'btn btn-outline-success btn-sm text-truncate',
                 'button': 'btn btn-outline-success btn-sm no-cursor text-truncate'}
    req = soup.find_all('h3', {'class': 'mb-0'})
    primary_req_list = find_req(req[0])
    return primary_req_list


def get_sec_req(soup):
    def find_req(req):
        req_list = []
        for k, v in find_dict.items():
            rows = req.find_all(k, {'class': v})
            req_list.extend(r.get_text().strip() for r in rows)
        return req_list
    find_dict = {'object': 'btn btn-outline-success btn-sm text-truncate',
                 'button': 'btn btn-outline-success btn-sm no-cursor text-truncate'}
    req = soup.find_all('h3', {'class': 'mb-0'})
    secondary_req_list = find_req(req[1]) if len(req) > 1 else []
    return secondary_req_list


def get_money(soup):
    value_currency_contract = []
    cash_list_class = soup.find_all('div', {'class': "salary"})
    for cash_class in cash_list_class:
        if """class="salary">""" in str(cash_class):
            cash = cash_class.find('h4', {'class': 'mb-0'}).get_text()
            cash = re.sub(r'\s(?=\s)', '', re.sub(r'\s', ' ', cash)).strip()
            cash = re.sub(r'(\d)\s+(\d)', r'\1\2', cash)
            value = [int(s) for s in cash.split() if s.isdigit()]
            currency = [str(s) for s in cash.split() if not s.isdigit()]
            if '-' in currency:
                currency.remove('-')
            currency = ', '.join(str(e) for e in currency)
            contract = cash_class.find('div', {
                'class': 'paragraph font-size-14 d-flex align-items-center flex-wrap type position-relative'}).get_text()
            contract = re.sub(r'\s(?=\s)', '', re.sub(
                r'\s', ' ', contract)).strip()
            value = value + [currency] + [contract]
            value_currency_contract.append(value)
    return value_currency_contract


def get_locations(soup):
    try:
        locations = soup.find('ul', {'class': 'list-unstyled m-0'}).get_text()
        locations = re.sub(r'\s(?=\s)', '', re.sub(r'\s', ' ', locations))
        locations = re.sub(r'Zdalnie •', '', locations)
        locations = re.findall(r'•(.*?),', locations)
        locations = [x.strip() for x in locations]
    except AttributeError:
        locations = np.nan
    return locations


def get_remote(soup):
    try:
        remote = soup.find('li', {'class': 'remote'}).get_text()
        remote = re.sub(r'\s(?=\s)', '', re.sub(r'\s', ' ', remote))
        if remote == ' Zdalnie ':
            remote = True
    except AttributeError:
        remote = np.nan
    return remote


def get_posting_time(soup):
    posting_time = soup.find('div', {'class': 'posting-time-row'}).get_text()
    return re.sub(r'\s(?=\s)', '', re.sub(r'\s', ' ', posting_time)).strip()


def get_tasks(soup):
    try:
        tasks = soup.find(id='posting-tasks').get_text().split('\n')
        tasks = [task.strip() for task in tasks if task.strip() != '']
        tasks = [task for task in tasks if not task.isdigit()]
    except AttributeError:
        tasks = np.nan


def get_specs(soup):
    specs = soup.find(id='posting-specs').get_text()
    specs = specs.split('•')
    return [spec.strip() for spec in specs]


def get_gear(soup):
    gear = soup.find(
        'section', {'class': 'd-flex align-items-start'}).get_text()
    gear = gear.split('  ')
    return [g.strip() for g in gear]


def get_envs(soup):
    try:
        envs_raw = soup.find(id='posting-environment')
        envs_raw = envs_raw.find_all('div', {'class': 'px-0'})
        envs = [e.text.replace('\xa0', ' ').strip() for e in envs_raw]
    except AttributeError:
        envs = np.nan
    return envs


def get_benfs(soup):
    try:
        benfs_raw = soup.find(id='posting-benefits')
        benfs_raw = benfs_raw.find_all('dd', {'class': 'mb-0 text-truncate'})
        benfs = [b.text.replace('\xa0', ' ').strip() for b in benfs_raw]
    except AttributeError:
        benfs = np.nan
    return benfs


now = datetime.datetime.now()
now = now.strftime("%Y-%m-%d %H:%M:%S")

urls = pd.read_csv('nofluffjobs_urls.csv')
urls = [f'https://nofluffjobs.com{x}' for x in urls['urls']]
# urls = urls[-20:-10]
# urls = ['https://nofluffjobs.com/pl/job/technical-writer-with-python-devsdata-llc-remote-d1bj60dv']

data = []
for u in urls:
    print(u)
    page = requests.get(u, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")
    value_currency_contract = get_money(soup)

    scrape_dict = {'key': u.split('-')[-1]}
    scrape_dict['timestamp'] = now
    scrape_dict['link'] = u
    scrape_dict['title'] = get_title(soup)
    scrape_dict['company'] = get_company(soup)
    scrape_dict['level_low'] = get_level_low(soup)
    scrape_dict['level_high'] = get_level_high(soup)
    scrape_dict['primary_req'] = get_pri_req(soup)
    scrape_dict['secondary_req'] = get_sec_req(soup)
    for i in range(len(value_currency_contract)):
        scrape_dict[value_currency_contract[i][-1]
                    ] = value_currency_contract[i][:-1]
    scrape_dict['locations'] = get_locations(soup)
    scrape_dict['remote'] = get_remote(soup)
    scrape_dict['posting_time'] = get_posting_time(soup)
    scrape_dict['tasks'] = get_tasks(soup)
    scrape_dict['specs'] = get_specs(soup)
    scrape_dict['gear'] = get_gear(soup)
    scrape_dict['envs'] = get_envs(soup)
    scrape_dict['benfs'] = get_benfs(soup)
    data.append(scrape_dict)

# make dataframe and pivot it
df_data = pd.DataFrame(data)
df_data = pd.melt(df_data, id_vars=['key'])

# explode values in lists but keep original sorting
df_data = df_data.groupby('key', as_index=False)
df_data = df_data.apply(lambda x: x.reset_index(drop=True)).reset_index()
with contextlib.suppress(KeyError):
    df_data = df_data.drop('level_0', axis=1).set_index(
        'level_1').reset_index(drop=True)
df_data = df_data.explode('value').reset_index(drop=True)

# some uop and b2b are empty. remove them
missing_cur = df_data[df_data['value'].isnull()]
missing_cur = missing_cur[missing_cur['variable'].isin(
    ['brutto miesięcznie (UoP) oblicz netto',
     '+ vat (B2B) miesięcznie oblicz "na rękę"'])].index
df_data = df_data.drop(missing_cur).reset_index(drop=True)

# make propper uop and b2b
choices = ['B2B', 'UoP']
for k in df_data['key'].unique():
    df = df_data[df_data['key'] == k]
    for c in choices:
        if not df[df['variable'].str.contains(c)].empty:
            index = df[df['variable'].str.contains(c)]['value'].index
            df_data['variable'][index[0]] = f'{c}_cash_low'
            df_data['variable'][index[1]] = f'{c}_cash_high'
            df_data['variable'][index[2]] = f'{c}_cash_currency'

# save
df_data.to_csv('result.csv', index=False)
df_data.to_excel('result.xlsx', index=False)
