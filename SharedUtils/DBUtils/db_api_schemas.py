"""
API for schemas Conversations table, using the Wrapper module

Author: Shaya Weissberg
"""
from .db_utils_api import DBUtilsAPI
from .wrapper import Wrapper
import string


class SchemasAPI(DBUtilsAPI):

    def __init__(self, DBname):
        DBUtilsAPI.__init__(self, DBname, 'SchemasConversations', "(api, method, schema)",
                            "api TEXT NOT NULL, method TEXT NOT NULL, schema TEXT, PRIMARY KEY (api, method)")
        self.create_table()

    def save_schema(self, api: string, method: string, schema):
        if self.get_schema_for_api(api, method):
            print("Replacing existing schema")  # TODO: change to log
            self.delete_schema_for_api(api, method)
        self.save((api, method, schema))

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
