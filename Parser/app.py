import regex_founder
import re
import json

from SharedUtils.HttpClass.HttpConversation import HttpConversation
from SharedUtils.HttpClass.Packet import Packet
from SharedUtils.HttpClass.HttpBody import HttpBody
from SharedUtils.HttpClass.HttpHeaders import HttpHeaders
from SharedUtils.HttpClass.HttpHeaderField import HttpHeaderField
from SharedUtils.DBUtils.db_api_raw_conv import RawConversationsAPI
from SharedUtils.DBUtils.db_api_parsed_conv import ParsedConversationsAPI
from SharedUtils.raw_conversation import RawConversation

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
    raw_conv_db = RawConversationsAPI('/home/db/db.db')
    parsed_conv_db = ParsedConversationsAPI('/home/db/db.db')
    conversations =  raw_conv_db.get_all_conversations()

    for conversation in conversations:
        fixed_api = regex_founder.get_regex_of_url(conversation.url.split('://')[1])
        req = Packet()
        req.http_headers = parse_header(conversation.reqheaders)
        try:
            # for now i do this workaround for empty string but it can also be not json
            val = json.loads(conversation.req)
        except Exception as e:
            print('got json error {} from string {}'.format(e, conversation.req))
            val = ''

        req.http_body = HttpBody(type_body='json', value=val)
        res = Packet()
        res.http_headers = parse_header(conversation.resheaders)
        try:
            # for now i do this workaround for empty string but it can also be not json
            val = json.loads(conversation.res)
        except Exception as e:
            print('got json error {} from string {}'.format(e, conversation.res))
            val = ''
            
        res.http_body = HttpBody(type_body='json', value=val)
        cur_conversation = HttpConversation(req, res, fixed_api, conversation.method)
        parsed_conv_db.save_conversation_by_api(fixed_api, conversation.method, cur_conversation)
       
        #parse headersrm

if __name__ == "__main__":
    main()
