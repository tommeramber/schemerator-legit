"""
API for Raw Conversations table, using the Wrapper module

Author: Shaya Weissberg
"""


from .wrapper import Wrapper
import string


class RawConversationsAPI:

    def __init__(self, name):
        self.db = Wrapper(name)

    def save_one_conversation(self, url: string, method: string,  reqheaders: string,
                              req: string, resheaders: string, res: string):

    def save_all_conversations(self, list_of_conversations):

    def get_all_conversations(self):
        return  list_of_conversations

    def delete_one_conversation(self, unique_id: int):

    def delete_all_conversations(self):