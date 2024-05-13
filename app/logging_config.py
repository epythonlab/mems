# logger_config.py

import logging
from logging.handlers import TimedRotatingFileHandler

def setup_logging():
    # Create a TimedRotatingFileHandler with the desired configuration
    handler = TimedRotatingFileHandler(filename='errors.log', when='midnight', interval=1, backupCount=0)

    # Set the logging level to ERROR
    handler.setLevel(logging.ERROR)

    # Define the log format
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    # Add the handler to the root logger
    logging.root.addHandler(handler)
