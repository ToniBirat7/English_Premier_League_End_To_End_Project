# This is an init file for the package
# __init__.py file
import os
import sys
import logging

logging_format = "[%(asctime)s] - %(levelname)s - %(message)s"

log_dirs = 'logs'
log_filepath = os.path.join(log_dirs, 'logging.log')

if not os.path.exists(log_dirs):
    os.makedirs(log_dirs)

logging.basicConfig(
    level=logging.INFO,
    format=logging_format,

    handlers=[
        logging.FileHandler(log_filepath), # Log to a file
        logging.StreamHandler(sys.stdout) # Log to console
    ]
)

src_logger = logging.getLogger("Logger Setup for The Project") # Create a logger for the package