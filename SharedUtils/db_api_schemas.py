"""
API for schemas Conversations table, using the Wrapper module

Author: Shaya Weissberg
"""

from .wrapper import Wrapper
import string


class SchemasAPI:

    def __init__(self, name):
        self.table_api = Wrapper(name)
        self.TABLE_NAME = 'SchemasConversations'
        self.table_api.create_table(self.TABLE_NAME, "api TEXT NOT NULL, method TEXT NOT NULL, schema TEXT, "
                                                     "PRIMARY KEY (api, method)")

    def save_schema(self, api: string, method: string, schema):
        pass

    def get_schema_for_api(self, api: string, method: string):
        pass
        #return schema

    def get_all_schemas(self):
        pass
        #return list_of_schemas

    def delete_schema_for_api(self, api: string, method: string):
        pass

    def delete_all_schemas(self):
        pass
