
import os

import pandas as pd
import requests
from bs4 import BeautifulSoup

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36", "Accept-Encoding": "gzip, deflate",
           "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT": "1", "Connection": "close", "Upgrade-Insecure-Requests": "1"}

for i in range(1, 20):
    URL = f'https://nofluffjobs.com/artificial-intelligence?page={i}'
    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")
    soup = BeautifulSoup(soup.prettify(), "html.parser")
    req = soup.find('div', {'class': 'list-container ng-star-inserted'})
    if req is not None:
        print(f'jobs found, page {i}')
        urls = [link.get('href') for link in soup.find_all('a')]
        urls = pd.Series([x for x in urls if '/pl/job/' in x], name='urls')
        # if nofluffjobs_urls.csv does not exist then create else append
        if not os.path.isfile('nofluffjobs_urls.csv'):
            urls.to_csv('nofluffjobs_urls.csv', index=False)
        else:
            urls.to_csv('nofluffjobs_urls.csv', mode='a',
                        header=False, index=False)
    else:
        print('No more jobs found')
        break
