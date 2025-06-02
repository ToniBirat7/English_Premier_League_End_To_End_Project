"""
## Simple Airflow Test DAG

This is a minimal DAG to test if Airflow is working correctly.
It only uses basic Python logging and doesn't require any external dependencies.
"""

import logging
from airflow.decorators import dag, task
from pendulum import datetime


# Set up basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dag(
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=False,
    doc_md=__doc__,
    default_args={"owner": "EPL_Team", "retries": 2},
    tags=["epl", "test", "simple"],
)
def simple_airflow_test():
    """
    Simple Airflow Test DAG
    """
    
    @task
    def test_basic_logging():
        """
        Test basic Python logging functionality.
        """
        logger.info("🚀 Simple Airflow Test DAG - Starting basic logging test")
        logger.info("✅ Basic Python logging is working correctly")
        logger.info("🎯 EPL ML Pipeline - Airflow environment is functional")
        
        return {"status": "success", "message": "Basic logging test completed"}
    
    @task
    def test_dag_execution():
        """
        Test DAG execution and task dependencies.
        """
        logger.info("🔄 Testing DAG execution flow")
        logger.info("📊 Task dependencies are working correctly")
        logger.info("🎉 Simple Airflow test completed successfully")
        
        return {"status": "completed", "message": "DAG execution test passed"}
    
    # Define task dependencies
    basic_test = test_basic_logging()
    execution_test = test_dag_execution()
    
    basic_test >> execution_test


# Instantiate the DAG
simple_airflow_test()
