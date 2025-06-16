"""
DAG for scraping Premier League data from API, storing in PostgreSQL, 
and then exporting to CSV in the Datasets folder
"""

from airflow import DAG
from datetime import datetime, timedelta
import os
import pandas as pd
import psycopg2
from psycopg2.extras import RealDictCursor
from pathlib import Path
from Scrapping_Scripts.web_scraper import PremierLeagueWebScraper

from airflow.decorators import task

from dotenv import load_dotenv

# Import project-specific modules
from src import src_logger as logger
from src.config.configuration import ConfigurationManager
from src.constants import *

load_dotenv()  # Load environment variables from .env file

# Define the default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# PostgreSQL config from environment variables or constants
postgres_config = {
    'host': os.getenv('POSTGRES_HOST', 'http://192.168.1.79:5434/'),
    'port': os.getenv('POSTGRES_PORT', '5434'),
    'user': os.getenv('POSTGRES_USER', 'postgres'),
    'password': os.getenv('POSTGRES_PASSWORD', 'postgres'),
    'database': os.getenv('POSTGRES_DATABASE', 'weekly_scrapped_data')
}

TABLE_NAME = "PREMIER_LEAGUE_MATCHES_4"  # Same as in web_scraper.py

# Define the DAG
with DAG(
    'scrape_store_as_csv_dag',
    default_args=default_args,
    description='DAG for scraping data, storing in PostgreSQL, and exporting to CSV',
    schedule=timedelta(days=1),  # Run daily
) as dag:

    @task
    def initialize_configuration_manager():
        """
        Task to initialize the configuration manager and return config as dict.
        """
        logger.info("Initializing configuration manager")
        config_manager = ConfigurationManager(
            config_file_path=CONFIG_FILE_PATH,
            params_file_path=PARAMS_FILE_PATH,
            schema_file_path=SCHEMA_FILE_PATH,
        )
        config = config_manager.get_data_ingestion_config()
        logger.info("Configuration manager initialized successfully")
        
        # Return config as a dictionary to avoid serialization issues
        config_dict = {
            'dataset_path': str(config.dataset_path),
            'root_dir': str(config.root_dir),
            'ingestion_dir': str(config.ingestion_dir)
        }
        logger.info(f"Configuration: {config_dict}")
        return config_dict

    @task
    def run_web_scraper():
        """
        Task to run the web scraper script to fetch data from API and store in PostgreSQL.
        """
        logger.info("Starting web scraper task")
        logger.info(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info(f"Target: 2024-25 Premier League Season")
        logger.info(f"Database: weekly_scrapped_data.db")
        logger.info("=" * 60)

        # Initialize scraper
        scraper = PremierLeagueWebScraper(db_table=TABLE_NAME)
        
        # Run scraping process
        success = scraper.run_scraper("2024-25")
        
        if success:
            logger.info("\n✅ Scraping completed successfully!")
            logger.info(f"✅ Data saved to PostgreSQL database '{scraper.db_config['database']}'")
            logger.info(f"✅ Table name: '{scraper.table_name}'")
            logger.info(f"✅ Database running on: {scraper.db_config['host']}:{scraper.db_config['port']}")
        else:
            logger.error("\n❌ Scraping failed. Check logs for details.")

        logger.info("=" * 60)

    @task
    def fetch_data_from_postgresql():
        """
        Task to fetch the complete data from PostgreSQL database.
        """
        logger.info("Starting task to fetch data from PostgreSQL")
        
        conn = None
        
        try:
            # Connect to PostgreSQL
            logger.info(f"Connecting to PostgreSQL: {postgres_config['host']}:{postgres_config['port']}/{postgres_config['database']}")
            conn = psycopg2.connect(
                host=postgres_config['host'],
                port=postgres_config['port'],
                user=postgres_config['user'],
                password=postgres_config['password'],
                database=postgres_config['database']
            )
            
            # Use RealDictCursor to get column names
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            # Query to get all data from the table
            query = f"SELECT * FROM {TABLE_NAME} ORDER BY DT, HT, AT"
            
            logger.info(f"Executing query: {query}")
            cursor.execute(query)
            
            # Fetch all rows
            rows = cursor.fetchall()
            
            if not rows:
                logger.warning("No data found in PostgreSQL table")
                return None
                
            logger.info(f"Retrieved {len(rows)} rows from PostgreSQL")

            # Log the first few rows for debugging
            logger.info("Sample data from PostgreSQL:")
            for row in rows[:5]:  # Log first 5 rows
                logger.info(row)  
            
            # Convert to pandas DataFrame
            df = pd.DataFrame(rows)

            logger.info("Data successfully fetched from PostgreSQL")
            logger.info(f"DataFrame shape: {df.shape}")
            logger.info(f"DataFrame columns: {df.columns.tolist()}")
            logger.info(f"DataFrame head:\n{df.head()}")
            logger.info(f"DataFrame info:\n{df.info()}")
            logger.info(f"DataFrame dtypes:\n{df.dtypes}")
            
            # Return DataFrame as a dictionary for serialization in Airflow
            return df.to_dict()
            
        except Exception as e:
            logger.error(f"Error fetching data from PostgreSQL: {e}")
            raise
        finally:
            if 'conn' in locals() and conn:
                conn.close()
                logger.info("PostgreSQL connection closed")

    @task
    def convert_to_csv_and_save(data_dict, config_dict):
        """
        Task to convert data to CSV and save to the Datasets folder.
        """
        if not data_dict:
            logger.warning("No data to convert to CSV")
            return None
            
        try:
            # Convert dictionary back to DataFrame
            logger.info("Converting data to DataFrame")
            df = pd.DataFrame.from_dict(data_dict)
            
            # Generate filename with date and time
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"premier_league_data_{timestamp}.csv"
            
            # Get dataset path from config
            dataset_path = config_dict['dataset_path']
            
            # Check if the existing path exists, if not create it
            logger.info(f"Ensuring dataset path exists: {dataset_path}")
            # Ensure the path exists
            Path(dataset_path).mkdir(parents=True, exist_ok=True)
            
            # Full path for the CSV file
            csv_path = os.path.join(dataset_path, filename)
            
            logger.info(f"Saving data to CSV: {csv_path}")
            
            # Save DataFrame to CSV, format it for pandas read_csv
            df.to_csv(csv_path, index=False, encoding='utf-8')
            
            logger.info(f"Data successfully saved to CSV: {csv_path}")
            return csv_path
            
        except Exception as e:
            logger.error(f"Error converting data to CSV: {e}")
            raise

    @task
    def log_csv_file_path(csv_path):
        """
        Task to log the CSV file path.
        """
        if csv_path:
            logger.info(f"CSV file created: {csv_path}")
            
            # Get file size
            file_size = os.path.getsize(csv_path)
            logger.info(f"CSV file size: {file_size / 1024:.2f} KB")
            
            # Get row count
            try:
                row_count = sum(1 for _ in open(csv_path)) - 1  # Subtract header
                logger.info(f"CSV row count: {row_count}")
            except Exception as e:
                logger.warning(f"Could not count rows: {e}")
        else:
            logger.warning("No CSV file was created")

    # Define the task dependencies
    config = initialize_configuration_manager()
    scraper_success = run_web_scraper()
    postgresql_data = fetch_data_from_postgresql()
    csv_path = convert_to_csv_and_save(postgresql_data, config)
    log_csv_file_path(csv_path)