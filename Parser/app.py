import sqlite3
import regex_founder
import pickle
from SharedUtils.HttpClass.HttpConversation import HttpConversation
from SharedUtils.HttpClass.Packet import Packet
from SharedUtils.HttpClass.HttpBody import HttpBody
from SharedUtils.HttpClass.HttpHeaders import HttpHeaders

def main():
    conn = sqlite3.connect('db.db')
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS ParsedConversations (id INTEGER PRIMARY KEY AUTOINCREMENT, api TEXT, method TEXT, conversation BLOB)")
    cur.execute("select * from RawConversations")
    conversations =  cur.fetchall()

    for conversation in conversations:
        fixed_api = regex_founder.get_regex_of_url(conversation[1].split('://')[1])
        req = Packet()
        req.http_body = HttpBody('JSON', conversation[4])
        res = Packet()
        res.http_body = HttpBody('JSON', conversation[6])
        cur_conversation = HttpConversation(req, res, fixed_api, conversation[2])
        cur.execute("INSERT INTO ParsedConversations (api, method, conversation) VALUES (?, ?, ?)", (fixed_api, conversation[2], pickle.dumps(cur_conversation, 0)))
        #parse headers

    cur.close()
    conn.commit()
    conn.close()


if __name__ == "__main__":
    main()
