"""
API for parsed Conversations table, using the Wrapper module

Author: Shaya Weissberg
"""


from .wrapper import Wrapper
import string


class ParsedConversationsAPI:

    def __init__(self, name):
        self.db = Wrapper(name)

    def save_conversation_by_api(self, api: string, method: string, conversation):

    def get_list_apis(self):
        return list_of_apis

    def get_conversations_for_api(self, api: string):
        return list_of_conversations

    def delete_conversations_for_api(self, api: string):
