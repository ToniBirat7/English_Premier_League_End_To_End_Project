# Automated Script for a complete end-to-end ML project

from pathlib import Path
import logging
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

list_of_files = [
  f"WebApp/__init__.py",
]

for filepath in list_of_files:
    filepath = Path(filepath)
    filedir,filename = os.path.split(filepath)
    print(f"Processing file: {filedir}, {filename}")
    print(f"Type of file: {type(filedir)}")
    if not os.path.exists(filedir):
        if (not filedir):
            logging.info(f"File directory is empty, creating in current directory.")
        else:
          logging.info(f"Creating directory: {filedir}")
          os.makedirs(filedir,exist_ok=True)
    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        logging.info(f"Creating file: {filepath}")
        with open(filepath, 'w') as f:
          logging.info(f"Writing to file: {filepath}")
          # Write a comment or placeholder content based on the file type
          if filename == "__init__.py":
              f.write("# This is an init file for the package\n")
          if filename == "config.yaml":
              f.write("# Configuration file for the project\n")
          elif filename == "params.yaml":
              f.write("# Parameters for the project\n")
          elif filename == "schema.yaml":
              f.write("# Schema for the project\n")
          elif filename == "main.py":
              f.write("# Main entry point for the project\n")
          elif filename == "Dockerfile":
              f.write("# Dockerfile for the project\n")
          elif filename == "setup.py":
              f.write("# Setup script for the project\n")
          else:
              f.write(f"# {filename} file\n")
    else:
        logging.info(f"File already exists and is not empty: {filepath}")