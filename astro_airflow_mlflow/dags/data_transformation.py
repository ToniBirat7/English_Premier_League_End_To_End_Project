# We will create the data transformation DAG for Airflow.
from airflow import DAG
from airflow.decorators import task
from datetime import datetime, timedelta
from src import src_logger as logger
from src.components.data_transformation import DataTransformation
from src.config.configuration import ConfigurationManager
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
    dag_id='data_transformation',
    default_args=default_args,
    schedule='@daily',
    catchup=False
) as dag:

    @task
    def run_data_transformation():
        config = ConfigurationManager(
            config_file_path=CONFIG_FILE_PATH,
            params_file_path=PARAMS_FILE_PATH,
            schema_file_path=SCHEMA_FILE_PATH
        ).get_data_transformation_config()

        logger.info("Initialized Config Manager for Data Transformation\n")

        data_transformation = DataTransformation(config=config)

        logger.info("Initialized DataTransformation\n")

        is_saved = data_transformation.transform_data()

        if is_saved:
            logger.info("Data Transformation completed and saved successfully.")
        else:
            logger.warning("Data Transformation did not save any data.")

    run_data_transformation()