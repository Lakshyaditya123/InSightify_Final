import logging as lg
from pythonjsonlogger.json import JsonFormatter

leveldict = {
    'DEBUG': lg.DEBUG,
    'INFO': lg.INFO,
    'WARNING': lg.WARNING,
    'ERROR': lg.ERROR,
    'CRITICAL': lg.CRITICAL
}


class Logger:  # Capitalized class name following Python conventions

    def __init__(self, level=lg.INFO,
                 log_file="Task.log"):
        # Logging setup
        self.log = lg.getLogger(__name__)
        self.log.setLevel(level)

        # Clear any existing handlers to avoid duplicates
        self.log.handlers.clear()

        # Log file handler
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

    # Convenience methods for different log levels
    def debug(self, message):
        self.log.debug(message)

    def info(self, message):
        self.log.info(message)

    def warning(self, message):
        self.log.warning(message)

    def error(self, message):
        self.log.error(message)

    def critical(self, message):
        self.log.critical(message)