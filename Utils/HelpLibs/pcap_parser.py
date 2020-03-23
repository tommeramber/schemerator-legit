import json
import logging
import re
import subprocess
import multiprocessing
import os

from functools import partial
from pathlib import Path

from Utils.HelpLibs.binary_object_helper import save_object_in_binary

from Utils.HttpClasss.HttpBody import HttpBody
from Utils.HttpClasss.HttpConversation import HttpConversation
from Utils.HttpClasss.HttpHeaderField import HttpHeaderField
from Utils.HttpClasss.HttpHeaders import HttpHeaders
from Utils.HttpClasss.Packet import Packet
from Utils.HelpLibs.regex_founder import get_regex_of_url

##################################################################
# Log config.
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s:%(name)s:%(message)s")

Path("logs").mkdir(exist_ok=True)

log_file_handler = logging.FileHandler("logs/pcap-parser.log", mode="a")
log_file_handler.setFormatter(formatter)

logger.addHandler(log_file_handler)
##################################################################

# Globals

# line that hold http version and status might look like:
# GET /v2/url/abc/ HTTP/1.1         ( Request )
# HTTP/1.1 200 OK                   ( Response )
REGEX_GET_VERSION = re.compile(".*HTTP/(\d).(\d)")
REGEX_GET_STATUS = re.compile(".*HTTP/\d.\d (.*)")

HTTP_METHODS = ("GET", "HEAD", "POST", "PUT", "DELETE", "CONNECT", "OPTIONS", "TRACE", "PATCH")

# The first item in pkt_tshark_format is the first line in header,
# and in is first item he contain the string itself of the first line.
# might look like:
# 'GET /v2/servers/detail HTTP/1.1\\r\\n'
INDEX_FIRST_LINE_IN_HEADER = 0
INDEX_STRING_OF_FIRST_LINE = 0


def parse_object_pairs(pairs):
    """
    This help function get list of tuple's and check if have duplicate keys in list.
    if have then he just return the list, but if doesnt have then he return dict that represent the list.

    >>> parse_object_pairs([('first', 1), ('second', 2)])
    {"first":1, "second":2}

    >>> parse_object_pairs([('first', 1), ('second', 2), ('first', 5)])
    [('first', 1), ('second', 2), ('first', 5)]

    :param pairs: list tuples.
    :return: dict or list that contain the pairs.
    """
    dict_without_duplicate = dict()
    for key, value in pairs:
        if key in dict_without_duplicate:
            return pairs
        else:
            dict_without_duplicate[key] = value
    return dict_without_duplicate

# Because tshark output is JSON that can hold duplicate keys,
# and when json.loads() try convert this strings to json object he cut all duplicate keys.
# so we create custom decoder.
tshark_compatible_decoder = json.JSONDecoder(object_pairs_hook=parse_object_pairs)


def _pkt_is_req(pkt_in_tshark_format_http_layer):
    return pkt_in_tshark_format_http_layer[INDEX_FIRST_LINE_IN_HEADER][INDEX_STRING_OF_FIRST_LINE].\
        startswith(HTTP_METHODS)


def parse_one_connection(connection_pcap_path):
    """
    This method parse one connection pcap
    he run all over the packets that pcap hold,
    and convert him to HttpConversation objects.
    and return list of HttpConversation objects.

    :param connection_pcap_path: path to connection pcap file.
    :return: list of HttpConversation.
    """
    parse_pcap_process = \
        subprocess.run(["tshark", "-r", str(connection_pcap_path),
                        "-Y", "http",
                        "-T", "json",
                        "-j", "http"],
                       stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE)

    pcap_in_json = tshark_compatible_decoder.decode(parse_pcap_process.stdout.decode("utf-8"))

    # Create list of HTTP_CONVERSATION objects, from pcap.
    # Sometimes packets are not in req res order... so handle this.
    list_http_conversation = list()
    curr_http_conversation = None
    for pkt_tshark_format in pcap_in_json:
        pkt_http_tshark_format = pkt_tshark_format["_source"]["layers"]["http"]

        # Have edge case, which should not exist in normal use, the edge case is when have only one header,
        # and parse_object_pairs() return dict and not list.
        # but when we use this we use it like list (because in normal use will be more then one header)
        # so for this edge case we convert pkt_tshark_format to list.
        # we also sorted him because he wes sorted before he return from parse_object_pairs()
        # (and _pkt_is_req() check in the first cell after the methods)
        # also we change all values to be stored in tuple and not "key val" because this is also how they stored before.
        if isinstance(pkt_http_tshark_format, dict):
            pkt_http_tshark_format_with_one_header = list()
            for key in sorted(pkt_http_tshark_format.keys()):
                pkt_http_tshark_format_with_one_header.append((key, pkt_http_tshark_format[key]))
            pkt_http_tshark_format = pkt_http_tshark_format_with_one_header

        if _pkt_is_req(pkt_http_tshark_format):
            pkt = parse_pkt(pkt_http_tshark_format)

            # First line in header might look like:
            # GET /v2/url/abc/ HTTP/1.1
            # or
            # HTTP/1.1 200 OK
            first_line_in_header = pkt_http_tshark_format[INDEX_FIRST_LINE_IN_HEADER][INDEX_STRING_OF_FIRST_LINE]

            method, url = first_line_in_header.split(" ")[0:2]

            curr_http_conversation = HttpConversation(url=url, method=method, pkt_req=pkt)
        elif curr_http_conversation:
                curr_http_conversation.pkt_res = parse_pkt(pkt_http_tshark_format)
                list_http_conversation.append(curr_http_conversation)
                curr_http_conversation = None

    return list_http_conversation


def parse_pkt(pkt):
    """
    This function take list that represent packet and convert him to Packet object.
    The list is came from tshark so the format is just what that they export...
    The list might look like:

    [('HTTP/1.1 200 OK\\r\\n',
     [('filtered', 'HTTP/1.1 200 OK\\r\\n')]),
      ('http.content_length_header', '1898'),
       ('http.content_length_header_tree',
        [('filtered', 'http.content_length_header')]),
         ('http.response.line', 'Content-Length: 1898\r\n'),
          ('http.content_type', 'application/json'),
           ('http.response.line', 'Vary: X-OpenStack-Nova-API-Version\r\n'),
            ('http.response.line', 'X-Compute-Request-Id: req-8dcef1f4-c7da-4c84-b54e-c32fda17270a\r\n'),
             ('http.date', 'Sun, 05 Aug 2018 18:12:49 GMT'), ('http.response.line', 'Date: Sun, 05 Aug 2018 18:12:49 GMT\r\n'),
              ('http.connection', 'close'), ('http.response.line', 'Connection: close\r\n'), ('\\r\\n', ''), ('http.response', '1'),
               ('http.response_number', '1'),
                ('http.time', '0.311472000'),
                 ('http.request_in', '1'),
                  ('http.file_data', '{"some_json_object..}')] # HERE IS THE HTTP BODY!!!

    :param pkt: list of tuples that represent an HTTP packet.
    :return: Packet object.
    """
    list_headers_field = []
    curr_http_body = None
    for header in pkt:
        # In request they call the keys of headers "http.request.line" and in response "http.response.line"
        if header[0] in ["http.request.line", "http.response.line"]:
            header_name, header_value = header[1].split(": ", 1)

            # header_value = header_value[:-2] if header_value[-2:] == "\r\n" else header_value
            header_value = header_value.split("\r\n")[0]  # Drop trailing \r\n if they exist.

            list_headers_field.append(HttpHeaderField(name=header_name, value=header_value))
        elif header[0] == "http.file_data":  # "http.file_data" contain HTTP body (if have).
            try:
                http_body_val = json.loads(header[1])
                curr_http_body = HttpBody(type_body="json", value=http_body_val)
            # When have HTTP body that is not json object.
            # Todo: In future check if this is XML.
            except Exception:
                """ When have status Internal server Error (code 500)
                "http.file_data" doesnt contain Json, but he contain "Line based text data: text/plain"
                that will be something like:
                '500 Internal Server Error
                The server has either erred or is incapable of performing the requested operation.'

                so in this case for now we just not handle this and save None in Body

                And also where have a binary string (for example send some binary file ) we are save None in http body.
                """
                logger.error("An error occur while try parse http body, this was the body : {}".format(header[1]))

    # string_first_line Might look like:
    # 'GET /v2.1/asd/?name=yehuda HTTP/1.1\\r\\n'
    string_first_line = pkt[INDEX_FIRST_LINE_IN_HEADER][INDEX_STRING_OF_FIRST_LINE]

    # In pre example it will be
    # ("1","1")
    tuple_version_in_string = REGEX_GET_VERSION.search(string_first_line).groups()

    mjr_version = HttpHeaderField(name="mjr_version", header_type="numeric", value=int(tuple_version_in_string[0]))

    min_version = HttpHeaderField(name="min_version", header_type="numeric", value=int(tuple_version_in_string[1]))

    status = REGEX_GET_STATUS.search(string_first_line)

    # if have status (Is response packet, so status not None) then get the real status value.
    # status value save with "\\r\\n" so we cut this. (Its 4 bytes not 2)
    status = status.groups()[0][:-4] if status else None

    status = HttpHeaderField(name="status", header_type="string", value=status)

    return Packet(HttpHeaders(mjr_version=mjr_version,
                              min_version=min_version,
                              list_http_header_fields=list_headers_field,
                              status=status),
                  http_body=curr_http_body)


def save_conversation_in_binary_format(list_conversations, folder_to_save_objects):
    """
    This function get list of HttpConversation objects and save him in binary format.
    he save him in folder_to_save_objects.
    folder_to_save_objects will hold the objects in files that look like
    method_regex-url

    :param list_conversations:
    :param folder_to_save_objects:
    """
    for conversation in list_conversations:
        regex_url = get_regex_of_url(conversation.url)

        folder_path = Path(folder_to_save_objects) / regex_url

        folder_path.mkdir(parents=True, exist_ok=True)

        file_path = folder_path / conversation.method

        save_object_in_binary(obj=conversation, file_path=file_path)


def parse_and_save_connection(lock, folder_to_save_objects, file_path):
    try:
        # todo :use multiprocessing logger.
        # logger.info("Start parse connection pcap {}".format(file_path))
        curr_list_conversation = parse_one_connection(folder_to_save_objects / "connection_pcaps" / file_path)

        if curr_list_conversation:
            lock.acquire()
            save_conversation_in_binary_format(curr_list_conversation, folder_to_save_objects / "conversation_pickles")
            lock.release()

    except Exception as e:
        # todo :use multiprocessing logger.
        print(e)

    # Path(folder_to_save_objects / file_path).unlink()


def convert_connections_folder_to_binary_folder(folder_to_work_with):
    """
    This function take folder of connections pcap files and convert him to folder that hold pickle files
    that contains the HTTPConversations that represent them.
    do this by using the function parse_connection on all files (one by one to save RAM).

    :param connections_folder: folder that contain connections pcap file. (usually from the function split_pcap)
    :param folder_to_save_objects: folder to save in him pickle files that contains list of HttpConversation object.
    """
    logger.info("Start converting connections")
    connection_folder = folder_to_work_with / "connection_pcaps"

    manager = multiprocessing.Manager()
    lock = manager.Lock()
    func = partial(parse_and_save_connection, lock, folder_to_work_with)
    pool = multiprocessing.Pool()

    pool.map(func=func, iterable=os.listdir(str(connection_folder)))
    pool.close()
    pool.join()

    # Path(folder_to_work_with / "connections_pcaps").rmdir()

    logger.info('Finished converting connections')
