import logging
from logging.handlers import TimedRotatingFileHandler
import os
import time
from datetime import datetime, timedelta

class CustomLoggerHandler(TimedRotatingFileHandler):

    process_type = None

    def doRollover(self):
        # Close current stream
        if self.stream:
            self.stream.close()
            self.stream = None

        current_time = datetime.now()
        yesterday = current_time - timedelta(days=1)
        weekday = yesterday.strftime("%A")

        log_dir = os.path.dirname(self.baseFilename)
        rotated_file = os.path.join(
            log_dir,
            f"{self.process_type}_{weekday}.log"
        )

        if os.path.exists(rotated_file):
            os.remove(rotated_file)

        if os.path.exists(self.baseFilename):
            os.rename(self.baseFilename, rotated_file)

        if not self.delay:
            self.stream = self._open()

        new_rollover_at = self.computeRollover(int(time.time()))
        while new_rollover_at <= time.time():
            new_rollover_at += self.interval

        self.rolloverAt = new_rollover_at

def logger_setup(log_folder, process_type):

    log_formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)-7s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    log_file_path = os.path.join(log_folder, f"{process_type}_today.log")

    handler = CustomLoggerHandler(
        filename=log_file_path,
        when="midnight", 
        interval=1,
        backupCount=7
    )

    handler.process_type = process_type
    handler.setFormatter(log_formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    # Prevent duplicate handlers if logger_setup is called multiple times
    if not logger.handlers:
        logger.addHandler(handler)
        logger.addHandler(console_handler)

