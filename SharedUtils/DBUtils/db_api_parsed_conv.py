"""
API for parsed Conversations table, using the Wrapper module

Author: Shaya Weissberg
"""

from .wrapper import Wrapper
import string
import pickle


class ParsedConversationsAPI:

    def __init__(self, name):
        self.table_api = Wrapper(name)
        self.TABLE_NAME = 'ParsedConversations'
        self.table_api.create_table(self.TABLE_NAME, "id INTEGER PRIMARY KEY AUTOINCREMENT, api TEXT,"
                                                     " method TEXT, conversation BLOB")

    def save_conversation_by_api(self, api: string, method: string, conversation):
        self.table_api.insert(self.TABLE_NAME, (api, method, pickle.dumps(0, conversation)))
        pass

    def get_list_apis(self):
        pass
        #return list_of_apis

    def get_method_for_api(self, api: string):
        return

    def get_conversations_for_api(self, api: string, mathod: string):
        pass
        #return list_of_conversations

    def delete_conversations_for_api(self, api: string, mathod: string):
        pass
