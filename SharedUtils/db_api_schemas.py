"""
API for schemas Conversations table, using the Wrapper module

Author: Shaya Weissberg
"""
import sqlite3

from .wrapper import Wrapper
import string


class SchemasAPI:

    def __init__(self, name):
        self.table_api = Wrapper(name)
        self.table_name = 'SchemasConversations'
        try:
            with self.table_api.cursor as cur:
                cur.execute("CREATE TABLE [IF NOT EXISTS] Schemas (api TEXT NOT NULL, method TEXT NOT NULL, schema TEXT"
                            "PRIMARY KEY (api, method)")
        except sqlite3.Error as e:
            print("Failed to create Schemas table")  # TODO: change to log

    def save_schema(self, api: string, method: string, schema: blob):

    def get_schema_for_api(self, api: string, method: string):
        return schema

    def get_all_schemas(self):
        return list_of_schemas

    def delete_schema_for_api(self, api: string, method: string):

    def delete_all_schemas(self):
