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
REGEX_GET_STATUS = re.compile(".*HTTP/\d.\d (.*)")

URL_INDEX = 1
METHOD_INDEX = 2
REQ_HEADER_INDEX = 3
REQ_BODY_INDEX = 4 
RES_HEADER_INDEX = 5
RES_BODY_INDEX = 6


def parse_header(header: str) -> HttpHeaders:
    header_fields = []
    header_pairs = list(filter(None, header.split('\r\n')))

    first_line = header_pairs[0]

    for pair in header_pairs[1:]:
        pair_list = pair.split(': ', 1)
        header_fields.append(HttpHeaderField(name=pair_list[0], value=pair_list[1]))

    tuple_version_in_string = REGEX_GET_VERSION.search(first_line).groups()

    mjr_version = HttpHeaderField(name="mjr_version", header_type="numeric", value=int(tuple_version_in_string[0]))

    min_version = HttpHeaderField(name="min_version", header_type="numeric", value=int(tuple_version_in_string[1]))

    status = REGEX_GET_STATUS.search(first_line)
    status = status.groups()[0] if status else None

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
        fixed_api = regex_founder.get_regex_of_url(conversation[URL_INDEX].split('://')[1])
        req = Packet()
        req.http_headers = parse_header(conversation[REQ_HEADER_INDEX])
        req.http_body = HttpBody('JSON', conversation[REQ_BODY_INDEX])
        res = Packet()
        res.http_headers = parse_header(conversation[RES_HEADER_INDEX])
        res.http_body = HttpBody('JSON', conversation[RES_BODY_INDEX])
        cur_conversation = HttpConversation(req, res, fixed_api, conversation[METHOD_INDEX])
        cur.execute("INSERT INTO ParsedConversations (api, method, conversation) VALUES (?, ?, ?)", (fixed_api, conversation[METHOD_INDEX], pickle.dumps(cur_conversation, 0)))
        #parse headers

    cur.close()
    conn.commit()
    conn.close()


if __name__ == "__main__":
    main()
