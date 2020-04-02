import requests
import os
from bs4 import BeautifulSoup
from src.scotgov_covid_scraper import ScotgovCovidScraper
from src.data_uploader import DataUploader
from src.data_set import Dataset

if __name__ == "__main__":

    page = requests.get("https://www.gov.scot/coronavirus-covid-19/")
    soup = BeautifulSoup(page.content, 'html.parser')

    covid_scraper = ScotgovCovidScraper(soup)

    date = covid_scraper.get_date()
    print(date)

    total_tests = covid_scraper.get_total_infected()
    print("total tests: " + str(total_tests))

    positive_cases = covid_scraper.get_positive_cases()
    print("positive cases: " + str(positive_cases))

    negative_cases = covid_scraper.get_negative_cases()
    print("negative cases: " + str(negative_cases))

    total_deaths = covid_scraper.get_total_deaths()
    print("total deaths: " + str(total_deaths))

    deaths_by_healthboard = covid_scraper.get_health_board_deaths()
    print(deaths_by_healthboard)

    dataset = Dataset(date, total_tests, positive_cases, negative_cases, total_deaths, deaths_by_healthboard)

    with DataUploader() as uploader:
        uploader.upload_data(dataset)