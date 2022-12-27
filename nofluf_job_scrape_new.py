import pandas as pd
import requests
from bs4 import BeautifulSoup
import re

from config import *

NAME = "ai_2022-12-27"
urls = pd.read_csv(f"data/{NAME}_nofluffjobs_urls.csv")
urls = [f"https://nofluffjobs.com{x}" for x in urls["urls"]]

df = pd.DataFrame(columns=[
    "job_title", "company_name", "experience_low", "experience_high",
    "UoP_currency", "UoP_cash_low", "UoP_cash_high",
    "B2B_currency", "B2B_cash_low", "B2B_cash_high", "is_remote", "location",
    "when_published", "primary_skils", "secondary_skils",
    "primary_requirements", "secondary_requirements", "offer_description",
    "tasks_list", "offer_details", "equipment", "metodology", "office_benefits",
    "additional_benefits"])


for u in urls[2:5]:
    print(u)
    u = "https://nofluffjobs.com/pl/job/senior-data-scientist-indata-labs-remote-uq8jmtqh"
    response = requests.get(u)

    # Parse the HTML content
    soup = BeautifulSoup(response.content, "html.parser")

    try:
        job_title = soup.find(
            "h1", {"class": "font-weight-bold bigger"}).text.strip()
    except AttributeError:
        job_title = soup.find("h1", {"class": "font-weight-bold"}).text.strip()

    company_name = soup.find("a", {"id": "postingCompanyUrl"}).text.strip()
    experience_low = soup.find("li", {"id": "posting-seniority"}).text.strip()
    try:
        experience_low = experience_low.split(", ")[0]
        experience_high = experience_low.split(", ")[1]
    except IndexError:
        experience_high = experience_low

    salaries = soup.find("common-posting-salaries-list")
    salaries = salaries.find_all("div", {"class": "salary ng-star-inserted"})
    salaries = [x.text.strip().replace("\xa0", "") for x in salaries]

    def extract_info(string):
        cash_low = int(re.search(r"^\d+", string).group())
        try:
            cash_high = int(re.search(r"\s+\d+\s+", string).group().strip())
        except AttributeError:
            cash_high = cash_low
        currency_code = re.search(r"[A-Z]{3}", string).group()
        contract_type = re.search(r"(B2B|UoP)", string).group()
        return cash_low, cash_high, currency_code, contract_type

    salary_dict = {}
    for salary in salaries:
        cash_low, cash_high, currency_code, contract_type = extract_info(
            salary)
        salary_dict[f"{contract_type}_currency"] = currency_code
        salary_dict[f"{contract_type}_cash_low"] = cash_low
        salary_dict[f"{contract_type}_cash_high"] = cash_high

    try:
        is_remote = soup.find(
            "li", {"class": "remote ng-star-inserted"}).text.strip()
    except AttributeError:
        is_remote = ["No"]

    try:
        location = soup.find("div", {
                             "class": "tw-flex tw-items-center cursor-pointer ng-star-inserted"}).text.strip()
    except AttributeError:
        location = ["No"]

    when_published = soup.find(
        "div", {"class": "posting-time-row ng-star-inserted"}).text.strip()

    primary_skils = soup.find("section", {"branch": "musts"}).find("ul")
    primary_skils = list(filter(None, [x.text.strip() for x in primary_skils]))
    primary_skils = ", ".join(str(e) for e in primary_skils)
    try:
        secondary_skils = soup.find(
            "section", {"id": "posting-nice-to-have"}).find("ul")
        secondary_skils = list(
            filter(None, [x.text.strip() for x in secondary_skils]))
    except AttributeError:
        secondary_skils = ["No"]
    secondary_skils = ", ".join(str(e) for e in secondary_skils)

    requirements = soup.find(
        "section", {"data-cy-section": "JobOffer_Requirements"})
    primary_requirements = list(
        filter(None, requirements.find_all("ul")[0].text.strip().split("\n")))
    try:
        secondary_requirements = list(
            filter(None, requirements.find_all("ul")[1].text.strip().split("\n")))
    except IndexError:
        secondary_requirements = ["No"]
    primary_requirements = ", ".join(str(e) for e in primary_requirements)
    secondary_requirements = ", ".join(str(e) for e in secondary_requirements)

    offer_description = soup.find("section", {"id": "posting-description"}).find(
        "div", {"class": "tw-overflow-hidden ng-star-inserted"}).text.strip()

    try:
        tasks_list = soup.find("section", {"id": "posting-tasks"})
        tasks_list = [x.text.strip()
                      for x in tasks_list.find("ol").find_all("li")]
    except AttributeError:
        tasks_list = ["No"]
    tasks_list = ", ".join(str(e) for e in tasks_list)

    offer_details = soup.find(
        "section", {"class": "d-block p-20 border-top"}).find("ul")
    offer_details = [x.text.strip() for x in offer_details.find_all("li")]
    offer_details = ", ".join(str(e) for e in offer_details)

    equipment = soup.find("section", {"id": "posting-equipment"}).find("ul")
    equipment = [x.text.strip() for x in equipment.find_all("li")]
    equipment = ", ".join(str(e) for e in equipment)

    try:
        metodology = soup.find(
            "section", {"id": "posting-environment"}).find("ul")
        metodology = [x.text.strip() for x in metodology.find_all("li")]
    except AttributeError:
        metodology = ["No"]
    metodology = ", ".join(str(e) for e in metodology)

    try:
        benefits = soup.find(
            "div", {"id": "posting-benefits"}).find_all("section")
        office_benefits = [x.text.strip() for x in benefits[0].find_all("li")]
        additional_benefits = [x.text.strip()
                               for x in benefits[1].find_all("li")]
    except IndexError:
        office_benefits = ["No"]
        additional_benefits = ["No"]
    office_benefits = ", ".join(str(e) for e in office_benefits)
    additional_benefits = ", ".join(str(e) for e in additional_benefits)

    # ! TODO integrate salary_dict with df
    
    df_combine = pd.DataFrame({
        "job_title": job_title,
        "company_name": company_name,
        "experience_low": experience_low,
        "experience_high": experience_high,
        "UoP_currency": UoP_currency,
        "UoP_cash_low": UoP_cash_low,
        "UoP_cash_high": UoP_cash_high,
        "B2B_currency": B2B_currency,
        "B2B_cash_low": B2B_cash_low,
        "B2B_cash_high": B2B_cash_high,
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
        "additional_benefits": additional_benefits
    })

    df = pd.concat([df, df_combine], ignore_index=False)
