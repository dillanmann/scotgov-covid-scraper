import re
from datetime import datetime

class ScotgovCovidScraper:
    def __init__(self, soup):
        self.soup = soup
        self.number_pattern = r'([0-9]+(?:,[0-9]+)?)'
        self.date_pattern = r'(\d{2}\s\w+\s2020)'


    def get_element_text(self, selector):
        return self.soup.select_one(selector).get_text()

    def get_date_from_element(self, selector):
        text = self.get_element_text(selector)
        date = re.search(self.date_pattern, text).group(1)
        return datetime.strptime(date, '%d %B %Y')

    def get_number_from_element(self, selector):
        element_text = self.soup.select_one(selector).get_text()
        element_value = int(re.search(self.number_pattern, element_text).group(1).replace(',', ''))
        return element_value

    def get_date(self):
        return self.get_date_from_element('#overview > h3:nth-child(11)')

    def get_total_infected(self):
        return self.get_number_from_element('#overview > p:nth-child(12) > span:nth-child(2) > span > span > span')

    def get_negative_cases(self):
        return self.get_number_from_element('#overview > ul:nth-child(13) > li:nth-child(1)')

    def get_positive_cases(self):
        return self.get_number_from_element('#overview > ul:nth-child(13) > li:nth-child(2)')

    def get_total_deaths(self):
        return self.get_number_from_element('#overview > ul:nth-child(13) > li:nth-child(3)')

    def get_health_board_deaths(self):
        rows = len(self.soup.select('#overview > table > tbody > tr'))
        data = {}
        for row in range(2, rows):
            board_selector = '#overview > table > tbody > tr:nth-child({}) > td:nth-child(1)'.format(str(row))
            deaths_selector = '#overview > table > tbody > tr:nth-child({}) > td:nth-child(2)'.format(str(row))
            board = self.soup.select_one(board_selector).get_text().strip().replace(' ', '').lower()
            deaths_text = self.soup.select_one(deaths_selector).get_text().strip()
            deaths = int(re.search(self.number_pattern, deaths_text).group(1).replace(',', ''))
            data[board] = deaths

        return data