# config_entity.py file
from dataclasses import dataclass
from pathlib import Path

@dataclass
class DataIngestionConfig:
    """Data Ingestion Configuration"""
    dataset_path: Path
    root_dir: Path
    ingestion_path: Path
    ingestion_dir: Path

@dataclass
class DataValidationConfig:
    """
    Data Validation Configuration
    This class holds the configuration for data validation, including the root directory,
    status file, and the schema for validation.
    Attributes:
        root_dir (Path): The root directory where the data validation files are stored.
        STATUS_FILE (str): The name of the status file used to track validation status.
        all_schema (dict): A dictionary containing the schema for data validation.
    """
    root_dir: Path
    STATUS_FILE: Path
    all_schema: dict
    dataset_path: Path

@dataclass
class DataTransformationConfig:
    """Data Transformation Configuration"""
    root_dir: Path
    dataset_path: Path


@dataclass
class ModelTrainerConfig:
    """Model Trainer Configuration"""
    root_dir: Path
    model_path: Path
    model_name: str
    model_params: dict
    train_data_path: Path
    test_data_path: Path
    target_column: str

