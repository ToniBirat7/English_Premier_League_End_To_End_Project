# Automated Script for a complete end-to-end ML project

from pathlib import Path
import logging
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

list_of_files = [
  ".github/workflows/.gitkeep",
  f"src/__init__.py",
  f"src/components/__init__.py",
  f"src/components/data_ingestion.py",
  f"src/components/data_validation.py",
  f"src/components/data_transformation.py",
  f"src/components/model_trainer.py",
  f"src/components/model_evaluation.py",
  f"src/components/model_pusher.py",
  f"src/utils/__init__.py",
  f"src/utils/common.py",
  f"src/utils/logger.py",
  f"src/config/__init__.py",
  f"src/config/configuration.py",
  f"src/pipeline/__init__.py",
  f"src/entity/__init__.py",
  f"src/entity/config_entity.py",
  f"src/constants/__init__.py",
  "config/config.yaml",
  "params.yaml",
  "schema.yaml",
  "main.py",
  "Dockerfile",
  "setup.py",
  "research/research.ipynb",
  "templates/index.html",
  "requirements.txt",
  "README.md",
  ".gitignore",
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