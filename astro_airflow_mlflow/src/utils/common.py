# common.py file

from ensure import ensure_annotations # For ensuring type annotations
from box.exceptions import BoxValueError # For handling exceptions in ConfigBox
from .. import src_logger # Importing the logger from the parent package
from box import Box, ConfigBox # For handling configuration boxes
from pathlib import Path # For handling file paths
from typing import Any, Dict # For type hinting
import joblib # For saving and loading models
import os # For operating system related functionalities
import yaml # For handling YAML files
import json # For handling JSON files

@ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:
    """
    Reads a YAML file and returns its content as a ConfigBox.
    Args:
        path_to_yaml (Path): The path to the YAML file.
    Returns:
        ConfigBox: The content of the YAML file wrapped in a ConfigBox.
    Raises:
        ValueError: If the YAML file cannot be read or is invalid.
    """

    src_logger.info(f"Reading YAML file from {path_to_yaml}\n")

    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
            src_logger.info(f"YAML file read successfully: {path_to_yaml} \n")
            return ConfigBox(content)
    except BoxValueError as e:
        src_logger.error(f"Error reading YAML file: {e}\n")
        raise ValueError(f"Error reading YAML file: {e}") from e
    except Exception as e:
        src_logger.error(f"An unexpected error occurred while reading YAML file: {e}\n")
        raise e
    
@ensure_annotations
def create_directories(path_to_directories: list, verbose = True):
    """
    Creates directories if they do not exist.
    Args:
        path_to_directories (Path): The path to the directories to be created.
    """
    src_logger.info(f"Creating directories at {path_to_directories}\n")
    for path in path_to_directories:
        path = Path(path)
        try:
            if not os.path.exists(path):
                os.makedirs(path, exist_ok=True)
                if verbose:
                    src_logger.info(f"Created directory: {path}\n")
            else:
                if verbose:
                    src_logger.info(f"Directory already exists: {path}\n")
        except Exception as e:
            src_logger.error(f"Error creating directory {path}: {e}")
            raise e
        
@ensure_annotations
def save_json(path: Path, data: Dict[str, Any]) -> None:
    """
    Saves data to a JSON file.
    Args:
        path (Path): The path to the JSON file.
        data (Dict[str, Any]): The data to be saved.
    """
    src_logger.info(f"Saving data to JSON file at {path}")
    try:
        with open(path, 'w') as json_file:
            json.dump(data, json_file, indent=4)
            src_logger.info(f"Data saved successfully to {path}")
    except Exception as e:
        src_logger.error(f"Error saving data to JSON file: {e}")
        raise e
  
@ensure_annotations
def load_json(path: Path) -> Dict[str, Any]:
    """
    Loads data from a JSON file.
    Args:
        path (Path): The path to the JSON file.
    Returns:
        Dict[str, Any]: The data loaded from the JSON file.
    """
    src_logger.info(f"Loading data from JSON file at {path}")
    try:
        with open(path, 'r') as json_file:
            data = json.load(json_file)
            src_logger.info(f"Data loaded successfully from {path}")
            return ConfigBox(data)
    except Exception as e:
        src_logger.error(f"Error loading data from JSON file: {e}")
        raise e
    
@ensure_annotations
def save_model(path: Path, model: Any) -> None:
    """
    Saves a model to a specified path using joblib.
    Args:
        path (Path): The path where the model will be saved.
        model (Any): The model to be saved.
    """
    src_logger.info(f"Saving model to {path}")
    try:
        joblib.dump(model, path)
        src_logger.info(f"Model saved successfully at {path}")
    except Exception as e:
        src_logger.error(f"Error saving model: {e}")
        raise e
    
@ensure_annotations
def load_model(path: Path) -> Any:
    """
    Loads a model from a specified path using joblib.
    Args:
        path (Path): The path from where the model will be loaded.
    Returns:
        Any: The loaded model.
    """
    src_logger.info(f"Loading model from {path}")
    try:
        model = joblib.load(path)
        src_logger.info(f"Model loaded successfully from {path}")
        return model
    except Exception as e:
        src_logger.error(f"Error loading model: {e}")
        raise e
    