import sys
import pathlib2

import logging

from logging.handlers import SysLogHandler
from logging import FileHandler

SYSLOG_IP = "localhost"
SYSLOG_PORT = 517

##################################################################
# Log config.
alerts_logger = logging.getLogger(name="alerts_logger")
alerts_logger.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s:%(name)s:%(message)s")

pathlib2.Path("logs").mkdir(exist_ok=True)


log_file_handler = FileHandler("logs/alerts.log", mode="a")

log_file_handler.setFormatter(formatter)

# If want write into file from other level so change this here.
log_file_handler.setLevel(logging.INFO)

alerts_logger.addHandler(log_file_handler)

stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setFormatter(formatter)
stdout_handler.setLevel(logging.INFO)
alerts_logger.addHandler(stdout_handler)

syslog_handler = SysLogHandler((SYSLOG_IP, SYSLOG_PORT))
syslog_handler.setFormatter(formatter)
syslog_handler.setLevel(logging.INFO)
alerts_logger.addHandler(syslog_handler)
##################################################################



# import sys
# import pathlib2
#
# import logging
# ##################################################################
# # Log config.
# alerts_logger = logging.getLogger("alerts_logger")
# alerts_logger.setLevel(logging.INFO)
#
# formatter = logging.Formatter("%(asctime)s:%(name)s:%(message)s")
#
# pathlib2.Path("logs").mkdir(exist_ok=True)
# log_file_handler = logging.FileHandler("logs/alerts.log", mode="a")
#
# log_file_handler.setFormatter(formatter)
#
# # If want write into file from other level so change this here.
# log_file_handler.setLevel(logging.INFO)
#
# alerts_logger.addHandler(log_file_handler)
#
# stdout_handler = logging.StreamHandler(sys.stdout)
# stdout_handler.setFormatter(formatter)
# stdout_handler.setLevel(logging.INFO)
# alerts_logger.addHandler(stdout_handler)
# ##################################################################
