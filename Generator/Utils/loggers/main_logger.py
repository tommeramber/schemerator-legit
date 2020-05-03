import logging
import sys
from pathlib import Path

logger = None


def initialize_logger(log_name):
    # Log config.
    global main_logger
    main_logger = logging.getLogger(log_name)
    formatter = logging.Formatter("%(asctime)s (%(pathname)s:%(lineno)d) - %(levelname)s: %(message)s")

    # add file handler
    Path("logs").mkdir(exist_ok=True)
    log_file_handler = logging.FileHandler("logs/{}.log".format(log_name), mode="a")
    log_file_handler.setFormatter(formatter)
    log_file_handler.setLevel(logging.DEBUG)
    main_logger.addHandler(log_file_handler)
    # add stdout handler
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setFormatter(formatter)
    stdout_handler.setLevel(logging.DEBUG)
    main_logger.addHandler(stdout_handler)