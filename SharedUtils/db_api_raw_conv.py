"""
API for Raw Conversations table, using the Wrapper module

Author: Shaya Weissberg
"""
import sqlite3

from .wrapper import Wrapper
import string


class RawConversationsAPI:

    def __init__(self, name):
        self.table_api = Wrapper(name)
        self.table_name = 'RAW_CONVERSATIONS'
        try:
            with self.table_api.cursor as cur:
                cur.execute("CREATE TABLE [IF NOT EXISTS] RawConversations (id INTEGER PRIMARY KEY AUTOINCREMENT, url TEXT,"
                                    " method TEXT, reqheaders TEXT, req TEXT, resheaders TEXT, res TEXT)")
        except sqlite3.Error as e:
            print("Failed to create Raw Conversations table")  # TODO: change to log

    def save_one_conversation(self, url: string, method: string,  reqheaders: string,
                              req: string, resheaders: string, res: string):

    def save_all_conversations(self, list_of_conversations):

    def get_all_conversations(self):
        return  list_of_conversations

    def delete_one_conversation(self, unique_id: int):

    def delete_all_conversations(self):