# data_ingestion.py file
# data_ingestion.py file

from src.entity.config_entity import DataIngestionConfig
from src.utils.common import create_directories
from src import src_logger
from pathlib import Path
import pandas as pd
import os

class DataIngestion:
  def __init__(self,
               config:DataIngestionConfig) -> None:
    
    self.config = config
    create_directories([self.config.dataset_path, self.config.root_dir, self.config.ingestion_dir])

  def read_data(self, file_name: str) -> pd.DataFrame:
    """
    Reads the dataset from the specified path in the configuration.
    Returns:
        pd.DataFrame: The dataset as a pandas DataFrame.
    """
    src_logger.info("Reading the Data from the dataset path")
    data_set_path = self.config.dataset_path
    src_logger.info(f"We are Reading the Data from {data_set_path}")
    return pd.read_csv(os.path.join(data_set_path, file_name))

  def store_data(self, data: pd.DataFrame, file_name: str) -> None:
    src_logger.info(f"Storing the Data to {self.config.ingestion_dir}/{file_name}")
    data.to_csv(os.path.join(self.config.ingestion_dir, file_name), index=False)

  def fetch_all_files(self) -> None:
    """
    Fetches all files from the dataset path and stores them in the ingestion directory.
    """
    src_logger.info("Fetching all files from the dataset path")

    file_name_list = [file for file in os.listdir(self.config.dataset_path) if file.endswith('.csv')]

    if not file_name_list:
        src_logger.warning("No CSV files found in the dataset path.")
        return
    src_logger.info(f"Found {len(file_name_list)} CSV files in the dataset path")
    src_logger.info(f"Found CSV files: {file_name_list}")

    for file_name in file_name_list:
        data = self.read_data(file_name)
        self.store_data(data, file_name)
        src_logger.info(f"Stored {file_name} in {self.config.ingestion_dir}")

    src_logger.info("Fetching all files completed.")

    file_name_in_ingestion_dir = os.listdir(self.config.ingestion_dir)
    src_logger.info(f"Files in ingestion directory: {file_name_in_ingestion_dir}")

  def get_dataset_path(self) -> Path:
    return Path(self.config.ingestion_dir)