import requests
import os
import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from src.scotgov_covid_scraper import ScotgovCovidScraper
from src.data_uploader import DataUploader
from src.data_set import Dataset

def get_page_selenium(url):
    chrome_opts = Options()
    chrome_opts.add_argument("--headless")
    chrome_opts.binary_location = 'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe'

    driver = webdriver.Chrome(chrome_options=chrome_opts)
    driver.get(url)
    return driver.page_source


def get_page_requests(url):
    return requests.get(url).text


if __name__ == "__main__":

    urls = ['https://www.gov.scot/coronavirus-covid-19/']

    for url in urls:
        page_source = get_page_requests(url)

        covid_scraper = ScotgovCovidScraper(page_source)

        date = None
        try:
            date = covid_scraper.get_date()
        except:
            date_in = input(
                "no date found, enter date for URL {} in format DD MONTH YYYY".format(url))
            date = covid_scraper.parse_date(date_in)

        print(date)

        total_tests = covid_scraper.get_total_tests()
        print("total tests: " + str(total_tests))

        positive_cases = covid_scraper.get_positive_cases()
        print("positive cases: " + str(positive_cases))

        negative_cases = covid_scraper.get_negative_cases()
        print("negative cases: " + str(negative_cases))

        total_deaths = covid_scraper.get_total_deaths()
        print("total deaths: " + str(total_deaths))

        cases_by_healthboard = covid_scraper.get_health_board_cases()
        print(cases_by_healthboard)

        dataset = Dataset(date, total_tests, positive_cases,
                          negative_cases, total_deaths, cases_by_healthboard)

        with DataUploader() as uploader:
            uploader.upload_data(dataset)
