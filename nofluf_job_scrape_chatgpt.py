import csv
import contextlib
import datetime
import re

import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
from config import *


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
    # def find_req(req):
    #     req_list = []
    #     find_dict = {'object': 'btn btn-outline-success btn-sm text-truncate',
    #                  'class': 'btn btn-outline-success btn-sm no-cursor text-truncate ng-star-inserted'}
    #     for k, v in find_dict.items():
    #         rows = req.find_all(k, {'class': v})
    #         req_list.extend(r.get_text().strip() for r in rows)
    #     return req_list
    def find_req(req):
        req_list = []
        for p in req.find_all('p'):
            if p.text.startswith('Skills and experience you will need'):
                for li in p.next_sibling.find_all('li'):
                    req_list.append(li.text)
        return req_list
    req = soup.find_all(
        'div', {'class': 'tw-overflow-hidden ng-star-inserted'})
    primary_req_list = find_req(req[0])
    return primary_req_list


def get_sec_req(soup):
    def find_req(req):
        req_list = []
        find_dict = {'object': 'btn btn-outline-success btn-sm text-truncate',
                     'button': 'btn btn-outline-success btn-sm no-cursor text-truncate'}
        for k, v in find_dict.items():
            rows = req.find_all(k, {'class': v})
            req_list.extend(r.get_text().strip() for r in rows)
        return req_list
    req = soup.find_all('h3', {'class': 'mb-0'})
    secondary_req_list = find_req(req[1]) if len(req) > 1 else []
    return secondary_req_list


def get_money(soup):
    value_currency_contract = []
    cash_list_class = soup.find_all('div', {'class': "salary"})
    try:
        for cash_class in cash_list_class:
            if """salary ng-star-inserted""" in str(cash_class):
                cash = cash_class.find('h4', {'class': 'tw-mb-0'}).get_text()
                cash = re.sub(r'\s(?=\s)', '', re.sub(
                    r'\s', ' ', cash)).strip()
                cash = re.sub(r'(\d)\s+(\d)', r'\1\2', cash)
                value = [int(s) for s in cash.split() if s.isdigit()]
                currency = [str(s) for s in cash.split() if not s.isdigit()]
                if '-' in currency:
                    currency.remove('-')
                currency = ', '.join(str(e) for e in currency)
                contract = cash_class.find('div', {
                    'class': 'font-weight-medium text-success'}).get_text().strip()
                value_currency_contract.append(
                    [value[0], currency, contract])
            elif """salary ng-star-inserted""" not in str(cash_class):
                cash = cash_class.find('h4', {'class': 'tw-mb-0'}).get_text()
                cash = re.sub(r'\s(?=\s)', '', re.sub(
                    r'\s', ' ', cash)).strip()
                cash = re.sub(r'(\d)\s+(\d)', r'\1\2', cash)
                value = [int(s) for s in cash.split() if s.isdigit()]
                currency = [str(s) for s in cash.split() if not s.isdigit()]
                if '-' in currency:
                    currency.remove('-')
                currency = ', '.join(str(e) for e in currency)
                contract = cash_class.find(
                    'div', {'class': 'font-weight-medium'}).get_text().strip()
                value_currency_contract.append(
                    [value[0], currency, contract])
    except AttributeError:
        value_currency_contract.append(['', '', ''])
    return value_currency_contract


def get_description(soup):
    try:
        description_class = soup.find(
            'div', {'class': 'job-description'}).get_text().strip()
    except AttributeError:
        description_class = ''
    return description_class


def get_location(soup):
    try:
        location_class = soup.find(
            'div', {'class': 'font-weight-medium'}).get_text().strip()
    except AttributeError:
        location_class = ''
    return location_class


def get_apply_link(soup):
    try:
        link_class = soup.find(
            'a', {'class': 'btn btn-primary py-2 px-4'})['href']
    except TypeError:
        link_class = ''
    return link_class


def get_apply_email(soup):
    try:
        email_class = soup.find(
            'div', {'class': 'font-weight-medium text-secondary'}).get_text().strip()
    except AttributeError:
        email_class = ''
    return email_class


def get_apply_phone(soup):
    try:
        phone_class = soup.find(
            'div', {'class': 'font-weight-medium text-secondary'}).get_text().strip()
    except AttributeError:
        phone_class = ''
    return phone_class


def get_apply_person(soup):
    try:
        person_class = soup.find(
            'div', {'class': 'font-weight-medium text-secondary'}).get_text().strip()
    except AttributeError:
        person_class = ''
    return person_class


def main(u):

    # Make a GET request to the website
    response = requests.get(u)

    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Get the job title
    title = get_title(soup)

    # Get the company name
    company = get_company(soup)

    # Get the low and high levels of the job
    level_low = get_level_low(soup)
    level_high = get_level_high(soup)

    # Get the primary requirements for the job
    primary_req_list = get_pri_req(soup)

    # Get the secondary requirements for the job
    secondary_req_list = get_sec_req(soup)

    # Get the salary details for the job
    value_currency_contract = get_money(soup)

    # Get the job description
    description = get_description(soup)

    # Get the location of the job
    location = get_location(soup)

    # Get the apply link for the job
    apply_link = get_apply_link(soup)

    # Get the apply email for the job
    apply_email = get_apply_email(soup)

    # Get the apply phone number for the job
    apply_phone = get_apply_phone(soup)

    # Get the apply person for the job
    apply_person = get_apply_person(soup)

    # Write the job details to a CSV file
    with open('jobs.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([title, company, level_low, level_high, primary_req_list,
                         secondary_req_list, value_currency_contract, description, location, apply_link, apply_email, apply_phone, apply_person])


if __name__ == '__main__':
    urls = pd.read_csv(f'data/{NAME}_nofluffjobs_urls.csv')
    urls = [f'https://nofluffjobs.com{x}' for x in urls['urls']]
    for u in [urls[0]]:
        print(u)
        main(u)
