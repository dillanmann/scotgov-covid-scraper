from datetime import timedelta
import requests
import os
import sys
from src.scotgov_covid_scraper import ScotgovCovidScraper
from src.data_provider import DataProvider
from src.scraped_data_set import ScrapedDataSet
from src.calculated_data_set import CalculatedDataSet
from src.data_set import DataSet

def get_page__via_requests(url):
    return requests.get(url).text


if __name__ == "__main__":

    urls = ['https://www.gov.scot/publications/coronavirus-covid-19-tests-and-cases-in-scotland/']

    for url in urls:
        page_source = get_page__via_requests(url)

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

        scraped_data_set = ScrapedDataSet(total_tests, positive_cases,
                          negative_cases, total_deaths, cases_by_healthboard)

        with DataProvider() as provider:
            daily_deaths = scraped_data_set.total_deaths - provider.get_total_deaths_for_date(date - timedelta(days=1))
            print("daily deaths: " + str(daily_deaths))
            calculated_data_set = CalculatedDataSet(daily_deaths)

            dataset = DataSet(date, scraped_data_set, calculated_data_set)

            provider.upload_data(dataset)
