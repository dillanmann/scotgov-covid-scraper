import uuid
class Dataset:
    def __init__(self, date, total_tests, positive_tests, negative_tests, total_deaths, deaths_by_healthboard, id = None):
        self.date = date
        self.total_tests = total_tests
        self.positive_tests = positive_tests
        self.negative_tests = negative_tests
        self.total_deaths = total_deaths
        self.deaths_by_healthboard = deaths_by_healthboard
        self.id = uuid.uuid4()
        self.ayrshireandarran_deaths = deaths_by_healthboard['ayrshireandarran'],
        self.borders_deaths = deaths_by_healthboard['borders'],
        self.dumfriesandgalloway_deaths = deaths_by_healthboard['dumfriesandgalloway'],
        self.fife_deaths = deaths_by_healthboard['fife'],
        self.forthvalley_deaths = deaths_by_healthboard['forthvalley'],
        self.grampian_deaths = deaths_by_healthboard['grampian'],
        self.greaterglasgowandclyde_deaths = deaths_by_healthboard['greaterglasgowandclyde'],
        self.highland_deaths = deaths_by_healthboard['highland'],
        self.lanarkshire_deaths = deaths_by_healthboard['lanarkshire'],
        self.lothian_deaths = deaths_by_healthboard['lothian'],
        self.orkney_deaths = deaths_by_healthboard['orkney'],
        self.shetland_deaths = deaths_by_healthboard['shetland'],
        self.tayside_deaths = deaths_by_healthboard['tayside']