import logging
import sys

main_logger = None


def initialize_logger(log_name):
    # Log config.
    global main_logger
    if not main_logger:
        main_logger = logging.getLogger(log_name)
        main_logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(asctime)s (%(pathname)s:%(lineno)d) - %(levelname)s: %(message)s")
    
        # add file handler
        #log_file_handler = logging.FileHandler(log_path, mode="a")
        #log_file_handler.setFormatter(formatter)
        #log_file_handler.setLevel(logging.INFO)
        #main_logger.addHandler(log_file_handler)
    
        # add stdout handler
        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setFormatter(formatter)
        stdout_handler.setLevel(logging.DEBUG)
        main_logger.addHandler(stdout_handler)
