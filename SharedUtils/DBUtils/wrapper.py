"""
A simple wrapper for sqlite DB in the context of Schemrator project
The purpose of this module is to give context aware methods for all the
containers in Schemrator project, to easily handle db

Author: Shaya Weissberg
"""

import sqlite3
import json
import string
from contextlib import closing


def is_json(myjson):    # used for data validation
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
        self.connection = None
        self.cursor = None
        self.name = name
        self.__open_connection()

    # Private method to clean op a db connection
    def __open_connection(self):
        try:
            self.connection = sqlite3.connect(self.name)
            self.cursor = self.connection.cursor()
        except sqlite3.Error as e:
            print("Error connecting to database!")  # TODO: change to log
            raise e

    def __close_connection(self):
        if self.connection:
            self.connection.commit()
            self.cursor.close()
            self.connection.close()

    # For using in 'with' seatmates
    def __enter__(self):
        self.__open_connection()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.__close_connection()

    def __delete__(self, instance):
        self.__close_connection()

    def create_table(self, name: string, columns: string):  #TODO: do it nicer, columns not as one long string
        try:
            with closing(self.cursor) as cur:
                cur.execute("CREATE TABLE IF NOT EXISTS " + name + " (" + columns + ")")
        except sqlite3.Error as e:
            print("Failed to create Raw Conversations table")  # TODO: change to log
            raise e


  #  def insert(self, table, data):
  #     with closing(self.cursor) as cur:
  #          cur.execute("INSERT INTO ? ()", (table,  ))

  #  def data_validation (self, data):
