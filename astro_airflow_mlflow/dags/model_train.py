# First well need to connect to MariaDB to fetch the data

# We will create the data transformation DAG for Airflow.

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
    dag_id='model_train',
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

            return final_dataset_path

        except Exception as e:
            logger.error(f"Error during data loading and transformation: {e}")
        finally:
            connection.close()
            logger.info("Database connection closed.")
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

        df = None
        # Load data from Redis
        try:
            redis_client = redis.Redis(host=redis_config['host'], port=redis_config['port'], decode_responses=False)
            redis_client.ping()
            logger.info("✅ Redis connection successful")
            # Fetch the final dataset from Redis
            logger.info(f"Fetching final dataset from Redis with key: {model_train_config['redis_key']['final_dataset_key']}")

            # Check if the key exists in Redis
            if not redis_client.exists(model_train_config['redis_key']['final_dataset_key']):
                logger.error(f"❌ Redis key '{model_train_config['redis_key']['final_dataset_key']}' does not exist.")
            # logger.info(f"✅ Redis key '{model_train_config['redis_key']['final_dataset_key']}' exists. Proceeding to load data.")

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

            # Configure Model Trainer
            config = ConfigurationManager(
                config_file_path=CONFIG_FILE_PATH,
                params_file_path=PARAMS_FILE_PATH,
                schema_file_path=SCHEMA_FILE_PATH
            ).get_model_trainer_config()

            logger.info("Initialized Config Manager for Model Trainer")

            # Initialize Model Trainer
            model_trainer = ModelTrainer(config=config)

            # Get all the visualizations
            if df is not None:
                logger.info("Starting data visualization")
                plots_created = model_trainer.get_visualized_data(df)
                if plots_created is not None:
                    logger.info(f"Data visualization completed with {len(plots_created)} plots created.")
                else:
                    logger.warning("⚠️ No plots were created during visualization")
            else:
                logger.error("❌ DataFrame is None, cannot proceed with visualization")

           # Log those visualizations to MLFlow
            logger.info("Logging visualizations to MLFlow")

            if ml_flow_config['uri']:
                mlflow.set_tracking_uri(ml_flow_config['uri'])
            else:
                logger.warning("MLFlow tracking URI is not set, using default")

            if ml_flow_config['experiment_name']:
                mlflow.set_experiment(ml_flow_config['experiment_name'])
            else:
                logger.warning("MLFlow experiment name is not set, using default")
            
            with mlflow.start_run(run_name="Model_Training_Visualizations"):
                # Log Dummy parameters for the run
                mlflow.log_param("model_name", config.model_name)
                mlflow.log_param("model_params", config.model_params)
                mlflow.log_param("train_data_path", config.train_data_path)
                mlflow.log_param("target_column", config.target_column)
        except Exception as e:
            logger.error(f"❌ Error loading final dataset from Redis: {e}")
            return
        
    @task
    def load_data_from_redis_for_hyperparameter_tuning():
        logger.info("Loading data from Redis for hyperparameter tuning")

        # Load data from Redis
        try:
            redis_client = redis.Redis(host=redis_config['host'], port=redis_config['port'], decode_responses=False)
            redis_client.ping()
            logger.info("✅ Redis connection successful")
            # Fetch the final dataset from Redis
            logger.info(f"Fetching final dataset from Redis with key: {model_train_config['redis_key']['final_dataset_key']}")

            # Check if the key exists in Redis
            if not redis_client.exists(model_train_config['redis_key']['final_dataset_key']):
                logger.error(f"❌ Redis key '{model_train_config['redis_key']['final_dataset_key']}' does not exist.")
            # logger.info(f"✅ Redis key '{model_train_config['redis_key']['final_dataset_key']}' exists. Proceeding to load data.")

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
            
            with mlflow.start_run(run_name="Hyperparameter_Tuning"):
                
                # Perform hyperparameter tuning
                logger.info("Starting hyperparameter tuning")
                parameters = { 'learning_rate' : [0.1],
                     'n_estimators' : [40],
                     'max_depth': [3],
                     'min_child_weight': [3],
                     'gamma':[0.4],
                     'subsample' : [0.8],
                     'colsample_bytree' : [0.8],
                     'scale_pos_weight' : [1],
                     'reg_alpha':[1e-5]
                   }  
                grid_search = model_trainer.hyperparameter_tuning(X_train, y_train_encoded, parameters)

                mlflow.log_param("model_name", config.model_name)
                mlflow.log_param("model_params", config.model_params)
                mlflow.log_param("train_data_path", config.train_data_path)
                mlflow.log_param("target_column", config.target_column)

                best_model = grid_search.best_estimator_
                logger.info(f"Best model found: {best_model}")

                # Find the F1 score of the best model
                train_f1, train_accuracy = model_trainer.predict_labels(best_model, X_train, y_train_encoded)
                test_f1, test_accuracy = model_trainer.predict_labels(best_model, X_test, y_test_encoded)

                logger.info(f"Train F1 Score: {train_f1}, Train Accuracy: {train_accuracy}")
                logger.info(f"Test F1 Score: {test_f1}, Test Accuracy: {test_accuracy}")

                # Mlflow metrics logging
                mlflow.log_metric("train_f1_score", float(train_f1))
                mlflow.log_metric("train_accuracy", float(train_accuracy))
                mlflow.log_metric("test_f1_score", float(test_f1))
                mlflow.log_metric("test_accuracy", float(test_accuracy))

                # Mlflow log parameters
                for key, value in grid_search.best_params_.items():
                    mlflow.log_param(key, value)

                logger.info("Hyperparameter tuning completed successfully")

                # Confusion Matrix and Classification Report
                logger.info("Generating confusion matrix and classification report")
                y_test_pred = best_model.predict(X_test)

                cm = confusion_matrix(y_test_encoded, y_test_pred)
                cr = classification_report(y_test_encoded, y_test_pred)

                logger.info(f"Confusion Matrix:\n{cm}")
                logger.info(f"Classification Report:\n{cr}")

                # Log confusion matrix and classification report to MLFlow
                mlflow.log_text(str(cm), "confusion_matrix.txt")
                mlflow.log_text(str(cr), "classification_report.txt")

                # Log the Model Signature
                mlflow.log_param("model_signature", str(signature))

                # Log Model 
                print(f"Using local file system for model logging...")
                sklearn.log_model(
                    sk_model=best_model,
                    artifact_path="model",
                    signature=signature
                )
                logger.info("Model logged to MLFlow successfully")

                # Save the best model to the specified path
                model_save_dir = os.path.join(config.root_dir, config.model_path)
                model_save_path = os.path.join(model_save_dir, config.model_name)

                logger.info(f"Model save directory: {model_save_dir}")
                logger.info(f"Saving the best model to {model_save_path}")

                create_directories([model_save_dir])
                
                # Save the model with Pickle and Joblib
                try:
                    # Save the model using joblib
                    joblib.dump(best_model, model_save_path + '.joblib')
                    logger.info(f"Model saved successfully to {model_save_path}.joblib")
                    mlflow.log_artifact(model_save_path + '.joblib')

                    # Save the model using pickle
                    with open(model_save_path + '.pkl', 'wb') as f:
                        pickle.dump(best_model, f)
                    logger.info(f"Model saved successfully to {model_save_path}.pkl")
                    mlflow.log_artifact(model_save_path + '.pkl')
                except Exception as e:
                    logger.error(f"❌ Error saving model artifacts: {e}")

        except Exception as e:
            logger.error(f"❌ Error loading final dataset from Redis: {e}")
            return

    # Task Dependency
    load_and_transform_data_task = load_from_mariadb_save_the_final_dataset()
    save_to_redis_task = load_final_csv_file_and_save_to_redis(load_and_transform_data_task)
    load_data_from_redis_visualize_with_MLFlow()
    load_data_from_redis_for_hyperparameter_tuning()