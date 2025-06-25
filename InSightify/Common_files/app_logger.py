import logging as lg
from pythonjsonlogger.json import JsonFormatter
leveldict = {
    'DEBUG': lg.DEBUG,
    'INFO': lg.INFO,
    'WARNING': lg.WARNING,
    'ERROR': lg.ERROR,
    'CRITICAL': lg.CRITICAL
}


class logger:

    def _init_(self, level=lg.INFO, log_file="/Users/lakshyadityabhatnagar/Desktop/Intern work Tasks/New_InSightify/InSightify_Backend/insightify_app/Task.log"):
        # Logging setup
        self.log = lg.getLogger(__name__)
        self.log.setLevel(level)

        # Log file
        file_handler = lg.FileHandler(filename=log_file, mode="w")
        formatter=JsonFormatter("%(asctime)s %(levelname)s %(message)s")
        file_handler.setFormatter(formatter)
        self.log.addHandler(file_handler)

        # Terminal
        stream_handler = lg.StreamHandler()
        stream_handler.setFormatter(formatter)
        self.log.addHandler(stream_handler)


    def get_logger(self):
       return self.log