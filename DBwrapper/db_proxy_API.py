"""
specific use of the Wrapper module for the DB to Proxy interface

Author: Shaya Weissberg
"""


from .Wrapper import Wrapper
import string


class DBproxy:

    def __init__(self, config_file=None):
        self.db = Wrapper(None, config_file)

    #####################################
    # conversation handling
    #####################################

    # save one raw conversation
    def save_one_conversation(self, url: string, method: string,  reqheaders: string,
                              req: string, resheaders: string, res: string):

    def save_all_conversations(self, list_of_conversations):

    def get_all_conversations(self):
        return  list_of_conversations

    def delete_one_conversation(self, unique_id: int):

    def delete_all_conversations(self):



