"""
API for Raw Conversations table, using the Wrapper module

Author: Shaya Weissberg
"""

from .wrapper import Wrapper
import string


class RawConversationsAPI:

    def __init__(self, name):
        self.table_api = Wrapper(name)
        self.TABLE_NAME = 'RawConversations'
        self.table_api.create_table(self.TABLE_NAME, "id INTEGER PRIMARY KEY AUTOINCREMENT, url TEXT,"
                                                     " method TEXT, reqheaders TEXT, req TEXT,"
                                                     " resheaders TEXT, res TEXT")

    def save_one_conversation(self, url: string, method: string, reqheaders: string,
                              req: string, resheaders: string, res: string):
        values = (url, method, reqheaders, req, resheaders, res)
        self.table_api.insert(self.TABLE_NAME, values)

    def save_all_conversations(self, list_of_conversations):
        pass

    def get_all_conversations(self):
        pass
        # return  list_of_conversations

    def delete_one_conversation(self, unique_id: int):
        pass

    def delete_all_conversations(self):
        pass
