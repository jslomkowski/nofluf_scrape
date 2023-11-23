"""
This module contains a script that scrapes job offers from nofluffjobs.com
website. The script reads urls from a csv file, scrapes the data from each url,
and saves the results in a csv and xlsx file. The scraped data includes job
title, company name, experience level, salary information, location, skills,
requirements, offer description, tasks list, offer details, equipment,
methodology, office benefits, and additional benefits.
"""
import contextlib
import os
import re
import sys

import pandas as pd
import requests
from bs4 import BeautifulSoup

from config import NAME

with contextlib.suppress(FileExistsError):
    os.mkdir(f"data/results/{NAME}")

urls = pd.read_csv(f"data/urls/{NAME}_nofluffjobs_urls.csv")
urls = [f"https://nofluffjobs.com{x}" for x in urls["urls"]]

df_all = pd.DataFrame(columns=[
    "job_title", "link", "company_name", "experience_low", "experience_high",
    "employment_currency", "employment_cash_low", "employment_cash_high",
    "B2B_currency", "B2B_cash_low", "B2B_cash_high",
    "UoD_currency", "UoD_cash_low", "UoD_cash_high",
    "mandate_currency", "mandate_cash_low", "mandate_cash_high",
    "is_remote", "location",
    "when_published", "primary_skils", "secondary_skils",
    "primary_requirements", "secondary_requirements", "offer_description",
    "tasks_list", "offer_details", "equipment", "metodology", "office_benefits",
    "additional_benefits"])

for u in urls:
    print(u)

    extract = {}
    try:
        with open("data/offers/" + u[31:], "r", encoding="utf-8") as file:
            soup = BeautifulSoup(file.read(), "html.parser")
    except FileNotFoundError:
        response = requests.get(u, timeout=10)
        soup = BeautifulSoup(response.content, "html.parser")
        with open("data/offers/" + u[31:], "w", encoding="utf-8") as file:
            file.write(str(soup))

    if "504 Gateway Time-out" in soup.text.strip():
        print('Error 504 Gateway Time-out. Exiting.')
        sys.exit(1)

    try:
        job_title = soup.find(
            "h1", {"class": "font-weight-bold bigger"}).text.strip()
    except AttributeError:
        job_title = soup.find(
            "h1", {"class": "font-weight-bold"}).text.strip()
    extract["job_title"] = job_title

    extract["link"] = u

    extract["company_name"] = soup.find(
        "a", {"id": "postingCompanyUrl"}).text.strip()

    experience_low = soup.find("li", {"id": "posting-seniority"}).text.strip()
    try:
        extract["experience_low"] = experience_low.split(", ")[0]
        extract["experience_high"] = experience_low.split(", ")[1]
    except IndexError:
        extract["experience_high"] = experience_low

    salaries = soup.find("common-posting-salaries-list")
    salaries = salaries.find_all("div", {"class": "salary ng-star-inserted"})
    salaries = [x.text.strip().replace("\xa0", "") for x in salaries]

    def extract_info(salary):
        """Extracts salary information from a string."""
        try:
            cash_low = int(re.search(r"^\d+", salary).group())
            try:
                cash_high = int(
                    re.search(r"\s+\d+\s+", salary).group().strip())
            except AttributeError:
                cash_high = cash_low
            currency_code = re.search(r"[A-Z]{3}", salary).group()
            contract_type = re.search(
                r"(B2B|employment|UoD|mandate)", salary).group()
        except AttributeError:
            cash_low = None
            cash_high = None
            currency_code = None
            contract_type = "Unpaid internship"
        return cash_low, cash_high, currency_code, contract_type

    for salary in salaries:
        cash_low, cash_high, currency_code, contract_type = extract_info(
            salary)
        extract[f"{contract_type}_currency"] = currency_code
        extract[f"{contract_type}_cash_low"] = cash_low
        extract[f"{contract_type}_cash_high"] = cash_high

    try:
        if soup.find("li", {"class": "remote ng-star-inserted"}).text.strip() == "Zdalnie":
            extract["is_remote"] = "Yes"
    except AttributeError:
        extract["is_remote"] = "No"

    try:
        extract["location"] = soup.find("div", {
            "class": "tw-flex tw-items-center cursor-pointer ng-star-inserted"}).text.strip()
    except AttributeError:
        extract["location"] = "No"

    extract["when_published"] = soup.find(
        "div", {"class": "posting-time-row ng-star-inserted"}).text.strip()

    primary_skils = soup.find("section", {"branch": "musts"}).find("ul")
    primary_skils = list(filter(None, [x.text.strip() for x in primary_skils]))
    extract["primary_skils"] = ", ".join(str(e) for e in primary_skils)
    try:
        secondary_skils = soup.find(
            "section", {"id": "posting-nice-to-have"}).find("ul")
        secondary_skils = list(
            filter(None, [x.text.strip() for x in secondary_skils]))
    except AttributeError:
        secondary_skils = [False]
    extract["secondary_skils"] = ", ".join(str(e) for e in secondary_skils)

    requirements = soup.find(
        "section", {"data-cy-section": "JobOffer_Requirements"})

    try:
        primary_requirements = list(
            filter(None, requirements.find_all("ul")[0].text.strip().split("\n")))
    except (AttributeError, IndexError):
        primary_requirements = [False]

    try:
        secondary_requirements = list(
            filter(None, requirements.find_all("ul")[1].text.strip().split("\n")))
    except (AttributeError, IndexError):
        secondary_requirements = [False]

    extract["primary_requirements"] = ", ".join(
        str(e) for e in primary_requirements)
    extract["secondary_requirements"] = ", ".join(
        str(e) for e in secondary_requirements)

    try:
        extract["offer_description"] = soup.find(
            "section", {"id": "posting-description"}).find(
                "div", {"class": "tw-overflow-hidden ng-star-inserted"}).text.strip()
    except AttributeError:
        extract["offer_description"] = False

    try:
        tasks_list = soup.find("section", {"id": "posting-tasks"})
        tasks_list = [x.text.strip()
                      for x in tasks_list.find("ol").find_all("li")]
    except AttributeError:
        tasks_list = [False]
    extract["tasks_list"] = ", ".join(str(e) for e in tasks_list)

    offer_details = soup.find(
        "section", {"class": "d-block p-20 border-top"}).find("ul")
    offer_details = [x.text.strip() for x in offer_details.find_all("li")]
    extract["offer_details"] = ", ".join(str(e) for e in offer_details)

    try:
        equipment = soup.find(
            "section", {"id": "posting-equipment"}).find("ul")
        equipment = [x.text.strip() for x in equipment.find_all("li")]
        extract["equipment"] = ", ".join(str(e) for e in equipment)
    except AttributeError:
        extract["equipment"] = False

    try:
        metodology = soup.find(
            "section", {"id": "posting-environment"}).find("ul")
        metodology = [x.text.strip() for x in metodology.find_all("li")]
    except AttributeError:
        metodology = [False]
    extract["metodology"] = ", ".join(str(e) for e in metodology)

    try:
        benefits = soup.find(
            "div", {"id": "posting-benefits"}).find_all("section")
        office_benefits = [x.text.strip() for x in benefits[0].find_all("li")]
        additional_benefits = [x.text.strip()
                               for x in benefits[1].find_all("li")]
    except IndexError:
        office_benefits = [False]
        additional_benefits = [False]
    extract["office_benefits"] = ", ".join(
        str(e) for e in office_benefits)
    extract["additional_benefits"] = ", ".join(
        str(e) for e in additional_benefits)

    df_extract = pd.DataFrame([extract], columns=df_all.columns)
    df_all = pd.concat([df_all, df_extract], ignore_index=True)

df_all.to_csv(f"data/results/{NAME}/{NAME}_output.csv", index=False, sep="|")
df_all.to_excel(f"data/results/{NAME}/{NAME}_output.xlsx", index=False)
