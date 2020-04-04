import requests
import os
import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys  
from selenium.webdriver.chrome.options import Options  
from src.scotgov_covid_scraper import ScotgovCovidScraper
from src.data_uploader import DataUploader
from src.data_set import Dataset

if __name__ == "__main__":

    args = sys.argv
    if len(args) < 2:
        raise Exception(
            ('No URLS specified to parse. Provide urls by calling the program like: \n'
                'python program.py "<url>;<url>"'))

    urls = args[1].split(';')
    chrome_opts = Options()
    chrome_opts.add_argument("--headless")  
    chrome_opts.binary_location = 'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe'

    driver = webdriver.Chrome(chrome_options=chrome_opts)
    for url in urls:
        driver.get(url)

        if len(driver.find_elements_by_id('overview')) == 0:
            raise Exception("Failed to find root data element")

        covid_scraper = ScotgovCovidScraper(driver.page_source)

        date = None
        try:
            date = covid_scraper.get_date()
        except:
            date_in = input("no date found, enter date for URL {} in format DD MONTH YYYY".format(url))
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

        dataset = Dataset(date, total_tests, positive_cases, negative_cases, total_deaths, cases_by_healthboard)

        with DataUploader() as uploader:
            uploader.upload_data(dataset)