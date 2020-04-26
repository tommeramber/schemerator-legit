import json
import os
from collections import defaultdict

from Utils.HelpLibs.GensonPlusPlus.builder import SchemaBuilder as SchemaBuilderPlusPlus
from Utils.loggers.main_logger import main_logger

from Utils.ConfigClass import GlobalConfig

from SharedUtils.DBUtils.db_api_parsed_conv import ParsedConversationsAPI
from SharedUtils.DBUtils.db_api_schemas import SchemasAPI

class JsonSchemas:
    SIGN_OF_SIMPLE_SPLIT_PATH = "/"
    SCHEMA_JSON_FILES_NAME = "schema.json"

    # Schema build from two schemas, request and response that save in TYPE_OF_BIG_SCHEMA field.
    # for example:
    """
    {"anyOf": [
    "request schema...",
    "response schema..."
    ]
    """
    TYPE_OF_BIG_SCHEMA = "anyOf"
    REQ_SCHEMA_INDEX = 0
    RES_SCHEMA_INDEX = 1

    def __init__(self, schemas: defaultdict=defaultdict()):
        # Schemas is dict that keys is url+method and value is Genson++ builders.
        self.schemas = schemas

    def load_from_folder(self, folder_path):
        main_logger.info("Load schemas from folder {}".format(folder_path))

        if not os.path.isdir(folder_path):
            raise OSError("FOLDER NOT EXIST")

        for url_folder in self._list_dirs_in_dir(folder_path):
            for method_folder in self._list_dirs_in_dir(os.path.join(folder_path, url_folder)):
                with open(os.path.join(folder_path, url_folder, method_folder, self.SCHEMA_JSON_FILES_NAME)) as f:
                    main_logger.info("Load schema about url : {}, and method : {}".format(url_folder, method_folder))

                    self.schemas[url_folder] = dict()
                    self.schemas[url_folder][method_folder] = dict()
                    self.schemas[url_folder][method_folder]["req"] = SchemaBuilderPlusPlus()
                    self.schemas[url_folder][method_folder]["res"] = SchemaBuilderPlusPlus()

                    schemas_req_and_res = json.loads(f.read())

                    schemas_req, schema_res = schemas_req_and_res[JsonSchemas.TYPE_OF_BIG_SCHEMA]

                    self.schemas[url_folder][method_folder]["req"].add_schema(schemas_req)
                    self.schemas[url_folder][method_folder]["res"].add_schema(schema_res)

    def update_schemas_by_list_http_conversation(self, url: str, method, list_of_conversation):
        request_json_list = []
        response_json_list = []
        for conversation in list_of_conversation:
            # only when have http body (is not None) and have value in him, append the lists by him.
            if conversation.pkt_req.http_body and conversation.pkt_req.http_body.value:
                request_json_list.append(conversation.pkt_req.http_body.value)
            if conversation.pkt_res.http_body and conversation.pkt_res.http_body.value:
                response_json_list.append(conversation.pkt_res.http_body.value)

        # Check if have this entry (url + method) and if not then create him.
        try:
            self.schemas[url][method]
        except KeyError:
            self.schemas[url] = dict()
            self.schemas[url][method] = dict()
            self.schemas[url][method]["req"] = SchemaBuilderPlusPlus()
            self.schemas[url][method]["res"] = SchemaBuilderPlusPlus()

        for req in request_json_list:
            self.schemas[url][method]["req"].add_object(req)
        for res in response_json_list:
            self.schemas[url][method]["res"].add_object(res)


    def write_schemas(self, db_path: str):
        """
        This method write the json schemas into db.

        :param db_path: the path of db to write schemas into it.
        """
        data_handler = SchemasAPI(db_path)

        for url_regex in self.schemas.keys():
            for method in self.schemas[url_regex].keys():
                req_schema = self.schemas[url_regex][method]["req"].to_schema()
                req_schema["title"] = "Request schema."
                res_schema = self.schemas[url_regex][method]["res"].to_schema()
                res_schema["title"] = "Response schema."

                json_schema = {"anyOf": [req_schema, res_schema]}

                if url_regex.startswith("\\"):
                    url_regex = url_regex[1:]
                
                data_handler.save_schema(url_regex, method, json.dumps(obj=json_schema, indent=4))

    def generate_from_db(self, db_path: str):
        """
        load Parsed conversations from db in db_path and create json schemas acording to them.

        :param db_path: path for the Parsed conversation db
        """
        data_handler = ParsedConversationsAPI(db_path)
        for api in data_handler.get_list_apis():
            # TODO: add iteration of methods
            self.update_schemas_by_list_http_conversation(api, 'GET', data_handler.get_conversations_for_api(api, 'GET'))


    def __eq__(self, other):
        return vars(self) == vars(other)

    def __ne__(self, other):
        return vars(self) != vars(other)
