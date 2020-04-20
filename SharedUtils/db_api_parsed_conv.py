"""
API for parsed Conversations table, using the Wrapper module

Author: Shaya Weissberg
"""
import sqlite3

from .wrapper import Wrapper
import string


class ParsedConversationsAPI:

    def __init__(self, name):
        self.table_api = Wrapper(name)
        self.table_name = 'ParsedConversations'
        try:
            with self.table_api.cursor as cur:
                cur.execute("CREATE TABLE [IF NOT EXISTS] ParsedConversations (id INTEGER PRIMARY KEY AUTOINCREMENT, api TEXT,"
                                    " method TEXT, conversation BLOB")
        except sqlite3.Error as e:
            print("Failed to create Parsed Conversations table")  # TODO: change to log

    def save_conversation_by_api(self, api: string, method: string, conversation):

    def get_list_apis(self):
        return list_of_apis

    def get_conversations_for_api(self, api: string):
        return list_of_conversations

    def delete_conversations_for_api(self, api: string):
