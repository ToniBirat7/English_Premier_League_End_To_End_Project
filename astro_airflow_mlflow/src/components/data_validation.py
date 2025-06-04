# data_validation.py file

from src.entity.config_entity import DataValidationConfig
from src.utils.common import create_directories
from src import src_logger
from pathlib import Path
import pandas as pd
import os

class DataValidation:
    def __init__(self, config: DataValidationConfig) -> None:
        self.config = config
        create_directories([self.config.root_dir])

    def validate_data(self) -> bool:
        """
        Validates the data against the schema.
        Returns:
            bool: True if data is valid, False otherwise.
        """
        src_logger.info("Validating data against schema")
        # List all the files names from the dataset path, validate if all the files are CSV files
        file_name_list = [file for file in os.listdir(self.config.dataset_path) if file.endswith('.csv')]

        src_logger.info(f"Found {len(file_name_list)} CSV files in the dataset path")

        src_logger.info(f"CSV files found: {file_name_list}")

        if not file_name_list:
            src_logger.error("No CSV files found")
            return False
        
        src_logger.info("Data validation passed")
        return True

    def save_validation_status(self, status: bool) -> None:
        """
        Saves the validation status to a file.
        """
        status_file_path = self.config.STATUS_FILE
        with open(status_file_path, 'w') as f:
            f.write("True" if status else "False")
        src_logger.info(f"Validation status saved to {status_file_path}")

    def get_dataset_path(self) -> Path:
        return Path(self.config.dataset_path)