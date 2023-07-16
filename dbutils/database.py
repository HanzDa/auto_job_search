import psycopg2
from dotenv import dotenv_values


config = dotenv_values('../.env')


class Database:
    def __init__(self):
        self.conn = None
        self.cursor = None

    def connect(self):
        try:
            self.conn = psycopg2.connect(
                host=config['host'],
                port=config['port'],
                database=config['database'],
                user=config['user'],
                password=config['password']
            )
            self.cursor = self.conn.cursor()
        except (Exception, psycopg2.Error) as error:
            raise f"Error while connecting to PostgreSQL:\n {error}"

    def close_connection(self):
        try:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
        except (Exception, psycopg2.Error) as error:
            print("Error while closing the connection:", error)

    def execute_query(self, query):
        try:
            self.connect()
            self.cursor.execute(query)
        except (Exception, psycopg2.Error) as error:
            raise Exception(f'There was an error trying to execute the query:\n {error}')
