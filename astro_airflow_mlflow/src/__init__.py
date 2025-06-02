import os
import sys
import logging

log_dirs = '/usr/local/airflow/logs'
log_filepath = os.path.join(log_dirs, 'logging.log')
os.makedirs(log_dirs, exist_ok=True)

def get_logger(name="EPLLogger"):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.hasHandlers():
        formatter = logging.Formatter("[%(asctime)s] - %(levelname)s - %(message)s")
        file_handler = logging.FileHandler(log_filepath)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        logger.addHandler(logging.StreamHandler(sys.stdout))

    return logger
