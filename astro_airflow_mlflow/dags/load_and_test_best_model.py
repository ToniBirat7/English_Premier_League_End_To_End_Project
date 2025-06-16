# Load the Dataset from the Redis and Load the Saved Model from MLFlow and Test the Model
# Compare the predictions with the actual values and log the results

import os
import redis
import pandas as pd
import pymysql
import pyarrow as pa
from io import BytesIO
from pathlib import Path
from airflow import DAG
from dotenv import load_dotenv
from datetime import datetime, timedelta
from airflow.decorators import task
import pyarrow.parquet as pq
import mlflow
from src import src_logger as logger
from src.constants import *
from src.utils.common import read_yaml, create_directories
from src.components.model_trainer import ModelTrainer
from src.config.configuration import ConfigurationManager
from mlflow.models import infer_signature
from mlflow import sklearn
from sklearn.metrics import confusion_matrix, classification_report
import joblib
import pickle


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

ml_flow_config = {
  "uri": os.getenv('MLFLOW_TRACKING_URI'),
  "experiment_name": os.getenv('MLFLOW_EXPERIMENT_NAME')
}

REGISTERED_MODEL_NAME = "Best_XGBoost_Model"
MODEL_VERSION = "2"  # Load version 2 explicitly

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
logger.info("📦 MLFlow Configuration:")
logger.info(f"  MLFlow URI: {ml_flow_config['uri']}")
logger.info(f"  MLFlow Experiment Name: {ml_flow_config['experiment_name']}")

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
  dag_id='load_and_test_best_model',
  description='Load the best model from MLFlow and test it with data from Redis',
  default_args=default_args,
  schedule='@daily',
  catchup=False
) as dag:

  @task
  def load_model_from_mlflow_and_test():
    # Load data from Redis and test the best model from MLFlow
    logger.info("Starting the process to load model from MLFlow and test it with data from Redis")
    try:
      redis_client = redis.Redis(host=redis_config['host'], port=redis_config['port'], decode_responses=False)
      redis_client.ping()
      logger.info("✅ Redis connection successful")
      # Fetch the final dataset from Redis
      logger.info(f"Fetching final dataset from Redis with key: {model_train_config['redis_key']['final_dataset_key']}")

      # Check if the key exists in Redis
      if not redis_client.exists(model_train_config['redis_key']['final_dataset_key']):
        logger.error(f"❌ Redis key '{model_train_config['redis_key']['final_dataset_key']}' does not exist.")

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
        return
    except Exception as e:
      logger.error(f"❌ Error loading data from Redis: {e}")

    try:
      if ml_flow_config['uri'] is None:
        logger.error("❌ MLFlow tracking URI is not set in environment variables")
        raise ValueError("MLFlow tracking URI is required")
      
      mlflow.set_tracking_uri(ml_flow_config['uri'])
      mlflow.set_experiment('Load and Test Best Model Experiment_' + datetime.now().strftime("%Y-%m-%d"))
      logger.info(f"✅ MLFlow tracking URI set to: {ml_flow_config['uri']}")
      logger.info(f"✅ MLFlow experiment name set to: Load and Test Best Model Experiment")

      # Load the best model from MLFlow
      model_uri = f"models:/{REGISTERED_MODEL_NAME}/{MODEL_VERSION}"
      logger.info(f"Loading model from MLFlow with URI: {model_uri}")
      model = mlflow.pyfunc.load_model(model_uri)
      logger.info(f"✅ Model loaded from MLFlow with URI: {model_uri}")

      # Configure Model Trainer
      config = ConfigurationManager(
        config_file_path=CONFIG_FILE_PATH,
        params_file_path=PARAMS_FILE_PATH,
        schema_file_path=SCHEMA_FILE_PATH
      ).get_model_trainer_config()

      logger.info("Initialized Config Manager for Model Trainer")

      # Initialize Model Trainer
      model_trainer = ModelTrainer(config=config)

      # Split the DataFrame into features and target
      X_all, y_all = model_trainer.split_data(df)

      # Split the data into training and testing sets
      X_train, X_test, y_train, y_test = model_trainer.split_data_train__test(X_all, y_all)

      # Log the training and testing data shapes
      logger.info(f"Training data shape: {X_train.shape}, Testing data shape: {X_test.shape}")
      logger.info(f"Training target shape: {y_train.shape}, Testing target shape: {y_test.shape}")

      # Encode the target variable
      y_train_encoded, y_test_encoded = model_trainer.encode_variable(y_train, y_test)

      # Set inference signature for the best model
      signature = infer_signature(X_train, y_train_encoded)

      # Set the MLFlow tracking URI and experiment name
      if ml_flow_config['uri']:
        mlflow.set_tracking_uri(ml_flow_config['uri'])
        mlflow.set_experiment(ml_flow_config['experiment_name'])
      else:
        logger.warning("MLFlow tracking URI is not set, using default")

      with mlflow.start_run(run_name="Model_Testing"):
        mlflow.log_param("model_name", config.model_name)
        mlflow.log_param("train_data_path", config.train_data_path)
        mlflow.log_param("target_column", config.target_column)

        # Make predictions on test data
        y_test_pred = model.predict(X_test)
        
        # Find the F1 score of the best model
        train_f1, train_accuracy = model_trainer.predict_labels(model, X_train, y_train_encoded)
        test_f1, test_accuracy = model_trainer.predict_labels(model, X_test, y_test_encoded)

        logger.info(f"Train F1 Score: {train_f1}, Train Accuracy: {train_accuracy}")
        logger.info(f"Test F1 Score: {test_f1}, Test Accuracy: {test_accuracy}")

        # Mlflow metrics logging
        mlflow.log_metric("train_f1_score", float(train_f1))
        mlflow.log_metric("train_accuracy", float(train_accuracy))
        mlflow.log_metric("test_f1_score", float(test_f1))
        mlflow.log_metric("test_accuracy", float(test_accuracy))

        logger.info("Model testing completed successfully")

        # Generate confusion matrix and classification report
        cm = confusion_matrix(y_test_encoded, y_test_pred)
        cr = classification_report(y_test_encoded, y_test_pred)

        logger.info(f"Confusion Matrix:\n{cm}")
        logger.info(f"Classification Report:\n{cr}")

        # Log confusion matrix and classification report to MLFlow
        mlflow.log_text(str(cm), "confusion_matrix.txt")
        mlflow.log_text(str(cr), "classification_report.txt")

        # Log the Model Signature
        mlflow.log_param("model_signature", str(signature))

    except Exception as e:
      logger.error(f"❌ Error loading model from MLFlow: {e}")

  # Task Definition
  load_model_and_test = load_model_from_mlflow_and_test()