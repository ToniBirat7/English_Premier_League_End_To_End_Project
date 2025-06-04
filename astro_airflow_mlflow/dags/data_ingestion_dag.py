# Here we will define the DAG for data ingestion

from airflow import DAG
from datetime import datetime, timedelta
from src import src_logger as logger
from airflow.decorators import task
from src.components.data_ingestion import DataIngestion
from src.entity.config_entity import DataIngestionConfig
from src.config.configuration import ConfigurationManager
from src.pipeline.data_ingestion_pipeline import DataIngestionTrainingPipeline
from src.constants import *

# Define the default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
with DAG(
    'data_ingestion_dag',
    default_args=default_args,
    description='DAG for data ingestion',
    schedule=timedelta(days=1),
) as dag:

    @task
    def initialize_configuration_manager():
        """
        Task to initialize the configuration manager and return config as dict.
        """
        logger.info("Initializing configuration manager")
        config_manager = ConfigurationManager(
            config_file_path=CONFIG_FILE_PATH,
            params_file_path=PARAMS_FILE_PATH,
            schema_file_path=SCHEMA_FILE_PATH,
        )
        config = config_manager.get_data_ingestion_config()
        logger.info("Configuration manager initialized successfully")
        
        # Return config as a dictionary to avoid serialization issues
        config_dict = {
            'dataset_path': str(config.dataset_path),
            'root_dir': str(config.root_dir),
            'ingestion_dir': str(config.ingestion_dir)
        }
        logger.info(f"Configuration: {config_dict}")
        return config_dict

    @task
    def data_ingestion_task(config_dict):
        """
        Task to perform data ingestion.
        """
        logger.info("Starting data ingestion task")
        logger.info(f"Using configuration: {config_dict}")
        
        # Recreate the configuration manager to get the config object
        config_manager = ConfigurationManager(
            config_file_path=CONFIG_FILE_PATH,
            params_file_path=PARAMS_FILE_PATH,
            schema_file_path=SCHEMA_FILE_PATH,
        )
        config = config_manager.get_data_ingestion_config()
        
        # Perform data ingestion
        data_ingestion = DataIngestion(config)
        data_ingestion.fetch_all_files()
        
        logger.info("Data ingestion task completed successfully")
        
        # Return the dataset path as string
        dataset_path = str(data_ingestion.get_dataset_path())
        return dataset_path
   
    @task
    def log_the_path(dataset_path):
        """
        Task to log the dataset path.
        """
        logger.info(f"Dataset is stored in the path: {dataset_path}")
    
    # Define task dependencies
    config = initialize_configuration_manager()
    dataset_path = data_ingestion_task(config)
    log_the_path(dataset_path)