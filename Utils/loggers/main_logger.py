import logging
import sys
import pathlib2

##################################################################
# Log config.
main_logger = logging.getLogger("main_logger")
main_logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s:%(name)s:%(message)s")

# add file handler
pathlib2.Path("logs").mkdir(exist_ok=True)
log_file_handler = logging.FileHandler("logs/main.log", mode="a")
log_file_handler.setFormatter(formatter)
main_logger.addHandler(log_file_handler)
# add stdout handler
stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setFormatter(formatter)
stdout_handler.setLevel(logging.INFO)
main_logger.addHandler(stdout_handler)
##################################################################
