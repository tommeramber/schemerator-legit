"""
A simple wrapper for sqlite DB in the context of Schemrator project
The purpose of this module is to give context aware methods for all the
containers in Schemrator project, to easily handle db

Author: Shaya Weissberg
"""

import sqlite3
import json


def is_json(myjson):
    try:
        json.loads(myjson)
    except ValueError:
        return False
    return True


class Wrapper:

    # open a db connection on init.
    # Each container in Schemrator project has a well defined db table,
    # but they all use the same db
    # @param name The name of the database to open.
    def __init__(self, name):
        try:
            self.connection = sqlite3.connect(name)
            self.cursor = self.connection.cursor()

        except sqlite3.Error as e:
            print("Error connecting to database!")  # TODO: change to log



    # Private method to clean op a db connection
    def __close_connection(self):
        self.connection.commit()
        self.cursor.close()
        self.connection.close()

    # For using in 'with' seatmates
    def __exit__(self, exc_type, exc_value, traceback):
        self.__close_connection()

    def __enter__(self):
        return self


    ##################################
    # Generic db handling
    ##################################

    def insert(self, table_name, *data):
        self.data = ""
        for value in data:
            self.data += '"' + value + '"' + ','
        self.data = self.data[0:len(self.data) - 1]

        self.cursor.execute("INSERT INTO {} values({})".format(table_name, self.data))
        self.cursor.commit()

    def get_items(self, table_name, where=1):
        if (table_name != 1):
            self.where = where
            self.items = self.cursor.execute("SELECT * FROM {} WHERE {}".format(table_name, self.where))
            self.cursor.commit()
            return list(self.items)
        else:
            return {}


    def data_validation (self, data)
