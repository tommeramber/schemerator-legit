#!/usr/bin/python3

import pathlib
import subprocess

from pathlib import Path

from Utils.loggers.main_logger import main_logger
from Utils.HelpLibs.binary_object_helper import get_iterator_all_files_name

SEPARATE_LINE_SIGN = "\n##################################################################"


def split_pcap(pcap_path, folder_for_save_connections=Path("connection_pcaps")):
    """
    This function wrapper the tool PcapSplitter.
    split files by connection, meaning all packets of a connection will be in the same file.

    :param pcap_path: Pcap file to split, or folder of pcaps.
    :param folder_for_save_connections: Folder to save all pcap files.
    """
    pathlib.Path(folder_for_save_connections).mkdir(parents=True, exist_ok=True)

    # All logs from Pcap splitter will be between two SEPARATE_LINE_SIGN
    main_logger.info(SEPARATE_LINE_SIGN)
    main_logger.info("PcapSplitter :\n")

    if pathlib.Path(pcap_path).is_file():
        pcaps_to_split = [pcap_path]
    elif pathlib.Path(pcap_path).is_dir():
        pcaps_to_split = get_iterator_all_files_name(pcap_path)
    else:
        raise FileNotFoundError

    for curr_pcap_path in pcaps_to_split:
        pcap_splitter = subprocess.run(["PcapSplitter",
                                        "-f", str(Path(curr_pcap_path).absolute()),
                                        "-o", str(folder_for_save_connections),
                                        "-m", "connection",
                                        "-p", "16"],
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)

        # Print the result from PcapSplitter,
        # when have error PcapSplitter print a lot of information that not needed after "\n\n\n" so we cut this.
        main_logger.info(pcap_splitter.stdout.decode("utf-8").split("\n\n\n", 1)[0])

    # Only when error occur have strings in stderr.
    if pcap_splitter.stderr:
        main_logger.error(pcap_splitter.stderr)

    main_logger.info(SEPARATE_LINE_SIGN)
