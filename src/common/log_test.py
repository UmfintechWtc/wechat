import logging
import sys

from colorlog import ColoredFormatter

from src.common.const import *
from src.common.utility import CreateDirectory

logName = f"./logs/{APP_NAME}.log"


class XLogger_Test:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.logger = cls._instance.setup_logger()
        return cls._instance

    def setup_logger(self):
        CreateDirectory("logs")
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)

        # Create a file handler and set the log level to DEBUG
        file_handler = logging.FileHandler(logName)
        file_handler.setLevel(logging.DEBUG)

        # Create a formatter with the desired log format
        log_format = "%(asctime)s  %(levelname)-8s | %(message)s"
        formatter = logging.Formatter(log_format)

        # Set the formatter for both file handler and console handler
        file_handler.setFormatter(formatter)

        # Create a colored formatter for console output
        console_formatter = ColoredFormatter(
            "%(log_color)s%(asctime)s | %(levelname)-8s%(reset)s | %(log_color)s%(message)s%(reset)s")
        # support stdout
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(console_formatter)
        console_handler.setLevel(logging.DEBUG)

        # Add the handlers to the logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        return logger

    def set_log_level(self, module_name, level):
        module_logger = logging.getLogger(module_name)
        module_logger.setLevel(level)

    def set_apscheduler_log_level(self, level):
        apscheduler_logger = logging.getLogger('apscheduler')
        apscheduler_logger.setLevel(level)

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


xlogger = XLogger_Test()
xlogger.set_apscheduler_log_level(logging.INFO)
xlogger.set_log_level("urllib3", logging.WARNING)
xlogger.set_log_level("requests.packages.urllib3", logging.WARNING)