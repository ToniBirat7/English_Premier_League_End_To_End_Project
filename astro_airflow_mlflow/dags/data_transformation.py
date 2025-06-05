# We will create the data transformation DAG for Airflow.

from airflow import DAG
from airflow.decorators import task
from datetime import datetime, timedelta
from src import src_logger as logger
from src.components.data_transformation import DataTransformation
from src.config.configuration import ConfigurationManager
from src.constants import *
from src.utils.common import read_yaml
from dotenv import load_dotenv
import os
import pymysql
import pandas as pd

# Load environment variables from .env file
load_dotenv()

# Access them using os.environ
main_maradb_container_name = os.getenv("main_maradb_container_name")
container_port = os.getenv("main_mariadb_container_port")
mariadb_root_user = os.getenv("main_mariadb_container_user")
mariadb_root_password = os.getenv("main_mariadb_container_password")
host_name = os.getenv("host")

# Database paths
scrapped_dataset_path = os.getenv("scrapped_data_database_1")
cleaned_dataset_path = os.getenv("cleaned_data_database_2")

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

# Another DAG for the establishing mariadb connection and saving the transformed data

    @task
    def save_transformed_data_in_mariadb():
        logger.info("Saving transformed data in MariaDB")

        mariadb_config = read_yaml(CONFIG_FILE_PATH)

        final_dataset_root_dir = mariadb_config['mariadb_load']['final_dataset_path']
        final_dataset_name = mariadb_config['mariadb_load']['final_dataset_name']

    run_data_transformation()