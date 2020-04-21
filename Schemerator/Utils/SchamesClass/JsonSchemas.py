import json
import os
import pathlib
from collections import defaultdict

from Utils.HelpLibs.binary_object_helper import load_all_binary_objects
from Utils.HelpLibs.GensonPlusPlus.builder import SchemaBuilder as SchemaBuilderPlusPlus
from Utils.loggers.main_logger import main_logger

from Utils.ConfigClass import GlobalConfig


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

    @staticmethod
    def _list_dirs_in_dir(dir_path: str):
        """
        This is help function
        he return the list of all directories in directory.

        :return: list of directories path.
        """
        return [x for x in os.listdir(dir_path) if os.path.isdir(os.path.join(dir_path, x))]

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

    @staticmethod
    def _write_schema(path, json_schema):
        pathlib.Path(path).mkdir(parents=True, exist_ok=True)

        with open(os.path.join(path, JsonSchemas.SCHEMA_JSON_FILES_NAME), "w") as f:
            json.dump(obj=json_schema, fp=f, indent=4)

    def write_schemas(self, folder_path: str):
        self._write_schemas_basic_format(folder_path)

        log_format_string = 'Basic'

        main_logger.info('\nWrite Json schemas tree in path: "{}". in "{}" format.'.format(
                GlobalConfig.global_config.vars.OUTPUT_FOLDER_PATH, log_format_string))

    def _write_schemas_basic_format(self, folder_path: str):
        """
        This method write the json schemas into dirs.

        :param folder_path: the path of folder to write schemas into it.
                            must be real path and not relative path.
        """
        pathlib.Path(folder_path).mkdir(parents=True, exist_ok=True)

        for url_regex in self.schemas.keys():
            for method in self.schemas[url_regex].keys():
                req_schema = self.schemas[url_regex][method]["req"].to_schema()
                req_schema["title"] = "Request schema."
                res_schema = self.schemas[url_regex][method]["res"].to_schema()
                res_schema["title"] = "Response schema."

                json_schema = {"anyOf": [req_schema, res_schema]}

                if url_regex.startswith("\\"):
                    url_regex = url_regex[1:]
                schema_final_path = os.path.join(folder_path, url_regex, method)

                self._write_schema(schema_final_path, json_schema)

    def update_by_conversations_folder(self, folder_conversation_path):
        main_logger.info('Started creating json schemas from conversation pickles folder : "{}"'.format(
                folder_conversation_path))
        # Convert from pathlib.Path object to regular string.
        folder_conversation_path = str(folder_conversation_path)

        # Run all over files of conversations.
        # and get the list of HTTPConversations object from each file.
        # and append schemas by him.
        for (dir_path, dir_names, file_names) in os.walk(folder_conversation_path):
            dir_path_without_folder_conversation_path = dir_path[len(folder_conversation_path):]
            for method_file_name in file_names:
                curr_http_conversations = load_all_binary_objects(os.path.join(dir_path, method_file_name))
                self.update_schemas_by_list_http_conversation(url=dir_path_without_folder_conversation_path,
                                                              method=method_file_name,
                                                              list_of_conversation=curr_http_conversations)

    def generate_from_db(self, db_path):
        pass

    def __eq__(self, other):
        return vars(self) == vars(other)

    def __ne__(self, other):
        return vars(self) != vars(other)
