import os
import sys
import logging

# log_dirs = '/usr/local/airflow/logs' # Container path for logs
log_dirs = './logs' # Local path for logs, useful for local development
log_filepath = os.path.join(log_dirs, 'logging.log')

# Create log directory if it doesn't exist
os.makedirs(log_dirs, exist_ok=True)

# Create logger
src_logger = logging.getLogger("Logger Setup for The Project")
src_logger.setLevel(logging.INFO)

# Setup logging format
formatter = logging.Formatter("[%(asctime)s] - %(levelname)s - %(message)s")

# Avoid adding handlers multiple times in subprocesses
if not src_logger.hasHandlers():
    # File handler
    file_handler = logging.FileHandler(log_filepath)
    file_handler.setFormatter(formatter)
    src_logger.addHandler(file_handler)

    # Stream handler (stdout for Airflow UI)
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)
    src_logger.addHandler(stream_handler)
