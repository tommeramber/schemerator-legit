"""
specific use of the Wrapper module for the DB to Schemerator interface

Author: Shaya Weissberg
"""

from .Wrapper import Wrapper


class DBschemerator:

    def __init__(self, name):
        self.db = Wrapper(name)

    #####################################
    # conversation handling
    #####################################

    def get_all_conversations(self):
        return list_of_conversations

    def delete_one_conversation(self, unique_id: int):

    def delete_all_conversations(self):

    #####################################
    # apis handling
    #####################################

    def get_list_apis(self):
        return list_of_apis

    def get_conversations_for_api(self, api: string):
        return list_of_conversations

    def delete_conversations_for_api(self, api: string):

    #####################################
    # schema handling
    #####################################

    def save_schema(self, api: string, method: string, schema: blob):

    def get_schema_for_api(self, api: string, method: string):
        return schema

    def get_all_schemas(self):
        return list_of_schemas

    def delete_schema_for_api(self, api: string, method: string):

    def delete_all_schemas(self):


