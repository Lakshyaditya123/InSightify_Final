import logging as lg
from pythonjsonlogger.json import JsonFormatter
from InSightify.Common_files.config import config

class Logger:

    def __init__(self, level=lg.INFO, log_file=config.LOG_FILE):
        # Logging setup
        self.log = lg.getLogger(__name__)
        self.log.setLevel(level)
        self.log.handlers.clear()
        file_handler = lg.FileHandler(filename=log_file, mode="a")
        formatter = JsonFormatter("%(asctime)s %(levelname)s %(message)s")
        file_handler.setFormatter(formatter)
        self.log.addHandler(file_handler)

        # Terminal handler
        stream_handler = lg.StreamHandler()
        stream_handler.setFormatter(formatter)
        self.log.addHandler(stream_handler)

    def get_logger(self):
        return self.log
