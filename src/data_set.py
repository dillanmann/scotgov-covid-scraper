import uuid
class Dataset:
    def __init__(self, date, total_tests, positive_tests, negative_tests, total_deaths, cases_by_healthboard, id = None):
        self.date = date
        self.total_tests = total_tests
        self.positive_tests = positive_tests
        self.negative_tests = negative_tests
        self.total_deaths = total_deaths
        self.deaths_by_healthboard = cases_by_healthboard
        self.id = uuid.uuid4()
        self.ayrshireandarran_cases = cases_by_healthboard.get('ayrshireandarran', 0),
        self.borders_cases = cases_by_healthboard.get('borders', 0),
        self.dumfriesandgalloway_cases = cases_by_healthboard.get('dumfriesandgalloway', 0),
        self.fife_cases = cases_by_healthboard.get('fife', 0),
        self.forthvalley_cases = cases_by_healthboard.get('forthvalley', 0),
        self.grampian_cases = cases_by_healthboard.get('grampian', 0),
        self.greaterglasgowandclyde_cases = cases_by_healthboard.get('greaterglasgowandclyde', 0),
        self.highland_cases = cases_by_healthboard.get('highland', 0),
        self.lanarkshire_cases = cases_by_healthboard.get('lanarkshire', 0),
        self.lothian_cases = cases_by_healthboard.get('lothian', 0),
        self.orkney_cases = cases_by_healthboard.get('orkney', 0),
        self.shetland_cases = cases_by_healthboard.get('shetland', 0),
        self.tayside_cases = cases_by_healthboard.get('tayside', 0)