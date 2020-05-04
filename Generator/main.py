#!/usr/bin/python3

import argparse
import sys
import os

import datetime
from pathlib import Path

import SharedUtils.main_logger as log

from Utils.SchamesClass.HttpSchema import HttpSchema
from Utils.SchamesClass.JsonSchemas import JsonSchemas

from Utils.ConfigClass import GlobalConfig


def log_running_time(start_running):
    log.main_logger.info("Program run {} until now.".format(datetime.datetime.now() - start_running))


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
    # TODO: Acctually use it
    log.initialize_logger('generator')
    GlobalConfig.global_config = GlobalConfig.GlobalConfig('config.yaml')
    db_path = '/home/db/db.db'

    try:
        http_config = HttpSchema()

        http_config.generate_from_db(db_path)

        #what are you?
        if GlobalConfig.global_config.vars.EXPAND_SIZES_IN_HTTP_CONFIG:
            http_config.expand_integer_sizes()

        http_config.write_schema(db_path)

        json_schemas = JsonSchemas()
        
        json_schemas.generate_from_db(db_path)

        json_schemas.write_schemas(db_path)

        log.main_logger.info("SUCCESS!")
    except Exception as e:
        log.main_logger.exception(e)

if __name__ == "__main__":
    start_time = datetime.datetime.now()
    main()
    log_running_time(start_running=start_time)
