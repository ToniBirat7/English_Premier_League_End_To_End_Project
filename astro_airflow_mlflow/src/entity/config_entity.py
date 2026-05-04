# config_entity.py file
from dataclasses import dataclass
from pathlib import Path

@dataclass
class DataIngestionConfig:
    """Data Ingestion Configuration"""
    dataset_path: Path
    root_dir: Path
    ingestion_dir: Path

@dataclass
class DataValidationConfig:
    """
    Data Validation Configuration
    Attributes:
        root_dir: Where the data validation status file is written.
        STATUS_FILE: yaml status file path.
        dataset_path: Directory of CSVs to validate (post-ingestion).
        raw_columns: {column_name: dtype_string} required in every input CSV.
    """
    root_dir: Path
    STATUS_FILE: Path
    dataset_path: Path
    raw_columns: dict

@dataclass
class DataTransformationConfig:
    """Data Transformation Configuration"""
    root_dir: Path
    dataset_path: Path
    status_file: Path

@dataclass
class ModelTrainerConfig:
    """Model Trainer Configuration"""
    root_dir: Path
    model_path: Path
    model_name: str
    model_params: dict
    train_dir: Path
    test_dir: Path
    train_data_path: Path
    test_data_path: Path
    target_column: str

