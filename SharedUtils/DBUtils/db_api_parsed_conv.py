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

    def save_conversation_by_api(self, api: string, method: string, conversation):
        self.save((api, method, pickle.dumps(conversation, 0)))


    def get_list_apis(self):
        # return list of apis, without duplications
        return list(dict.fromkeys(sum(self.get_column("api"), ())))

    def get_method_for_api(self, api: string):
        # return list of methods, for given api
        return list(sum(self.get('method', 'api="{}"'.format(api)), ()))

    def get_conversations_for_api(self, api: string, method: string):
        list_of_pikles = list(sum(self.get("conversation", 'api="{}" AND method ="{}"'.format(api, method)), ()))
        return list(map(pickle.loads, list_of_pikles))
        #return list_of_conversations

    def delete_conversations_for_api(self, api: string, method: string):
        pass
