"""
sspecific use of the Wrapper module for the DB to Parser interface

Author: Shaya Weissberg
"""

from .Wrapper import Wrapper
import string

class DBparser:

    def __init__(self, config_file=None):
        self.db = Wrapper(None, config_file)

    #####################################
    # conversation handling
    #####################################

    #Save PARSED conversation
    def save_conversation_by_api(self, api: string, method: string, conversation):

    def get_one_raw_conversations(self, unique_id: int):
        return conversation

    def get_all_raw_conversations(self):
        return list_of_conversations

    def delete_one_raw_conversation(self, unique_id: int):

    def delete_url_raw_conversation(self, url: string):

    def delete_all_raw_conversations(self):

    #####################################
    # apis handling
    #####################################

    def get_list_apis(self):
        return list_of_apis

    def get_conversations_for_api(self, api: string):
        return list_of_conversations

    def delete_conversations_for_api(self, api: string):

