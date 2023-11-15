"""This module scrapes job URLs from a website and saves them to a CSV file."""

import os

import pandas as pd
import requests
from bs4 import BeautifulSoup

from config import FIRST_PAGE, NAME, headers

for i in range(1, 999):
    url = f'{FIRST_PAGE[1:-2]}{i}'
    page = requests.get(url, headers=headers, timeout=10)
    soup = BeautifulSoup(page.content, "html.parser")
    soup = BeautifulSoup(soup.prettify(), "html.parser")
    req = soup.find('div', {'class': 'list-container ng-star-inserted'})
    if req is not None:
        print(f'jobs found, page {i}')
        urls = [link.get('href') for link in soup.find_all('a')]
        urls = pd.Series([x for x in urls if '/pl/job/' in x], name='urls')
        if not os.path.isfile(f'data/urls/{NAME}_nofluffjobs_urls.csv'):
            urls.to_csv(f'data/urls/{NAME}_nofluffjobs_urls.csv', index=False)
        else:
            urls.to_csv(f'data/urls/{NAME}_nofluffjobs_urls.csv', mode='a',
                        header=False, index=False)
    else:
        print('No more jobs found')
        break
