import os
import time

import pandas as pd
import requests
from bs4 import BeautifulSoup

from config import FIRST_PAGE, NAME, headers


def get_job_urls(soup):
    """
    Extracts job URLs from the given BeautifulSoup object.
    Args:
        soup (BeautifulSoup): The BeautifulSoup object representing the HTML
        content.
    Returns:
        set: A set of job URLs.
    """
    all_links = soup.find_all('a', href=True)
    job_links = set(link['href']
                    for link in all_links if '/job/' in link['href'])
    return job_links


def is_last_page(current_urls, previous_urls):
    """
    Checks if the current page's URLs are the same as the previous page's URLs.
    Args:
        current_urls (set): The URLs of the current page.
        previous_urls (set): The URLs of the previous page.
    Returns:
        bool: True if the current page's URLs are the same as the previous
        page's URLs, False otherwise.
    """
    return current_urls == previous_urls


def scrape_job_urls():
    """
    Scrapes job URLs from a website and saves them to a CSV file.
    Returns:
        None
    """
    with requests.Session() as session:
        session.headers.update(headers)
        page_number = 1
        all_urls = set()
        previous_page_urls = set()
        while True:
            url = f"{FIRST_PAGE}{page_number}"
            response = session.get(url, timeout=10)
            print(f'Requesting: {url}, Status Code: {response.status_code}')
            soup = BeautifulSoup(response.content, "html.parser")
            current_page_urls = get_job_urls(soup)
            if not current_page_urls or is_last_page(current_page_urls,
                                                     previous_page_urls):
                print('No more jobs found or duplicate page detected')
                break
            print(f'Jobs found, page {page_number}')
            all_urls.update(current_page_urls)
            previous_page_urls = current_page_urls.copy()
            page_number += 1
            time.sleep(1)  # delay to prevent rapid requests
    urls_series = pd.Series(list(all_urls), name='urls')
    csv_file = f'data/urls/{NAME}_nofluffjobs_urls.csv'
    if not os.path.isfile(csv_file):
        urls_series.to_csv(csv_file, index=False)
    else:
        urls_series.to_csv(csv_file, mode='a', header=False, index=False)


scrape_job_urls()

df = pd.read_csv(f'data/urls/{NAME}_nofluffjobs_urls.csv')
