from .IConfigParser import IConfigParser

from .GlobalConfigurationVars import GlobalConfigurationVars

from Utils.loggers.main_logger import main_logger

import yaml
import re


class YamlConfigParser(IConfigParser):
    @staticmethod
    def read_config_file(path):
        global_configuration_vars = GlobalConfigurationVars()
        with open(path, 'r') as yaml_file:
            try:
                config_data = yaml.safe_load(yaml_file)
                global_configuration_vars.INPUT_PCAP_PATH = config_data["input_pcap_path"]
                global_configuration_vars.OUTPUT_FOLDER_PATH = config_data["output_folder_path"]
                global_configuration_vars.PRE_SCHEMAS_FOLDER = config_data["pre_schemas_folder"]
                global_configuration_vars.GENERATE_JSON_SCHEMAS = config_data["generate_json_schemas"]
                global_configuration_vars.GENERATE_HTTP_CONFIG = config_data["generate_http_config"]
                global_configuration_vars.EXPAND_SIZES_IN_HTTP_CONFIG = config_data["expand_sizes_in_http_config"]
                global_configuration_vars.WORK_ONLY_WITH_HEADERS_IN_RFC = config_data["work_only_with_headers_in_rfc"]
                global_configuration_vars.ADD_REQUIRED_IN_JSON_SCHEMA = config_data["add_required_in_json_schema"]

                # Configuration for create regex for headers.
                global_configuration_vars.ADD_LENGTH_TO_REGEX_IN_HEADERS = \
                    config_data["add_length_to_regex_in_headers"]
                global_configuration_vars.ADD_GROUPS_LETTERS_TO_REGEXS_IN_HEADERS =\
                    config_data["add_groups_letters_to_regexs_in_headers"]
                global_configuration_vars.ADD_ENUMS_IN_HEADERS =\
                    config_data["add_enums_in_headers"]

                global_configuration_vars.OPTIONAL_URL_REGEXS = \
                    [re.compile(s) for s in config_data["optional_url_regexs"]] if config_data["optional_url_regexs"] else None

                global_configuration_vars.OPTIONAL_HEADER_REGEXS = \
                    [re.compile(s) for s in config_data["optional_header_regexs"]] if config_data["optional_header_regexs"] else None

                global_configuration_vars.OPTIONAL_JSON_SCHEMA_REGEXS = \
                    [re.compile(s) for s in config_data["optional_json_schema_regexs"]] if config_data["optional_json_schema_regexs"] else None

            except yaml.YAMLError as exc:
                main_logger.exception(exc)

        return global_configuration_vars
