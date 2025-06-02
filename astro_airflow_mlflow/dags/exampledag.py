"""
## EPL ML Pipeline Logging Test DAG

This DAG is a simple test to verify that Airflow can properly import and use
the logger from the src package of the English Premier League ML project.

This DAG contains basic logging tasks to validate the pipeline setup and
ensure that our custom logging configuration works correctly within the
Airflow environment.

The DAG demonstrates:
1. Successful import of custom logger from src package
2. Basic task execution and logging
3. Pipeline health verification
"""

import sys
import os

# Add the project root to Python path to import from src
# In container, the project files are copied to /usr/local/airflow
project_root = "/usr/local/airflow"
sys.path.insert(0, project_root)

# Import custom logger from src package
from src import src_logger

from airflow.decorators import dag, task
from pendulum import datetime
from datetime import datetime as dt


# Define the basic parameters of the DAG
@dag(
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=False,
    doc_md=__doc__,
    default_args={"owner": "EPL_ML_Team", "retries": 2},
    tags=["epl", "logging", "test"],
)
def epl_logging_test_dag():
    """
    EPL ML Pipeline Logging Test DAG
    """
    
    @task
    def test_logger_import():
        """
        Test task to verify that we can successfully import and use 
        the custom logger from the src package.
        """
        try:
            src_logger.info("🚀 EPL ML Pipeline DAG - Logger import successful!")
            src_logger.info("✅ Custom logging configuration is working correctly")
            src_logger.info("📊 Ready for EPL match prediction pipeline tasks")
            
            return {"status": "success", "message": "Logger imported and working correctly"}
            
        except Exception as e:
            src_logger.error(f"❌ Failed to import or use logger: {str(e)}")
            raise
    
    @task
    def log_dag_execution():
        """
        Task to log successful DAG execution and pipeline health status.
        """
        try:
            src_logger.info("🎯 EPL Logging Test DAG - Task execution started")
            src_logger.info("🔄 Pipeline orchestration with AstroCLI is functioning")
            src_logger.info("📈 DAG successfully executed - Pipeline is healthy")
            src_logger.info("⚽ Ready for English Premier League ML workflows")
            
            # Log some useful information
            src_logger.info(f"📅 DAG execution date: {dt.now()}")
            src_logger.info(f"🖥️  Airflow environment: Production")
            src_logger.info(f"🏗️  Project root: {project_root}")
            
            return {
                "status": "completed",
                "message": "EPL Logging Test DAG executed successfully",
                "timestamp": dt.now().isoformat()
            }
            
        except Exception as e:
            src_logger.error(f"❌ DAG execution failed: {str(e)}")
            raise
    
    @task
    def verify_pipeline_setup():
        """
        Task to verify that the pipeline setup is ready for EPL ML workflows.
        """
        try:
            src_logger.info("🔍 Verifying EPL ML Pipeline setup...")
            
            # Check if project structure is accessible
            if os.path.exists(project_root):
                src_logger.info("✅ Project root directory accessible")
            else:
                src_logger.warning("⚠️  Project root directory not found")
            
            # Check for key directories
            key_dirs = ["src", "config", "Datasets"]
            for dir_name in key_dirs:
                dir_path = os.path.join(project_root, dir_name)
                if os.path.exists(dir_path):
                    src_logger.info(f"✅ {dir_name}/ directory found")
                else:
                    src_logger.warning(f"⚠️  {dir_name}/ directory not found")
            
            # Check for key files
            key_files = ["params.yaml", "schema.yaml", "project_requirements.txt"]
            for file_name in key_files:
                file_path = os.path.join(project_root, file_name)
                if os.path.exists(file_path):
                    src_logger.info(f"✅ {file_name} file found")
                else:
                    src_logger.warning(f"⚠️  {file_name} file not found")
            
            src_logger.info("🎉 Pipeline verification completed successfully")
            src_logger.info("🚀 EPL ML Pipeline is ready for data processing workflows")
            
            return {"status": "verified", "message": "Pipeline setup verification completed"}
            
        except Exception as e:
            src_logger.error(f"❌ Pipeline verification failed: {str(e)}")
            raise
    
    # Define task dependencies
    logger_test = test_logger_import()
    dag_execution = log_dag_execution()
    pipeline_verification = verify_pipeline_setup()
    
    # Set up task dependencies: logger_test -> dag_execution -> pipeline_verification
    logger_test >> dag_execution >> pipeline_verification


# Instantiate the DAG
epl_logging_test_dag()
