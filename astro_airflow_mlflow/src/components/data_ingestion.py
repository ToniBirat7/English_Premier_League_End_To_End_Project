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

  def read_data(self) -> pd.DataFrame:
    """
    Reads the dataset from the specified path in the configuration.
    Returns:
        pd.DataFrame: The dataset as a pandas DataFrame.
    """
    src_logger.info("Reading the Data from the dataset path")
    data_set_path = self.config.dataset_path
    src_logger.info(f"We are Reading the Data from {data_set_path}")
    return pd.read_csv(data_set_path)

  def store_data(self, data: pd.DataFrame) -> None:
    src_logger.info(f"Storing the Data to {self.config.ingestion_path}")
    data.to_csv(os.path.join(self.config.ingestion_dir, self.config.ingestion_path), index=False)

  def get_dataset_path(self) -> Path:
    return Path(os.path.join(self.config.ingestion_dir, self.config.ingestion_path))