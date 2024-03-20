import mysql.connector


class Database:
    # Class attributes for database credentials
    host = 'localhost'
    username = 'root'
    password = ''
    database = 'campustube'

    def __init__(self):
        self.connection = None

    def connect(self):
        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.username,
            password=self.password,
            database=self.database
        )
        return self.connection

    def close(self):
        if self.connection:
            self.connection.close()

    def execute_query(self, query, params=None):
        self.connect()
        cursor = self.connection.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        self.close()
        return result

    def execute_insert(self, query, params):
        self.connect()
        cursor = self.connection.cursor()
        cursor.execute(query, params)
        self.connection.commit()
        cursor.close()
        self.close()
