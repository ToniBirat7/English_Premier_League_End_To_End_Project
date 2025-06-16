#!/usr/bin/env python3
"""
Test script to load Premier League match data from PostgreSQL and display as DataFrame
"""

import pandas as pd
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv
import sys
from tabulate import tabulate

# Load environment variables from .env file if present
load_dotenv()

def load_postgres_data():
    """
    Connect to PostgreSQL, load data from the match table, and return as DataFrame
    """
    # PostgreSQL connection parameters
    postgres_config = {
        'host': os.getenv('POSTGRES_HOST', 'localhost'),
        'port': os.getenv('POSTGRES_PORT', '5434'),
        'user': os.getenv('POSTGRES_USER', 'postgres'),
        'password': os.getenv('POSTGRES_PASSWORD', 'postgres'),
        'database': os.getenv('POSTGRES_DATABASE', 'weekly_scrapped_data')
    }
    
    table_name = "PREMIER_LEAGUE_MATCHES_4"
    conn = None
    
    try:
        # Connect to PostgreSQL
        print(f"Connecting to PostgreSQL: {postgres_config['host']}:{postgres_config['port']}/{postgres_config['database']}")
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
        query = f"SELECT * FROM {table_name} ORDER BY DT, HT, AT"
        
        print(f"Executing query: {query}")
        cursor.execute(query)
        
        # Fetch all rows
        rows = cursor.fetchall()
        
        if not rows:
            print("No data found in PostgreSQL table")
            return None
            
        print(f"Retrieved {len(rows)} rows from PostgreSQL")
        
        # Convert to pandas DataFrame
        df = pd.DataFrame(rows)
        return df
        
    except Exception as e:
        print(f"Error fetching data from PostgreSQL: {e}")
        return None
    finally:
        if conn:
            conn.close()
            print("PostgreSQL connection closed")

def analyze_dataframe(df):
    """Display basic DataFrame analysis"""
    if df is None or df.empty:
        print("No data to analyze")
        return
    
    print("\n=== DataFrame Information ===")
    print(f"Shape: {df.shape}")
    print("\n=== Column Names ===")
    print(df.columns.tolist())
    
    print("\n=== Data Types ===")
    print(df.dtypes)
    
    print("\n=== Statistics Summary ===")
    print(df.describe().to_string())
    
    print("\n=== Sample Data (first 5 rows) ===")
    try:
        # Try to use tabulate for pretty printing if available
        if 'tabulate' in sys.modules:
            print(tabulate(df.head(), headers='keys', tablefmt='pretty'))
        else:
            print(df.head().to_string())
    except Exception:
        print(df.head().to_string())
    
    print("\n=== Sample Data (last 5 rows) ===")
    try:
        if 'tabulate' in sys.modules:
            print(tabulate(df.tail(), headers='keys', tablefmt='pretty'))
        else:
            print(df.tail().to_string())
    except Exception:
        print(df.tail().to_string())
    
    print("\n=== Unique Seasons ===")
    if 'SEASON' in df.columns:
        seasons = df['SEASON'].unique()
        print(seasons)
        
        print("\n=== Matches per Season ===")
        season_counts = df['SEASON'].value_counts().sort_index()
        print(season_counts)
    
    print("\n=== Null Values Count ===")
    print(df.isnull().sum())

def export_to_csv(df, filename=None):
    """Export DataFrame to CSV file"""
    if df is None or df.empty:
        print("No data to export")
        return
    
    if filename is None:
        # Generate filename with timestamp
        timestamp = pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')
        filename = f"premier_league_data_{timestamp}.csv"
    
    # Save DataFrame to CSV
    df.to_csv(filename, index=False)
    print(f"\nData exported to CSV: {filename}")
    print(f"File size: {os.path.getsize(filename) / 1024:.2f} KB")

def main():
    """Main function to run the test"""
    print("=" * 70)
    print("PREMIER LEAGUE DATABASE TEST")
    print("=" * 70)
    
    # Load data from PostgreSQL
    df = load_postgres_data()
    
    if df is not None and not df.empty:
        # Analyze the DataFrame
        analyze_dataframe(df)
        
        # Option to export to CSV
        export = input("\nExport data to CSV? (y/n): ").lower()
        if export == 'y':
            export_to_csv(df)
    
    print("\nTest completed")

if __name__ == "__main__":
    main()
