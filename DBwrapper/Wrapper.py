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

    def __init__(self, name=None, config_file=None):
        self.db = None

        if name:
            if config_file:
                name = self.__name_from_config_file(config_file)
            self.__open_connection(name)

    # Privte method to open a db connetion.
    # Each container in Schemrator project has a well defined db table,
    # but thay all use the same db
    # @param name The name of the database to open.
    def __open_connection(self, name):  # TODO: maybe name from config file?
        try:
            self.connection = sqlite3.connect(name)

        except sqlite3.Error as e:
            print("Error connecting to database!")  # TODO: change to log

    # Privte method to claen op a db connetion
    def __close_connection(self):
        if self.db:
            self.db.commit()
            self.db.close()

    # For using in 'with' seatmates
    def __exit__(self, exc_type, exc_value, traceback):

        self.__close_connection()

    def __enter__(self):
        return self

    def __name_from_config_file(self, config_file):
        # TODO: implemantation
        return name

    ##################################
    # Generic db handling
    ##################################

    def insert(self, table_name, *data):
        self.data = ""
        for value in data:
            self.data += '"' + value + '"' + ','
        self.data = self.data[0:len(self.data) - 1]

        self.db.execute("INSERT INTO {} values({})".format(table_name, self.data))
        self.db.commit()

    def get_items(self, table_name, where=1):
        if (table_name != 1):
            self.where = where
            self.items = self.db.execute("SELECT * FROM {} WHERE {}".format(table_name, self.where))
            self.db.commit()
            return list(self.items)
        else:
            return {}

    def get_list_apis(self):

        return list_api

    def get_conversations_for_api(self, api: string):
        return

    def data_validation (self, data)
