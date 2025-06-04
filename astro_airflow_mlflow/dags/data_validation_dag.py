# Here, we will write the data validation DAG for Airflow.
# Once the Data Ingestion is Completed we will trigger the Data Validation DAG.

from datetime import timedelta, datetime
from airflow import DAG
from airflow.decorators import task
from src import src_logger as logger
from src.pipeline.data_validation_pipeline import DataValidationPipeline

# Define the default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
with DAG(
    'data_validation_dag',
    default_args=default_args,
    description='DAG for data validation',
    schedule=timedelta(days=1),
    start_date=datetime(2023, 10, 1),
) as dag:

    @task
    def data_validation_task():
        """
        Task to perform data validation.
        """
        logger.info("Starting data validation task")
        try:
            obj = DataValidationPipeline()
            obj.main()
            logger.info("Data validation completed successfully")
        except Exception as e:
            logger.error(f"Error in data validation task: {e}")
            raise e

    # Define the task in the DAG
    validate_data = data_validation_task()