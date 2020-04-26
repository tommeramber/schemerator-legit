"""
A simple wrapper for sqlite DB in the context of Schemrator project
The purpose of this module is to hide all sqlite3 handling

Author: Shaya Weissberg
"""

import sqlite3
import json
import string
from contextlib import closing


def is_json(myjson):
    # used for data validation
    try:
        json.loads(myjson)
    except ValueError:
        return False
    return True


class Wrapper:

    def __init__(self, name):
        # open a db connection on init.
        # Each container in Schemrator project has a well defined db table,
        # but they all use the same db
        # @param name The name of the database to open.
        self.connection = None
        self.name = name
        self.__open_connection()

    def __del__(self):
        self.__close_connection()

    def __open_connection(self):
        # Private method to clean op a db connection
        try:
            self.connection = sqlite3.connect(self.name)
            self.cursor = self.connection.cursor()
        except sqlite3.Error as e:
            print("Error connecting to database! : {}".format(e))  # TODO: change to log
            raise e

    def __close_connection(self):
        #if self.connection:
        try:
            self.connection.commit()
            self.connection.close()
        except Exception as e:
            print("got closing exception {}".format(e))
            if self.connection != None:
                raise e

    def __enter__(self):
        # For using in 'with' seatmates
        self.__open_connection()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        # For using in 'with' seatmates
        self.__close_connection()



    def create_table(self, name: string, columns: string):  # TODO: do it nicer, columns not as one long string
        try:
            with closing(self.connection.cursor()) as cur:
                cur.execute("CREATE TABLE IF NOT EXISTS " + name + " (" + columns + ")")
        except sqlite3.Error as e:
            print("Failed to create table")  # TODO: change to log
            raise e

    def drop_table(self, name: string):  # TODO: test
        try:
            with closing(self.cursor) as cur:
                cur.execute("DROP TABLE " + name)
        except sqlite3.Error as e:
            print("Failed to drop table")  # TODO: change to log
            raise e

    def insert(self, table: string, columns: string, values: tuple):
        # insert values to tables. this func is not aware to the tables defined in db_apis
        place_holders = ''
        for i in values:
            place_holders += "?, "
        try:
            with closing(self.connection.cursor()) as cur:
                # TODO: sanitize against sql injection
                cur.execute("INSERT INTO {} {} VALUES ({})".format(table, columns, place_holders[:-2]), values)
        except sqlite3.Error as e:
            print("Failed to Insert")  # TODO: change to log
            raise e

    def select(self, columns: string, table: string, condition: string) -> list:
        # select value from tables.
        #
        try:
            with closing(self.connection.cursor()) as cur:
                # TODO: sanitize against sql injection
                cur.execute('SELECT {} FROM {} WHERE {}'.format(columns, table, condition))
                return cur.fetchall()
        except sqlite3.Error as e:
            print("Failed to SELECT")  # TODO: change to log
            raise e

#  def data_validation (self, data):
