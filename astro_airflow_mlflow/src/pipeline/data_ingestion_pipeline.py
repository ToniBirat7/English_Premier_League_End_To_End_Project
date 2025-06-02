from src.config.configuration import ConfigurationManager
from src.components.data_ingestion import DataIngestion
from src.constants import *
from src import src_logger

STAGE_NAME = "Data Ingestion Pipeline"

class DataIngestionTrainingPipeline:
  def __init__(self) -> None:
    pass

  def main(self):
    config = ConfigurationManager(
    config_file_path=CONFIG_FILE_PATH,
    params_file_path=PARAMS_FILE_PATH,
    schema_file_path=SCHEMA_FILE_PATH
  )

    src_logger.info("Initialized Config Manager\n")

    data_ingestion = DataIngestion(config=config.get_data_ingestion_config())
    src_logger.info("Initialized DataIngestion\n")

    data_set_path = data_ingestion.get_dataset_path()
    src_logger.info(f"We are reading dataset from {data_set_path}\n")

    load_data = data_ingestion.read_data()
    src_logger.info(f"Data loaded successfully from {data_set_path}\n")
    src_logger.info(f"Data shape: {load_data.shape}\n")
    src_logger.info(f"Data columns: {load_data.columns.tolist()}\n")

    data_ingestion.store_data(load_data)
    src_logger.info(f"Data stored successfully to {data_ingestion.config.ingestion_path}\n")
    
if __name__ == '__main__':
  try:
    src_logger.info(f">>>>>> Stage {STAGE_NAME} Started <<<<<<<\n")
    obj = DataIngestionTrainingPipeline()
    obj.main()
    src_logger.info(f">>>>> Stage {STAGE_NAME} Completed <<<<<<\n")
  except Exception as e:
    src_logger.exception(e)
    raise e