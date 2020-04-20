"""
API for schemas Conversations table, using the Wrapper module

Author: Shaya Weissberg
"""


from .wrapper import Wrapper
import string


class ParsedConversationsAPI:

    def __init__(self, name):
        self.db = Wrapper(name)


    def save_schema(self, api: string, method: string, schema: blob):

    def get_schema_for_api(self, api: string, method: string):
        return schema

    def get_all_schemas(self):
        return list_of_schemas

    def delete_schema_for_api(self, api: string, method: string):

    def delete_all_schemas(self):
