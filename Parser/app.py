import sqlite3
import regex_founder
import pickle
import re

from SharedUtils.HttpClass.HttpConversation import HttpConversation
from SharedUtils.HttpClass.Packet import Packet
from SharedUtils.HttpClass.HttpBody import HttpBody
from SharedUtils.HttpClass.HttpHeaders import HttpHeaders
from SharedUtils.HttpClass.HttpHeaderField import HttpHeaderField

REGEX_GET_VERSION = re.compile(".*HTTP/(\d).(\d)")

def parse_header(header: bytes, version: str, status: str) -> HttpHeaders:
    header_fields = []
    header_pairs = str(header, 'utf-8').split('\r\n')[:-1]

    for pair in header_pairs:
        pair_list = pair.split(':')
        header_fields.append(HttpHeaderField(name=pair_list[0], value=pair_list[1]))

    tuple_version_in_string = REGEX_GET_VERSION.search(version).groups()

    mjr_version = HttpHeaderField(name="mjr_version", header_type="numeric", value=int(tuple_version_in_string[0]))

    min_version = HttpHeaderField(name="min_version", header_type="numeric", value=int(tuple_version_in_string[1]))

    status_field = HttpHeaderField(name="status", header_type="string", value=status)

    return HttpHeaders(mjr_version=mjr_version,
                       min_version=min_version,
                       status=status_field,
                       list_http_header_fields=header_fields)

def main():
    conn = sqlite3.connect('db.db')
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS ParsedConversations (id INTEGER PRIMARY KEY AUTOINCREMENT, api TEXT, method TEXT, conversation BLOB)")
    cur.execute("select * from RawConversations")
    conversations =  cur.fetchall()

    for conversation in conversations:
        fixed_api = regex_founder.get_regex_of_url(conversation[1].split('://')[1])
        req = Packet()
        req.http_headers = parse_header(conversation[3], conversation[7], None)
        req.http_body = HttpBody('JSON', conversation[4])
        res = Packet()
        res.http_headers = parse_header(conversation[5], conversation[7], conversation[8])
        res.http_body = HttpBody('JSON', conversation[6])
        cur_conversation = HttpConversation(req, res, fixed_api, conversation[2])
        cur.execute("INSERT INTO ParsedConversations (api, method, conversation) VALUES (?, ?, ?)", (fixed_api, conversation[2], pickle.dumps(cur_conversation, 0)))
        #parse headers

    cur.close()
    conn.commit()
    conn.close()


if __name__ == "__main__":
    main()
