import psycopg2
from src.data_set import Dataset
import os

class DataUploader:
    def __init__(self):
        self.conn = None
        self.insert_dataset_sql = """
            INSERT INTO datasets(
                id, date, total_tests, positive_tests, negative_tests, total_deaths,
                ayrshireandarran_deaths, borders_deaths, dumfriesandgalloway_deaths,
                fife_deaths, forthvalley_deaths, grampian_deaths, greaterglasgowandclyde_deaths,
                highland_deaths, lanarkshire_deaths, lothian_deaths, orkney_deaths, shetland_deaths,
                tayside_deaths) 
                VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                returning id;"""
        self.date_already_exists_sql ="""
            SELECT 1 FROM datasets WHERE date = %s;
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
            cur = self.conn.cursor()

   #     execute a statement
            print('PostgreSQL database version:')
            cur.execute('SELECT version()')
    
            # display the PostgreSQL database server version
            db_version = cur.fetchone()
            print(db_version)
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)                      

    def upload_data(self, data):

        if self.date_already_exists(data.date):
            raise SystemError('Data with date {} already exists'.format(str(data.date)))

        id = None
        try:
            cur = self.conn.cursor()

            cur.execute(insert_dataset_sql, (str(data.id), data.date, data.total_tests, data.positive_tests,
            data.negative_tests, data.total_deaths, data.ayrshireandarran_deaths, data.borders_deaths,
            data.dumfriesandgalloway_deaths, data.fife_deaths, data.forthvalley_deaths, data.grampian_deaths,
            data.greaterglasgowandclyde_deaths, data.highland_deaths, data.lanarkshire_deaths, data.lothian_deaths,
            data.orkney_deaths, data.shetland_deaths, data.tayside_deaths))

            id = cur.fetchone()[0]
            self.conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def date_already_exists(self, date):
        try:
            cur = self.conn.cursor()
            cur.execute(self.date_already_exists_sql, [date,])           

            result = cur.fetchone()[0]
            return True if result == 1 else False
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)