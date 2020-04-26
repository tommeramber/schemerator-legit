"""
API for schemas Conversations table, using the Wrapper module

Author: Shaya Weissberg
"""
from SharedUtils.DBUtils.db_utils_api import DBUtilsAPI
import string


class SchemasAPI(DBUtilsAPI):

    def __init__(self, DBname):
        DBUtilsAPI.__init__(self, DBname, 'Schemas', "(api, method, schema)",
                            "api TEXT NOT NULL, method TEXT NOT NULL, schema TEXT, PRIMARY KEY (api, method)")
        self.create_table()

    def save_schema(self, api: string, method: string, schema):
        #if self.get_schema_for_api(api, method): # TODO: check if neccesary
            #print('Replacing existing schema')  # TODO: change to log
            #self.delete_schema_for_api(api, method)
        self.save((api, method, schema))

    def get_schema_for_api(self, api: string, method: string) -> string:
        # return schema as a string, out of list of tuple
        return self.get("schema", 'api="{}" AND method ="{}"'.format(api, method))[0][0] #TODO: looks a bit shitty

    def get_all_schemas(self) -> list:
        return list(sum(self.get_column("schema"), ()))

    def delete_schema_for_api(self, api: string, method: string):
        pass

    def delete_all_schemas(self):
        pass
