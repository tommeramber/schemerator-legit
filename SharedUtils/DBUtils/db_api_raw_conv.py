"""
API for Raw Conversations table, using the Wrapper module

Author: Shaya Weissberg
"""
from .db_utils_api import DBUtilsAPI
from SharedUtils.raw_conversation import RawConversation


def db_tuple_to_raw_conversation(value):  # TODO: is it good way to do it?
    url, method, reqheaders, req, resheaders, res = value
    return RawConversation(url, method, reqheaders, req, resheaders, res)


class RawConversationsAPI(DBUtilsAPI):

    def __init__(self, DBname):
        DBUtilsAPI.__init__(self, DBname, 'RawConversations', "(url, method, reqheaders, req, resheaders, res)",
                            "id INTEGER PRIMARY KEY AUTOINCREMENT, url TEXT,"
                            " method TEXT, reqheaders TEXT, req TEXT,"
                            " resheaders TEXT, res TEXT")

        self.create_table()

    def save_one_conversation(self, conversation: RawConversation):
        self.save(tuple(conversation.__dict__.values()))

    def save_all_conversations(self, list_of_conversations):
        pass

    def get_all_conversations(self) -> list:
        # return list of conversations
        return list(map(db_tuple_to_raw_conversation, self.get_all_table()))

    def delete_one_conversation(self, unique_id: int):
        pass

    def delete_all_conversations(self):
        pass
