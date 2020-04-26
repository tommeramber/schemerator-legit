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

from Utils.SchamesClass.HttpSchema import HttpSchema
from Utils.SchamesClass.JsonSchemas import JsonSchemas

from Utils.ConfigClass import GlobalConfig

# Globals
# Every time when program run he save all temp files in unique temp folder.
#TEMP_FILES_FOLDER = Path("D:\\tmp") / datetime.datetime.now().strftime("%m-%d-%y_%H-%M-%S")
#FOLDER_OF_CONNECTIONS_PCAPS = Path(TEMP_FILES_FOLDER) / "connection_pcaps"
#CONVERSATIONS_PICKLES_FOLDER = Path(TEMP_FILES_FOLDER) / "conversation_pickles"


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


def main():
    print_logo()

    # Initialize the Global config object.
    #GlobalConfig.global_config = GlobalConfig.GlobalConfig(args.input_config)
    GlobalConfig.global_config = GlobalConfig.GlobalConfig('config.yaml')

    #TEMP_FILES_FOLDER.mkdir(parents=True, exist_ok=True)

    #init DB Class

    try:
        http_config = HttpSchema()

        #http_config.update_by_folder_of_conversations('db_handle')
        http_config.generate_from_db('db.db')

        #what are you?
        if GlobalConfig.global_config.vars.EXPAND_SIZES_IN_HTTP_CONFIG:
            http_config.expand_integer_sizes()

        http_config.write_schema('db.db')

        json_schemas = JsonSchemas()
        
        #json_schemas.update_by_conversations_folder(folder_conversation_path=
        #                                            CONVERSATIONS_PICKLES_FOLDER)
        json_schemas.generate_from_db('db.db')

        json_schemas.write_schemas('db.db')

        main_logger.info("SUCCESS!")
    except Exception as e:
        main_logger.exception(e)
        raise e
    #finally:.
        #shutil.rmtree(str(TEMP_FILES_FOLDER))

def temp_main():
    print_logo()
    while True:
        continue

if __name__ == "__main__":
    start_time = datetime.datetime.now()
    main()
    log_running_time(start_running=start_time)
