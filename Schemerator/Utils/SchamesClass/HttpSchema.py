import os
import re

from SharedUtils.HttpClass.HttpHeaders import HttpHeaders

from .HttpConfigHeaderField import HttpConfigHeaderField
from .MinMax import MinMax
from .StringConfig import StringConfig

from Utils.ConfigClass import GlobalConfig

from Utils.loggers.main_logger import main_logger

from .HTTP_HEADER_LIST_FROM_RFC import HTTP_HEADER_LIST_FROM_RFC

from SharedUtils.DBUtils.db_api_parsed_conv import ParsedConversationsAPI
from SharedUtils.DBUtils.db_api_schemas import SchemasAPI

class HttpSchema:
    _COMMENT_SIGN = "#"
    _REGEX_LINE_COMMENT_ON_ENUMS = "# occurrences (\d*)"
    SPECIAL_HEADERS = ["status", "mjr_version", "min_version"]
    CONFIG_FILE_NAME = "config"

    def __init__(self,
                 dict_http_config_header=None,
                 mjr_version: HttpConfigHeaderField=None,
                 min_version: HttpConfigHeaderField=None,
                 status: HttpConfigHeaderField=None):

        self.dict_http_config_header = dict_http_config_header or dict()

        # Mjr_version and Min_version are special headers,
        # they save in the first line in HTTP Header.
        # something like that:
        # POST /Query HTTP/1.1\r\n
        # and also status exist only in response.
        self.mjr_version = mjr_version or HttpConfigHeaderField(name="Mjr_version",
                                                                value=MinMax(minimum=1, maximum=1))

        self.min_version = min_version or HttpConfigHeaderField(name="Min_version",
                                                                value=MinMax(minimum=1, maximum=1))
        # Save 20 in minimum value, because this will change to be the minimum len of all status after that.
        self.status = status or HttpConfigHeaderField(
                name="Status",
                value=StringConfig(string="",
                                   min_max=MinMax(minimum=20, maximum=0),
                                   list_optional_regexs=GlobalConfig.global_config.vars.OPTIONAL_HEADER_REGEXS))

    def to_string(self):
        config_string = "# This HTTP Config file was created by Schemerator.\n"

        for header_key, header_val in self.dict_http_config_header.items():
            config_string += header_val.to_string()
        config_string += self.mjr_version.to_string()
        config_string += self.min_version.to_string()
        config_string += self.status.to_string()

        return config_string

    def write_schema(self, db_path: str):
        """
            Saving the http schema to the given path using the Schema API.
            the HTTP schema is save as the API HTTP_CONFIG and the method CONFIG to seperate it from the JSON schemas.

            :param db_path: Path to the db location
        """
        schema_file = SchemasAPI(db_path)
        schema_file.save_schema('HTTP_CONFIG', 'CONFIG', self.to_string())

    def append_by_http_headers(self, http_headers: HttpHeaders):
            self.mjr_version.append_val(http_headers.mjr_version.value)
            self.min_version.append_val(http_headers.min_version.value)

            # Update status, Only in response have status.
            if http_headers.status.value:
                self.status.append_val(http_headers.status.value)

            for header_field in http_headers.list_http_header_fields:
                header_field.name = header_field.name.lower()
                if GlobalConfig.global_config.vars.WORK_ONLY_WITH_HEADERS_IN_RFC and\
                                header_field.name not in HTTP_HEADER_LIST_FROM_RFC:
                        main_logger.error("Was header {} "
                                          "and he is not part of headers in RFC."
                                          "and you try work only with headers in RFC".format(header_field))
                else:
                    if header_field.name not in self.dict_http_config_header:
                        if header_field.header_type == "numeric":
                            header_field.value = MinMax(minimum=header_field.value, maximum=header_field.value)
                        # else if header_field.header_type == "regex"
                        else:
                            header_field.value = StringConfig(string=header_field.value,
                                                              list_optional_regexs=GlobalConfig.global_config.vars.OPTIONAL_HEADER_REGEXS)

                        self.dict_http_config_header[header_field.name] = HttpConfigHeaderField(name=header_field.name,
                                                                                                value=header_field.value)
                    else:
                        self.dict_http_config_header[header_field.name].append_val(header_field.value)

    def load_from_pre_config(self, config_path):
        """
        not used!!!!!!
        config file might look like:

        Host regex "[a-zA-Z.0-9:]{0,255}"
        Content-Length numeric "255" "65535"
        _occurrences 55509
        Content-Type enum "application/json; charset=UTF-8" "application/json"

        :param config_path: path to config file.
        """
        main_logger.info("Start load pre HTTP Config from file : {}".format(config_path))
        curr_header_config = None

        with open(str(config_path), 'r') as f:
            line = f.readline()
            while line:
                if line.startswith("\n"):
                    line = f.readline()
                    continue
                if line.startswith(self._COMMENT_SIGN):
                    # if line contain _occurrences of the enum in next line.
                    occurrences = re.findall(pattern=self._REGEX_LINE_COMMENT_ON_ENUMS, string=line)
                    # if have comment that describe _occurrences of the values in next enum:
                    if occurrences:
                        # enum line might look like:
                        # Connection enum "Keep-Alive" "close"
                        # openstack-api-version enum "volume 3.0" "compute 2.1"
                        enum_line = f.readline()
                        # "[^\"]*" in regex mean any character except character \"
                        enum_options = re.findall('\"([^\"]*)\"', enum_line)
                        # In pre examples its will, enum_option will look like:
                        # ["Keep-Alive", "close"]
                        # ["volume 3.0", "compute 2.1"]
                        curr_header_config = StringConfig(enum=enum_options,
                                                          # because re.findall() return list of strings.
                                                          occurrences=int(occurrences[0]))

                        header_name = enum_line.split(" ", 1)[0]
                # if line is not comment.
                else:
                    header_name, config_type, config_value = line.split(" ", 2)
                    if config_type == "numeric":
                        minimum, maximum = re.findall('"(\d*)"', config_value)
                        curr_header_config = MinMax(minimum=int(minimum), maximum=int(maximum))
                    elif config_type == "regex":
                        # config value look like:
                        # '"[a-z]{0-9}$"\n'
                        # and we want change it to be
                        # '[a-z]{0-9}$'
                        regex_in_config_value = config_value[1:-2]
                        curr_header_config = StringConfig(regex=regex_in_config_value)
                    elif config_type == "enum":
                        # "[^\"]*" in regex mean any character except character \"
                        enum_options = re.findall('\"([^\"]*)\"', enum_line)
                        curr_header_config = StringConfig(enum=enum_options)
                    else:
                        main_logger.error("An error occur while try update by pre config\n"
                                          "This line made the error {}".format(line))
                        line = f.readline()
                        continue

                if curr_header_config:
                    self._help_insert_header_config_into_correct_var(header_name=header_name, header_config=curr_header_config)
                    curr_header_config = None

                line = f.readline()

    def generate_from_db(self, db_path: str):
        """ 
        This method appends http_headers to this object and creates the HTTP Schema by it/
        First we load all the conversation objects from the DB API.Saving happends in a different function.
        The function dosnt return anything just updates self.
        :param db_path: the path for the file of the db where data is stored (sqlite3 db file)
        :raise: exception if there is an error in the db
        """
        data_handler = ParsedConversationsAPI(db_path)
        for http_conversation in data_handler.get_all_conversations():
            self.append_by_http_headers(http_conversation.pkt_req.http_headers)
            self.append_by_http_headers(http_conversation.pkt_res.http_headers)

    def expand_integer_sizes(self):
        """
        This method expand the minimum and maximum of all headers without mjr/min version and status.
        he call to the func expand_integer_sizes() in StringConfig and MinMax object.
        """
        main_logger.info("Expanding the sizes of min/max in HTTP Config file to be in integer sizes.")

        for header_key, header_val in self.dict_http_config_header.items():
            header_val.value.expand_integer_sizes()

    def _help_insert_header_config_into_correct_var(self, header_name: str, header_config):
        http_config_header_field = HttpConfigHeaderField(name=header_name, value=header_config)
        if header_name not in self.SPECIAL_HEADERS:
            self.dict_http_config_header[header_name] = http_config_header_field
        else:
            if header_name == "mjr_version":
                self.mjr_version = http_config_header_field
            elif header_name == "min_version":
                self.min_version = http_config_header_field
            else:
                self.status = http_config_header_field

    def __eq__(self, other):
        return vars(self) == vars(other)

    def __ne__(self, other):
        return vars(self) != vars(other)
