# configuration.py file

from pathlib import Path
from src.constants import *
from src.utils.common import read_yaml
from src.entity.config_entity import DataIngestionConfig, DataValidationConfig, DataTransformationConfig, ModelTrainerConfig

# Configuration Manager
class ConfigurationManager:
  def __init__(self,
               config_file_path: Path,
               params_file_path: Path,
               schema_file_path: Path) -> None:
    
    self.config = read_yaml(config_file_path)
    self.schema = read_yaml(schema_file_path)
    self.params = read_yaml(params_file_path)

  def get_data_ingestion_config(self) -> DataIngestionConfig:
    return DataIngestionConfig(
      dataset_path=self.config.data_ingestion.dataset_location,
      root_dir=self.config.data_ingestion.root_dir,
    )

  def get_data_validation_config(self) -> DataValidationConfig:
    return DataValidationConfig(
      root_dir=self.config.data_validation.root_dir,
      STATUS_FILE=self.config.data_validation.STATUS_FILE,
      all_schema=self.schema.columns,
      dataset_path=self.config.data_validation.dataset_location
    )
  
  def get_data_transformation_config(self) -> DataTransformationConfig:
    return DataTransformationConfig(
      root_dir=self.config.data_transformation.root_dir,
      dataset_path=self.config.data_transformation.dataset_location
    )

  def get_model_trainer_config(self) -> ModelTrainerConfig:
    return ModelTrainerConfig(
      root_dir=self.config.model_trainer.root_dir,
      model_path=self.config.model_trainer.model_dir,
      model_name=self.config.model_trainer.model_name,
      model_params=self.params.ElasticNet,
      train_data_path=self.config.model_trainer.train_dataset_path,
      test_data_path=self.config.model_trainer.test_dataset_path,
      target_column=self.schema.target_column
    )