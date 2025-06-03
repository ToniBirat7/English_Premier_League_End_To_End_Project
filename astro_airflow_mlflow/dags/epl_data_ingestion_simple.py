"""
## EPL Data Ingestion DAG - Simplified Version

This DAG performs data ingestion for the English Premier League ML pipeline
using a simplified approach that avoids complex object serialization.
"""

from airflow.decorators import dag, task
from datetime import datetime, timedelta
import sys
import os

# Add project root to path
sys.path.insert(0, '/usr/local/airflow')

# Import after adding to path
from src import src_logger as logger


@dag(
    dag_id='epl_data_ingestion_simple',
    start_date=datetime(2023, 10, 1),
    schedule="@daily",
    catchup=False,
    default_args={
        'owner': 'EPL_Team',
        'depends_on_past': False,
        'retries': 2,
        'retry_delay': timedelta(minutes=5),
    },
    tags=['epl', 'data', 'ingestion', 'pipeline'],
    doc_md=__doc__
)
def epl_data_ingestion_pipeline():
    """
    Simplified EPL Data Ingestion Pipeline
    """
    
    @task
    def validate_environment():
        """
        Validate that all required files and directories are available.
        """
        logger.info("🔍 Validating environment for data ingestion...")
        
        # Check for required files
        required_files = [
            '/usr/local/airflow/config/config.yaml',
            '/usr/local/airflow/params.yaml',
            '/usr/local/airflow/schema.yaml',
        ]
        
        for file_path in required_files:
            if os.path.exists(file_path):
                logger.info(f"✅ Found: {file_path}")
            else:
                logger.warning(f"⚠️  Missing: {file_path}")
        
        # Check for dataset
        dataset_paths = [
            '/usr/local/airflow/Datasets/final_dataset.csv',
            'Datasets/final_dataset.csv'
        ]
        
        dataset_found = False
        for dataset_path in dataset_paths:
            if os.path.exists(dataset_path):
                logger.info(f"✅ Found dataset: {dataset_path}")
                dataset_found = True
                break
        
        if not dataset_found:
            logger.warning("⚠️  Dataset not found in expected locations")
        
        logger.info("🎉 Environment validation completed")
        return {"status": "validated", "dataset_available": dataset_found}
    
    @task
    def initialize_config():
        """
        Initialize configuration and return paths as simple dictionary.
        """
        logger.info("⚙️  Initializing configuration...")
        
        try:
            from src.constants import CONFIG_FILE_PATH, PARAMS_FILE_PATH, SCHEMA_FILE_PATH
            from src.config.configuration import ConfigurationManager
            
            logger.info("📋 Creating configuration manager...")
            config_manager = ConfigurationManager(
                config_file_path=CONFIG_FILE_PATH,
                params_file_path=PARAMS_FILE_PATH,
                schema_file_path=SCHEMA_FILE_PATH,
            )
            
            config = config_manager.get_data_ingestion_config()
            
            # Convert to simple dictionary for safe serialization
            config_dict = {
                'dataset_path': str(config.dataset_path),
                'root_dir': str(config.root_dir),
                'ingestion_dir': str(config.ingestion_dir),
                'ingestion_path': str(config.ingestion_path)
            }
            
            logger.info(f"✅ Configuration initialized: {config_dict}")
            return config_dict
            
        except Exception as e:
            logger.error(f"❌ Configuration initialization failed: {str(e)}")
            # Return a fallback configuration
            fallback_config = {
                'dataset_path': 'Datasets/final_dataset.csv',
                'root_dir': 'artifacts',
                'ingestion_dir': 'artifacts/data_ingestion',
                'ingestion_path': 'final_dataset.csv'
            }
            logger.info(f"🔄 Using fallback configuration: {fallback_config}")
            return fallback_config
    
    @task
    def perform_data_ingestion(config_dict: dict):
        """
        Perform the actual data ingestion using the configuration.
        """
        logger.info("📊 Starting data ingestion process...")
        logger.info(f"🔧 Using configuration: {config_dict}")
        
        try:
            import pandas as pd
            import shutil
            
            # Read the dataset
            dataset_path = config_dict['dataset_path']
            logger.info(f"📖 Reading dataset from: {dataset_path}")
            
            if not os.path.exists(dataset_path):
                raise FileNotFoundError(f"Dataset not found: {dataset_path}")
            
            df = pd.read_csv(dataset_path)
            logger.info(f"✅ Dataset loaded successfully!")
            logger.info(f"📏 Data shape: {df.shape}")
            logger.info(f"📝 Columns: {list(df.columns)}")
            
            # Prepare output directory
            ingestion_dir = config_dict['ingestion_dir']
            ingestion_path = config_dict['ingestion_path']
            
            logger.info(f"📁 Creating output directory: {ingestion_dir}")
            os.makedirs(ingestion_dir, exist_ok=True)
            
            # Create full output path
            output_path = os.path.join(ingestion_dir, ingestion_path)
            
            # Remove if it's a directory (fix for the previous issue)
            if os.path.isdir(output_path):
                logger.warning(f"🗑️  Removing existing directory: {output_path}")
                shutil.rmtree(output_path)
            
            # Save the dataset
            logger.info(f"💾 Saving dataset to: {output_path}")
            df.to_csv(output_path, index=False)
            
            # Verify the file was created
            if os.path.exists(output_path) and os.path.isfile(output_path):
                file_size = os.path.getsize(output_path)
                logger.info(f"✅ Dataset saved successfully!")
                logger.info(f"📊 File size: {file_size} bytes")
                
                return {
                    'status': 'success',
                    'output_path': output_path,
                    'rows': len(df),
                    'columns': len(df.columns),
                    'file_size': file_size
                }
            else:
                raise Exception(f"Failed to create output file: {output_path}")
                
        except Exception as e:
            logger.error(f"❌ Data ingestion failed: {str(e)}")
            import traceback
            logger.error(f"📄 Traceback: {traceback.format_exc()}")
            raise
    
    @task
    def log_completion(validation_result: dict, ingestion_result: dict):
        """
        Log the completion of the data ingestion pipeline.
        """
        logger.info("🎉 Data Ingestion Pipeline Completed!")
        logger.info(f"📋 Validation: {validation_result}")
        logger.info(f"📊 Ingestion: {ingestion_result}")
        
        if ingestion_result['status'] == 'success':
            logger.info("✅ All tasks completed successfully!")
            logger.info(f"📁 Dataset available at: {ingestion_result['output_path']}")
            logger.info(f"📊 Processed {ingestion_result['rows']} rows with {ingestion_result['columns']} columns")
        else:
            logger.error("❌ Pipeline completed with errors")
        
        return {"pipeline_status": "completed", "success": ingestion_result['status'] == 'success'}
    
    # Define task dependencies
    env_validation = validate_environment()
    config = initialize_config()
    ingestion_result = perform_data_ingestion(config)
    completion = log_completion(env_validation, ingestion_result)
    
    # Set dependencies
    env_validation >> config >> ingestion_result >> completion


# Instantiate the DAG
epl_data_ingestion_pipeline()
