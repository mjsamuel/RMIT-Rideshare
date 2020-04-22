import os

import MySQLdb
import configparser

class DatabaseUtil:
    __CONFIG = configparser.ConfigParser()

    def __init__(self, connection = None):
        self.__CONFIG.read(os.path.join(
            os.path.dirname(__file__),
            os.pardir,
            os.pardir,
            'config.ini'))
        if(connection == None):
            connection = MySQLdb.connect(
                self.__CONFIG['DEFAULT']['HOST'],
                self.__CONFIG['DEFAULT']['USER'],
                self.__CONFIG['DEFAULT']['PASSWORD'],
                self.__CONFIG['DEFAULT']['DATABASE'])
        self.__connection = connection

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def close(self):
        self.__connection.close()

    def create_user_table(self):
        with self.__connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    username VARCHAR(30) NOT NULL PRIMARY KEY,
                    password VARCHAR(30) NOT NULL)
                """)
        self.__connection.commit()

    def insert_user(self, name, password):
        with self.__connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO users (username, password)
                VALUES (%s, %s)
            """, [name, password])
        self.__connection.commit()

        return cursor.rowcount == 1

    def get_user(self, username):
        with self.__connection.cursor() as cursor:
            cursor.execute("""
                SELECT *
                  FROM users
                 WHERE username = %s
            """, [username])
            return cursor.fetchall()
