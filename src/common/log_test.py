import logging
import sys
import os
import time
from colorlog import ColoredFormatter

from src.common.const import *
from src.common.utility import CreateDirectory

logName = f"{os.path.dirname(os.path.abspath(__file__))}/logs/{APP_NAME}-{str(time.strftime('%Y-%m-%d'))}.log"


class XLogger:
    _instance = None

    def __new__(cls, output: str = "stdout"):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.logger = cls._instance.setup_logger(output)
        return cls._instance

    def setup_logger(self, output):
        # set the log level to DEBUG
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        # Create a formatter with the desired log format
        log_format = "%(asctime)s  %(levelname)-8s | %(message)s"
        formatter = logging.Formatter(log_format)
        if output == "stdout":
            # Create a colored formatter for console output
            console_formatter = ColoredFormatter(
                "%(log_color)s%(asctime)s | %(levelname)-8s%(reset)s | %(log_color)s%(message)s%(reset)s")
            # support stdout
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(console_formatter)
            logger.addHandler(console_handler)
        else:
            # Create a file handler and logs path
            CreateDirectory("logs")
            file_handler = logging.FileHandler(logName)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

        return logger

    def set_log_level(self, module_name, level):
        module_logger = logging.getLogger(module_name)
        module_logger.setLevel(level)

    # def set_apscheduler_log_level(self, level):
    #     apscheduler_logger = logging.getLogger('apscheduler')
    #     apscheduler_logger.setLevel(level)

    def info(self, msg):
        self.logger.info(msg)

    def debug(self, msg):
        self.logger.debug(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)

    def fatal(self, msg):
        self.logger.fatal(msg)
        exit(1)
