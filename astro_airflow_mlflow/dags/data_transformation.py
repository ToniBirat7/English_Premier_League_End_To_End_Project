# We will create the data transformation DAG for Airflow.

from airflow import DAG
from airflow.decorators import task
from datetime import datetime, timedelta
from src import src_logger as logger
from src.components.data_transformation import DataTransformation
from src.config.configuration import ConfigurationManager
from src.utils.eda_functions.eda_methods import generate_create_table_sql
from src.constants import *
from src.utils.common import read_yaml
from dotenv import load_dotenv
import os
import pymysql
import pandas as pd

# Load environment variables from .env file
load_dotenv()

# Define the paths for configuration files
db_config = {
  "host": os.getenv("main_mariadb_container_host", "localhost"),
  "user": os.getenv("main_mariadb_container_user"),
  "password": os.getenv("main_mariadb_container_password"),
  "database": os.getenv("cleaned_data_database_2"),
  "port": int(os.getenv("main_mariadb_container_port", 3306)),
}

logger.info("📦 Environment Variables Used:")
logger.info(f"  Host: {db_config['host']}")
logger.info(f"  User: {db_config['user']}")
logger.info(f"  Password: {db_config['password']}")
logger.info(f"  Port: {db_config['port']}")
logger.info(f"  Database: {db_config['database']}")

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

    # Define the task to save transformed data in MariaDB
    @task
    def save_transformed_data_in_mariadb():
        logger.info("Saving transformed data in MariaDB")

        mariadb_config = read_yaml(CONFIG_FILE_PATH)

        final_dataset_root_dir = mariadb_config['mariadb_load']['final_dataset_path']
        final_dataset_name = mariadb_config['mariadb_load']['final_dataset_name']
        table_name = mariadb_config['mariadb_load']['table_name']

        final_dataset_path = os.path.join(final_dataset_root_dir, final_dataset_name)
        logger.info(f"Final dataset path: {final_dataset_path}")

        # Read the final dataset
        try:
            df = pd.read_csv(final_dataset_path)
            logger.info(f"Final dataset loaded successfully with columns: {df.columns}")
        except FileNotFoundError:
            logger.error(f"Final dataset file not found at path: {final_dataset_path}")
            return
        except Exception as e:
            logger.error(f"Error reading final dataset: {e}")
            return
        
        # Generate CREATE TABLE SQL
        logger.info("Generating CREATE TABLE SQL")
        create_table_sql = generate_create_table_sql(df, table_name=table_name)
        logger.info(f"Generated SQL for creating table {table_name}:\n{create_table_sql}")

        # Connect to the MariaDB database
        try:
          # Connect to the DB
          conn = pymysql.connect(**db_config)
          cursor = conn.cursor()

          # Create table
          cursor.execute(create_table_sql)
          logger.info(f"✅ Table `{table_name}` created or already exists.")

          # Prepare and execute insert query
          placeholders = ", ".join(["%s"] * len(df.columns))
          insert_query = f"""
              INSERT INTO {table_name} ({', '.join(df.columns)})
              VALUES ({placeholders})
          """
          cursor.executemany(insert_query, df.values.tolist())
          conn.commit()
          logger.info(f"✅ Inserted {len(df)} rows into `{table_name}`")

        except Exception as e:
          logger.error("❌ Error:", e)

        finally:
          if conn:
              conn.close()
              logger.info("🔒 Connection closed.")

    # Define the task dependencies
    run_data_transformation_task = run_data_transformation()
    save_transformed_data_in_mariadb_task = save_transformed_data_in_mariadb()

    run_data_transformation_task >> save_transformed_data_in_mariadb_task