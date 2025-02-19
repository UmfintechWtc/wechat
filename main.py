import argparse
import sys
import logging
import threading
from app import openapi, alarm
from src.common.const import *
from src.common.log import XLogger
from src.config.wechat_config import Config
import signal
import getpass


class DefaultHelpParser(argparse.ArgumentParser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def error(self, message):
        print(f"{message}", file=sys.stderr)
        self.print_help()
        sys.exit(1)

    def add_options(self):
        self.add_argument('-c', '--config', default=f"{APP_CONFIG_DEFAULT_PATH}", required=False,
                          help=f"configuration path. default: {APP_CONFIG_DEFAULT_PATH}")
        self.add_argument('-H', '--Host', default="0.0.0.0", required=False,
                          help=f"listen ip address. default: 0.0.0.0")


class Parser:

    def __init__(self):
        self.parser = DefaultHelpParser()
        self.parser.add_options()

    @property
    def parse(self):
        args = self.parser.parse_args()
        return args

def signal_handler(signum, frame):
    global exit_event
    xlogger.info(f"Received signal {signum}. Program interrupted by user: {getpass.getuser()}")
    exit_event.set()


if __name__ == '__main__':
    args = Parser().parse
    config: Config = Config(args.config)

    # 初始化日志
    if config.log:
        xlogger = XLogger(config.log)
    else:
        xlogger = XLogger()
    xlogger.set_log_level("urllib3", logging.WARNING)
    xlogger.set_log_level("requests.packages.urllib3", logging.WARNING)

    openapi_instance = openapi(config)
    alarm_instance = alarm(config)

    # 创建并启动线程
    threading.Thread(
        target=alarm_instance.run,
        kwargs={
            'host': args.Host,
            'port': config.qywx.application.alarm.port,
            'debug': False
        },
        daemon=True
    ).start()
    threading.Thread(
        target=openapi_instance.run,
        kwargs={
            'host': args.Host,
            'port': config.qywx.application.openapi.port,
            'debug': False
        },
        daemon=True
    ).start()

    for sig in [signal.SIGINT, signal.SIGTERM]:
        signal.signal(sig, signal_handler)

    exit_event = threading.Event()
    try:
        while not exit_event.is_set():
            exit_event.wait(timeout=1)
        xlogger.info("All threads terminated. Exiting.")
    except Exception as e:
        xlogger.fatal(str(e))