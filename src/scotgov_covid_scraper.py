import re
from datetime import datetime
from bs4 import BeautifulSoup
import unicodedata

class ScotgovCovidScraper:
    def __init__(self, content):
        self.content = content
        self.soup = BeautifulSoup(self.content, 'html.parser')
        self.number_pattern = r'([0-9]+(?:,[0-9]+)?)'
        self.date_pattern = r'(\d{1,2}\s\w+\s\d{4})'
        self.total_tests_pattern = r'total of\s{0,1}([0-9]+(?:,[0-9]+)?)'
        self.date_selector = '#preamble h3'
        self.total_tests_selector = '#preamble > .body-content > p'
        self.negative_cases_selector = '#preamble > .body-content > ul > li'
        self.positive_cases_selector = '#preamble > .body-content > ul > li'
        self.total_deaths_selector = '#preamble > .body-content > ul > li'

    def get_element_text(self, selector):
        return self.soup.select_one(selector).get_text(strip=True)

    def get_date_from_element(self, element):
        return self.parse_date(element.text)

    def parse_date(self, text):
        date = re.search(self.date_pattern, text).group(1)
        return datetime.strptime(date, '%d %B %Y')

    def parse_number(self, text):
        return int(text.replace(',', ''))

    def get_number_from_element(self, selector):
        element_text = self.soup.select_one(selector).get_text(strip=True)
        element_value = self.parse_number(re.search(self.number_pattern, element_text).group(1))
        return element_value

    def get_date(self):
        for element in self.soup.select(self.date_selector):
            try:
                return self.get_date_from_element(element)
            except:
                pass
        
        raise Exception("failed to find date")
        

    def get_total_tests(self):
        for element in self.soup.select(self.total_tests_selector):
            text = element.get_text(strip=True)
            result = re.search(self.total_tests_pattern, text) 
            if result != None:
                return self.parse_number(result.group(1))
        
        raise Exception("failed to find total tests")

    def get_negative_cases(self):
        for element in self.soup.select(self.negative_cases_selector):
            text = element.get_text(strip=True)
            result = re.search(self.number_pattern, text) 
            if result != None and 'negative' in text:
                return self.parse_number(result.group(1))

        raise Exception("failed to find negative cases")

    def get_positive_cases(self):
        for element in self.soup.select(self.positive_cases_selector):
            text = element.get_text(strip=True)
            result = re.search(self.number_pattern, text) 
            if result != None and 'positive' in text:
                return self.parse_number(result.group(1))

        raise Exception("failed to find positive cases")

    def get_total_deaths(self):
        for element in self.soup.select(self.total_deaths_selector):
            text = element.get_text(strip=True)
            result = re.search(self.number_pattern, text) 
            if result != None and 'died' in text:
                return self.parse_number(result.group(1))

        # Deaths don't appear in every version of the site so return safe default
        return 0

    def get_health_board_cases(self):
        rows = len(self.soup.select('#preamble > div > table:nth-child(7) > tbody > tr'))
        data = {}
        for row in range(0, rows):
            board_selector = '#preamble > div > table:nth-child(7) > tbody > tr:nth-child({}) > td:nth-child(1)'.format(str(row+1))
            cases_selector = '#preamble > div > table:nth-child(7) > tbody > tr:nth-child({}) > td:nth-child(2)'.format(str(row+1))
            board = unicodedata.normalize('NFKD', self.soup.select_one(board_selector).get_text(strip=True)).replace(' ', '').lower()
            cases_text = self.soup.select_one(cases_selector).get_text(strip=True)
            result = re.search(self.number_pattern, cases_text)
            if result is None:
                continue
            cases = int(result.group(1).replace(',', ''))
            data[board] = cases

        if len(data) == 0:
            raise Exception("failed to find cases by health board")

        return data