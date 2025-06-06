# First well need to connect to MariaDB to fetch the data

# We will create the data transformation DAG for Airflow.

from airflow import DAG
from airflow.decorators import task
from datetime import datetime, timedelta
from src import src_logger as logger
from src.constants import *
from src.utils.common import read_yaml, create_directories
from dotenv import load_dotenv
import os
import pymysql
import pandas as pd
from pathlib import Path
import redis
import pyarrow as pa
import pyarrow.parquet as pq
from io import BytesIO

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

redis_config = {
  "host": os.getenv("redis_container_host", "localhost"),
  "port": int(os.getenv("redis_container_port", 6379)),
  "name": os.getenv("redis_container_name", "main-redis"),
}

logger.info("📦 Environment Variables Used:")
logger.info(f"  Host: {db_config['host']}")
logger.info(f"  User: {db_config['user']}")
logger.info(f"  Password: {db_config['password']}")
logger.info(f"  Port: {db_config['port']}")
logger.info(f"  Database: {db_config['database']}")
logger.info("📦 Redis Configuration:")
logger.info(f"  Redis Host: {redis_config['host']}")
logger.info(f"  Redis Port: {redis_config['port']}")
logger.info(f"  Redis Name: {redis_config['name']}")  

# Define the default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Read the MariaDB configuration
model_train_config = read_yaml(CONFIG_FILE_PATH)

# Define the DAG
with DAG(
    dag_id='data_transformation',
    default_args=default_args,
    schedule='@daily',
    catchup=False
) as dag:

    # Define the task to load the data from the MariaDB database and perform data transformation
    @task
    def load_from_mariadb_save_the_final_dataset():
        logger.info("Loading data from MariaDB")

        table_name = model_train_config['mariadb_load']['table_name']

        logger.info(f"Table name to load data from: {table_name}")

        # Connect to the MariaDB database
        connection = pymysql.connect(
            host=db_config['host'],
            user=db_config['user'],
            password=db_config['password'],
            database=db_config['database'],
            port=db_config['port']
        )

        try:
            # Load data from the specified table
            query = f"SELECT * FROM {table_name}"
            df = pd.read_sql(query, connection)
            logger.info(f"Data loaded successfully from {table_name}")

            # Log DataFrame information
            logger.info(f"DataFrame shape: {df.shape}")
            logger.info(f"DataFrame columns: {df.columns.tolist()}")

            logger.info("Data Loading completed successfully")

            # Save the final dataset to a CSV file
            final_dataset_root_dir = model_train_config['model_trainer']['save_train_data_dir']
            final_dataset_name = model_train_config['model_trainer']['dataset_name']

            create_directories([final_dataset_root_dir])

            logger.info(f"Final dataset root directory: {final_dataset_root_dir}")

            final_dataset_path = os.path.join(final_dataset_root_dir, final_dataset_name)
            df.to_csv(final_dataset_path, index=False)
            logger.info(f"Final dataset saved to {final_dataset_path}")

            return Path(final_dataset_path)

        except Exception as e:
            logger.error(f"Error during data loading and transformation: {e}")
        finally:
            connection.close()
    @task
    def load_final_csv_file_and_save_to_redis(final_dataset_path):
        logger.info("Loading final CSV file and saving to Redis")

        # Load the final dataset from the specified path
        try:
            df = pd.read_csv(final_dataset_path)
            logger.info(f"Final dataset loaded successfully with shape: {df.shape}")
        except FileNotFoundError:
            logger.error(f"Final dataset file not found at path: {final_dataset_path}")
            return
        except Exception as e:
            logger.error(f"Error reading final dataset: {e}")
            return
        # Test the Redis connection
        try:
            redis_client = redis.Redis(host=redis_config['host'], port=redis_config['port'], decode_responses=False)
            redis_client.ping()
            logger.info("✅ Redis connection successful")

            # Check if the Redis key already exists
            if redis_client.exists(model_train_config['redis_key']['final_dataset_key']):
                logger.warning(f"⚠️ Redis key '{model_train_config['redis_key']['final_dataset_key']}' already exists. Overwriting it.")
        except redis.ConnectionError as e:
            logger.error(f"❌ Redis connection failed: {e}")
            return

        # Convert DataFrame to PyArrow format and save to Redis
        try:
            table = pa.Table.from_pandas(df)
            buffer = BytesIO()
            pq.write_table(table, buffer)
            parquet_bytes = buffer.getvalue()

            # Save the data to Redis
            redis_client.set(model_train_config['redis_key']['final_dataset_key'], parquet_bytes)
            logger.info(f"✅ Final dataset saved to Redis with key: {model_train_config['redis_key']['final_dataset_key']}")
        except Exception as e:
            logger.error(f"❌ Error saving final dataset to Redis: {e}")
      
    @task
    def load_data_from_redis_visualize_with_MLFlow():
        
        logger.info("Loading data from Redis and visualizing with MLFlow")

        # Load data from Redis
        try:
            redis_client = redis.Redis(host=model_train_config['redis_key']['host'], port=model_train_config['redis_key']['port'], decode_responses=False)
            redis_client.ping()
            logger.info("✅ Redis connection successful")
            # Fetch the final dataset from Redis
            logger.info(f"Fetching final dataset from Redis with key: {model_train_config['redis_key']['final_dataset_key']}")

            # Check if the key exists in Redis
            if not redis_client.exists(model_train_config['redis_key']['final_dataset_key']):
                logger.error(f"❌ Redis key '{model_train_config['redis_key']['final_dataset_key']}' does not exist.")
                return
            logger.info(f"✅ Redis key '{model_train_config['redis_key']['final_dataset_key']}' exists. Proceeding to load data.")

            # Load the final dataset from Redis
            parquet_bytes = redis_client.get(model_train_config['redis_key']['final_dataset_key'])
            if parquet_bytes:
                buffer = BytesIO(parquet_bytes)
                table = pq.read_table(buffer)
                df = table.to_pandas()
                logger.info(f"✅ Final dataset loaded from Redis with shape: {df.shape}")
                logger.info(f"Final dataset loaded from Redis columns: {df.columns.tolist()}")
            else:
                logger.warning(f"⚠️ No data found in Redis for key: {model_train_config['redis_key']['final_dataset_key']}")
        except Exception as e:
            logger.error(f"❌ Error loading final dataset from Redis: {e}")
            return

    # Task Dependency
    load_and_transform_data_task = load_from_mariadb_save_the_final_dataset()
    save_to_redis_task = load_final_csv_file_and_save_to_redis(load_and_transform_data_task)