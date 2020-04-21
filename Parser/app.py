import sqlite3
import regex_founder
from SharedUtils.HttpClass.HttpConversation import HttpConversation
from SharedUtils.HttpClass.Packet import Packet
from SharedUtils.HttpClass.HttpBody import HttpBody
from SharedUtils.HttpClass.HttpHeaders import HttpHeaders

def main():
    conn = sqlite3.connect('db.db')
    cur = conn.cursor()
    list_conversations = list()
    cur.execute("select * from RawConversations")
    conversations =  cur.fetchall()

    for conversation in conversations:
        fixed_api = regex_founder.get_regex_of_url(convarsation[1])
        req = Packet()
        req.http_body = HttpBody('JSON', conversation[4])
        res = Packet()
        res.http_body = HttpBody('JSON', conversation[6])
        cur_conversation = HttpConversation(req, res, fixed_api, conversation[2])
        #parse headers


if __name__ == "__main__":
    main()
