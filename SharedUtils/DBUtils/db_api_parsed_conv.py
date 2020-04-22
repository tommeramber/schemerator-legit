"""
API for parsed Conversations table, using the Wrapper module

Author: Shaya Weissberg
"""
from .db_utils_api import DBUtilsAPI
import string
import pickle


class ParsedConversationsAPI(DBUtilsAPI):

    def __init__(self, DBname):
        DBUtilsAPI.__init__(self, DBname, 'ParsedConversations', "(api, method, conversation)",
                            "id INTEGER PRIMARY KEY AUTOINCREMENT, api TEXT,"
                            " method TEXT, conversation BLOB")
        self.create_table()

    def save_conversation_by_api(self, api: string, method: string, conversation):  #TODO: method include already in conv
        self.save((api, method, pickle.dumps(conversation, 0)))


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
