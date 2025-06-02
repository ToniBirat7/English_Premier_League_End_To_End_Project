# Main entry point for the project

from src import src_logger as logger
from src.pipeline.data_ingestion_pipeline import DataIngestionTrainingPipeline

logger.info("Starting the Data Ingestion Pipeline...")
try:
    ingestion_pipeline = DataIngestionTrainingPipeline()
    ingestion_pipeline.main()
    logger.info("Data Ingestion Pipeline completed successfully.")
except Exception as e:
    logger.error(f"An error occurred during the Data Ingestion Pipeline execution: {str(e)}")
    raise e
logger.info("Data Ingestion Pipeline execution finished.")

