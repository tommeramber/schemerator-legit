"""
API for parsed Conversations table, using the Wrapper module

Author: Shaya Weissberg
"""
from SharedUtils.DBUtils.db_utils_api import DBUtilsAPI
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

    def get_list_apis(self) -> list:
        # return list of apis, without duplications
        return list(dict.fromkeys(sum(self.get_column("api"), ())))

    def get_list_methods_for_api(self, api) -> list:
        # return list of apis, without duplications
        return list(dict.fromkeys(sum(self.get_column_where("method", 'api="{}"'.format(api)), ())))

    def get_method_for_api(self, api: string) -> list:
        # return list of methods, for given api
        return list(sum(self.get('method', 'api="{}"'.format(api)), ()))

    def get_conversations_for_api(self, api: string, method: string) -> list:
        # return list of conversations
        list_of_pikles = list(sum(self.get("conversation", 'api="{}" AND method ="{}"'.format(api, method)), ()))
        return list(map(pickle.loads, list_of_pikles))

    def get_all_conversations(self) -> list:
        all_tables = list(sum(self.get_all_table(), ()))
        num_of_pickels = int(len(all_tables)/3)
        index = -1
        all_conversations = []
        for i in range(num_of_pickels):
            index += 3 #get the conversation index
            all_conversations.append(pickle.loads(all_tables[index]))
        return all_conversations

    def delete_conversations_for_api(self, api: string, method: string):
        pass
