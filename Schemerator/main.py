#!/usr/bin/python3

import argparse
import sys
import os

ROOT_DIR = os.path.abspath("../../" + os.curdir)
sys.path.append(os.path.abspath(ROOT_DIR))

import datetime
import shutil
import tempfile
from pathlib import Path

from Utils.loggers.main_logger import main_logger
from Utils.HelpLibs.pcap_parser import convert_connections_folder_to_binary_folder
from Utils.HelpLibs.pcap_splitter import split_pcap

from Utils.SchamesClass.HttpConfig import HttpConfig
from Utils.SchamesClass.JsonSchemas import JsonSchemas

from Utils.ConfigClass import GlobalConfig

# Globals
# Every time when program run he save all temp files in unique temp folder.
TEMP_FILES_FOLDER = Path("D:\\tmp") / datetime.datetime.now().strftime("%m-%d-%y_%H-%M-%S")
FOLDER_OF_CONNECTIONS_PCAPS = Path(TEMP_FILES_FOLDER) / "connection_pcaps"
CONVERSATIONS_PICKLES_FOLDER = Path(TEMP_FILES_FOLDER) / "conversation_pickles"


def log_running_time(start_running):
    main_logger.info("Program run {} until now.".format(datetime.datetime.now() - start_running))


def print_logo():
    schemerator_logo =\
        """ _____      _                                   _
/  ___|    | |                                 | |
\\ `--.  ___| |__   ___ _ __ ___   ___ _ __ __ _| |_ ___  _ __
 `--. \\/ __| '_ \\ / _ \\ '_ ` _ \\ / _ \\ '__/ _` | __/ _ \\| '__|
/\\__/ / (__| | | |  __/ | | | | |  __/ | | (_| | || (_) | |
\\____/ \\___|_| |_|\\___|_| |_| |_|\\___|_|  \\__,_|\\__\\___/|_|  """

    print(schemerator_logo)


def parse_argument():
    parser = argparse.ArgumentParser(description="Schemarator: Create schemas.")
    parser.add_argument("-i",
                        "--input-config",
                        help="Configuration file path.",
                        type=str,
                        default="config.yaml")
    parser.add_argument("-v", "--version", action="version", version="%(prog)s 0.7.1")

    return parser.parse_args()


def main():
    print_logo()
    args = parse_argument()

    # Initialize the Global config object.
    GlobalConfig.global_config = GlobalConfig.GlobalConfig(args.input_config)

    if not GlobalConfig.global_config.vars.GENERATE_HTTP_CONFIG and not GlobalConfig.global_config.vars.GENERATE_JSON_SCHEMAS:
        main_logger.error("Invalid configuration provided, must generate HTTP Config or JSON Schemas.")
        sys.exit()

    TEMP_FILES_FOLDER.mkdir(parents=True, exist_ok=True)

    main_logger.info("\n\n#####\n"
                     "Using Pcap file: {}".format(Path(GlobalConfig.global_config.vars.INPUT_PCAP_PATH).resolve()))
    try:
        split_pcap(GlobalConfig.global_config.vars.INPUT_PCAP_PATH, FOLDER_OF_CONNECTIONS_PCAPS)
    except FileNotFoundError:
        main_logger.error("Input Pcap file not found in path {}".format(GlobalConfig.global_config.vars.INPUT_PCAP_PATH))
        sys.exit()

    convert_connections_folder_to_binary_folder(folder_to_work_with=TEMP_FILES_FOLDER)

    try:
        if GlobalConfig.global_config.vars.GENERATE_HTTP_CONFIG:
            http_config = HttpConfig()
            if GlobalConfig.global_config.vars.PRE_SCHEMAS_FOLDER:
                config_file_path = Path(GlobalConfig.global_config.vars.PRE_SCHEMAS_FOLDER) / HttpConfig.CONFIG_FILE_NAME
                if config_file_path.is_file():
                    http_config.load_from_pre_config(config_file_path)
                else:
                    main_logger.error("Can't find HTTP Config file in folder {}".format(
                            GlobalConfig.global_config.vars.PRE_SCHEMAS_FOLDER))

            http_config.update_by_folder_of_conversations(CONVERSATIONS_PICKLES_FOLDER)

            if GlobalConfig.global_config.vars.EXPAND_SIZES_IN_HTTP_CONFIG:
                http_config.expand_integer_sizes()

            http_config.write_config(GlobalConfig.global_config.vars.OUTPUT_FOLDER_PATH)

        if GlobalConfig.global_config.vars.GENERATE_JSON_SCHEMAS:
            json_schemas = JsonSchemas()
            if GlobalConfig.global_config.vars.PRE_SCHEMAS_FOLDER:
                json_schemas.load_from_folder(GlobalConfig.global_config.vars.PRE_SCHEMAS_FOLDER)

            json_schemas.update_by_conversations_folder(folder_conversation_path=
                                                        CONVERSATIONS_PICKLES_FOLDER)
            json_schemas.write_schemas(folder_path=GlobalConfig.global_config.vars.OUTPUT_FOLDER_PATH)

        main_logger.info("SUCCESS!")
    except Exception as e:
        main_logger.exception(e)
        raise e
    finally:
        shutil.rmtree(str(TEMP_FILES_FOLDER))


if __name__ == "__main__":
    start_time = datetime.datetime.now()
    main()
    log_running_time(start_running=start_time)
