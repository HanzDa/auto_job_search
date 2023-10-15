import psycopg2

from psycopg2.errors import UniqueViolation

from dotenv import dotenv_values


config = dotenv_values('.env')


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
        except psycopg2.Error as error:
            raise f"Error while connecting to PostgreSQL:\n {error}"

    def close_connection(self):
        try:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
        except psycopg2.Error as error:
            print("Error while closing the connection:", error)

    def execute_query(self, query):
        """ Execute and sql query.
            :params query: SQL query sentence

            return:
                boolean: True if is successful False otherwise.
        """
        try:
            self.connect()
            self.cursor.execute(query)
            return True
        except UniqueViolation as error:
            print(error)
            return False
