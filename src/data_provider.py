import psycopg2
from src.data_set import DataSet
import os

class DataProvider:
    def __init__(self):
        self.conn = None
        self.insert_scraped_dataset_sql = """
            INSERT INTO datasets(
                id, date, total_tests, positive_tests, negative_tests, total_deaths,
                ayrshireandarran_cases, borders_cases, dumfriesandgalloway_cases,
                fife_cases, forthvalley_cases, grampian_cases, greaterglasgowandclyde_cases,
                highland_cases, lanarkshire_cases, lothian_cases, orkney_cases, shetland_cases,
                tayside_cases) 
                VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
                """
        self.insert_calculated_dataset_sql = """
            INSERT INTO calculated_data(
                date, daily_deaths
            )
            VALUES(%s, %s);
        """
        self.date_already_exists_sql ="""
            SELECT 1 FROM datasets WHERE date = %s;
            """

        self.get_total_deaths_by_date_sql ="""
            SELECT total_deaths FROM datasets WHERE date = %s;
        """

    def __enter__(self): 
        self.connect()
        return self
  
    def __exit__(self, exc_type, exc_value, tb):
        if self.conn is not None:
            self.conn.close()
            print('Database connection closed.')
        
        if exc_type is not None:
            return False 
        
        return True

    def connect(self):
        """ Connect to the PostgreSQL database server """
        try:  
            # connect to the PostgreSQL server
            print('Connecting to the PostgreSQL database...')
            host = os.environ['SCOTGOV_COVID_DB_HOST']
            user = os.environ['SCOTGOV_COVID_DB_USER']
            password = os.environ['SCOTGOV_COVID_DB_PASSWORD']
            db_name = os.environ['SCOTGOV_COVID_DB_NAME']
            self.conn = psycopg2.connect(host=host, database=db_name, user=user, password=password)

            # create a cursor
            #cur = self.conn.cursor()

            # execute a statement
            #print('PostgreSQL database version:')
            #cur.execute('SELECT version()')
    
            # display the PostgreSQL database server version
            #db_version = cur.fetchone()
            #print(db_version)
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)                      

    def upload_data(self, dataset):

        date = dataset.date
        data = dataset.scraped_data_set
        calculated_data = dataset.calculated_data_set
        if self.date_already_exists(date):
            raise SystemError('Data with date {} already exists'.format(str(date)))

        try:
            cur = self.conn.cursor()

            cur.execute(self.insert_scraped_dataset_sql, (str(data.id), date, data.total_tests, data.positive_tests,
            data.negative_tests, data.total_deaths, data.ayrshireandarran_cases, data.borders_cases,
            data.dumfriesandgalloway_cases, data.fife_cases, data.forthvalley_cases, data.grampian_cases,
            data.greaterglasgowandclyde_cases, data.highland_cases, data.lanarkshire_cases, data.lothian_cases,
            data.orkney_cases, data.shetland_cases, data.tayside_cases))

            cur.execute(self.insert_calculated_dataset_sql, (date, calculated_data.daily_deaths))

            self.conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def get_total_deaths_for_date(self, date):
        try:
            cur = self.conn.cursor()

            cur.execute(self.get_total_deaths_by_date_sql, [date,])
            total_deaths = cur.fetchone()[0]
            cur.close()
            return total_deaths
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)


    def date_already_exists(self, date):
        try:
            cur = self.conn.cursor()
            cur.execute(self.date_already_exists_sql, [date,])           

            result = cur.fetchone() is not None
            cur.close()
            return result
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)