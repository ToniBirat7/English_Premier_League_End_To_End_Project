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
    'host': os.getenv('POSTGRES_HOST', 'host.docker.internal'),  # Use host.docker.internal to access host from container
    'port': os.getenv('POSTGRES_PORT', '5434'),
    'user': os.getenv('POSTGRES_USER', 'postgres'),
    'password': os.getenv('POSTGRES_PASSWORD', 'postgres'),
    'database': os.getenv('POSTGRES_DATABASE', 'weekly_scrapped_data')
}

# Api configuration 
api_config = {
    'base_url': os.getenv('base_url', 'http://host.docker.internal:3000'),  # Use host.docker.internal
    'api_url': os.getenv('api_url', 'http://host.docker.internal:8000/api')  # Use host.docker.internal
}

TABLE_NAME = "PREMIER_LEAGUE_MATCHES_5"  # Using existing table in the database

# Log the PostgreSQL configuration
logger.info(f"PostgreSQL Config: {postgres_config}")

# Log the API configuration
logger.info(f"API Config: {api_config}")

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
    def run_web_scraper(api_accessible=None):
        """
        Task to run the web scraper script to fetch data from API and store in PostgreSQL.
        Includes fallback to sample data generation if API is not accessible.
        """
        logger.info("Starting web scraper task")
        logger.info(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info(f"Target: 2024-25 Premier League Season")
        logger.info(f"Database: weekly_scrapped_data.db")
        logger.info("=" * 60)

        # Log whether API is accessible based on previous task
        if api_accessible is False:
            logger.warning("API was found to be inaccessible in the connectivity check task")
            logger.warning("Will rely on fallback mechanism in the scraper")
        
        # Initialize scraper with custom error handling
        try:
            scraper = PremierLeagueWebScraper(
                db_table=TABLE_NAME, 
                base_url=api_config['base_url'], 
                api_url=api_config['api_url'], 
                db_config=postgres_config
            )
            
            # Run scraping process
            success = scraper.run_scraper("2024-25")
            
            if success:
                logger.info("\n✅ Scraping completed successfully!")
                # Check if db_config is available before logging
                if hasattr(scraper, 'db_config') and scraper.db_config:
                    logger.info(f"✅ Data saved to PostgreSQL database '{scraper.db_config.get('database', 'weekly_scrapped_data')}'")
                    logger.info(f"✅ Table name: '{scraper.table_name}'")
                    logger.info(f"✅ Database running on: {scraper.db_config.get('host', 'localhost')}:{scraper.db_config.get('port', '5434')}")
                else:
                    logger.info(f"✅ Data saved to PostgreSQL database using default connection")
                    logger.info(f"✅ Table name: '{scraper.table_name}'")
                    logger.info(f"✅ Database running on: {postgres_config.get('host', 'localhost')}:{postgres_config.get('port', '5434')}")
                return True
            else:
                logger.warning("\n⚠️ Scraping did not find any data but completed without errors.")
                logger.info("=" * 60)
                # Even if no data was scraped, we'll continue the pipeline
                # The next tasks will handle the case where no data is available
                return False
                
        except Exception as e:
            logger.error(f"\n❌ Scraping failed with error: {e}")
            logger.error("=" * 60)
            # Return False but don't raise exception to allow the pipeline to continue
            # The next tasks will handle the case where no data is available
            return False

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
                database=postgres_config['database'],
                # Add timeout to avoid hanging
                connect_timeout=10
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
                # Return empty DataFrame as dict
                empty_df = pd.DataFrame()
                return empty_df.to_dict()
                
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
            
            # Convert datetime/timestamp columns to strings to prevent serialization errors
            for col in df.columns:
                # Check if column contains datetime-like objects
                if pd.api.types.is_datetime64_any_dtype(df[col]) or df[col].dtype == 'object' and df[col].notna().any() and isinstance(df[col].iloc[0], (pd.Timestamp, datetime)):
                    logger.info(f"Converting datetime column {col} to string format")
                    df[col] = df[col].astype(str)
                # Handle date objects specifically
                elif df[col].dtype == 'object' and df[col].notna().any() and hasattr(df[col].iloc[0], 'strftime'):
                    logger.info(f"Converting date column {col} to string format")
                    df[col] = df[col].apply(lambda x: x.strftime('%Y-%m-%d') if x is not None else None)
            
            logger.info("All datetime columns converted to strings for XCom compatibility")
            
            # Return DataFrame as a dictionary for serialization in Airflow
            return df.to_dict()
            
        except Exception as e:
            logger.error(f"Error fetching data from PostgreSQL: {e}")
            # Return empty DataFrame as dict instead of raising exception
            # This allows the DAG to continue running
            empty_df = pd.DataFrame()
            logger.info("Returning empty DataFrame as dict due to error")
            return empty_df.to_dict()
        finally:
            if conn:
                conn.close()
                logger.info("PostgreSQL connection closed")

    @task
    def convert_to_csv_and_save(data_dict, config_dict):
        """
        Task to convert data to CSV and save to the Datasets folder.
        """
        logger.info("Starting task to convert data to CSV and save to the Datasets folder")
        
        try:
            # Convert dictionary back to DataFrame
            logger.info("Converting data to DataFrame")
            df = pd.DataFrame.from_dict(data_dict)
            
            # Make sure all timestamp/datetime columns remain as strings
            # This handles any columns that might be automatically converted back to datetime
            for col in df.columns:
                if pd.api.types.is_datetime64_any_dtype(df[col]) or (df[col].dtype == 'object' and df[col].notna().any() and hasattr(df[col].iloc[0], 'strftime')):
                    logger.info(f"Ensuring column {col} remains as string format")
                    df[col] = df[col].astype(str)
            
            # Check if the DataFrame is empty
            if df.empty:
                logger.warning("DataFrame is empty. No data to convert to CSV.")
                logger.warning("Creating a minimal sample CSV file to maintain pipeline integrity.")
                
                # Create a minimal sample DataFrame with placeholder data
                logger.info("Creating a placeholder DataFrame with explanation row")
                placeholder_data = {
                    'Date': [datetime.now().strftime('%Y-%m-%d')],
                    'HomeTeam': ["NO_DATA_AVAILABLE"],
                    'AwayTeam': ["API_CONNECTION_FAILED"],
                    'FTR': ["N/A"],
                    'SEASON': ["2024-25"]
                }
                df = pd.DataFrame(placeholder_data)
                
                logger.info("Created a placeholder DataFrame with explanation row")
            
            # Generate filename with date and time
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"premier_league_data_scrapped_data.csv"
            
            # Get dataset path from config
            dataset_path = config_dict['dataset_path']
            
            # Check if the existing path exists, if not create it
            logger.info(f"Ensuring dataset path exists: {dataset_path}")
            # Ensure the path exists
            Path(dataset_path).mkdir(parents=True, exist_ok=True)
            
            # Full path for the CSV file
            csv_path = os.path.join(dataset_path, filename)
            
            # Rename columns to match expected format
            logger.info("Renaming columns to match expected format")
            # Create a column mapping dictionary
            column_mapping = {
                'dt': 'Date',
                'ht': 'HomeTeam',
                'at': 'AwayTeam',
                'fthg': 'FTHG',
                'ftag': 'FTAG',
                'ftr': 'FTR'
            }
            
            # For all other columns, capitalize them
            for col in df.columns:
                if col not in column_mapping:
                    # Handle special case for 'as_' column
                    if col == 'as_':
                        column_mapping[col] = 'AS'
                    else:
                        column_mapping[col] = col.upper()
            
            # Rename the columns
            df = df.rename(columns=column_mapping)
            logger.info(f"Columns after renaming: {df.columns.tolist()}")
            
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

    @task
    def check_api_connectivity():
        """
        Task to check if the API is accessible before attempting to scrape data.
        """
        import requests
        from requests.exceptions import RequestException
        
        logger.info(f"Checking API connectivity to: {api_config['api_url']}")
        
        # Remove any trailing whitespace from the URL
        api_url = api_config['api_url'].strip()
        
        try:
            # Test the base API URL
            response = requests.get(
                api_url, 
                timeout=10,
                headers={
                    'User-Agent': 'Airflow-API-Check/1.0',
                    'Accept': 'application/json'
                }
            )
            
            if response.status_code == 200:
                logger.info(f"✅ API is accessible! Status code: {response.status_code}")
                
                # Try to access the matches
                try:
                    data = response.json()
                    if isinstance(data, dict) and data.get('message') == 'Welcome to the Premier League API':
                        logger.info("✅ API response looks valid")
                    else:
                        logger.info(f"API response content: {data}")
                    return True
                except Exception as e:
                    logger.warning(f"⚠️ API is accessible but returned invalid JSON: {e}")
                    logger.warning(f"Response content: {response.text[:200]}...")
                    return False
            else:
                logger.warning(f"⚠️ API returned status code {response.status_code}")
                logger.warning(f"Response content: {response.text[:200]}...")
                return False
                
        except RequestException as e:
            logger.error(f"❌ API connectivity check failed: {e}")
            return False
        except Exception as e:
            logger.error(f"❌ Unexpected error during API connectivity check: {e}")
            return False

    # Define the task dependencies
    config = initialize_configuration_manager()
    api_accessible = check_api_connectivity()
    scraper_success = run_web_scraper(api_accessible)
    data = fetch_data_from_postgresql()
    csv_path = convert_to_csv_and_save(data, config)
    log_csv_file_path(csv_path)