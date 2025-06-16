#!/usr/bin/env python3
"""
Check existing tables in the PostgreSQL database
"""

import psycopg2
from psycopg2.extras import RealDictCursor

# Database configuration
postgres_config = {
    'host': 'localhost',
    'port': 5434,  # port as integer
    'user': 'postgres',
    'password': 'postgres',
    'database': 'weekly_scrapped_data'
}

def check_tables():
    """
    List all tables and sequences in the PostgreSQL database
    """
    conn = None
    try:
        # Connect to the database
        print(f"Connecting to PostgreSQL at {postgres_config['host']}:{postgres_config['port']}")
        conn = psycopg2.connect(**postgres_config)
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        # Get list of tables
        cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public'
        ORDER BY table_name;
        """)
        
        tables = cursor.fetchall()
        print("\nTables in database:")
        print("=" * 40)
        for table in tables:
            print(f"- {table['table_name']}")
        
        # Get list of sequences
        cursor.execute("""
        SELECT sequence_name 
        FROM information_schema.sequences 
        WHERE sequence_schema = 'public'
        ORDER BY sequence_name;
        """)
        
        sequences = cursor.fetchall()
        print("\nSequences in database:")
        print("=" * 40)
        for seq in sequences:
            print(f"- {seq['sequence_name']}")
        
        # For each table, get its columns
        print("\nTable details:")
        print("=" * 40)
        for table in tables:
            table_name = table['table_name']
            cursor.execute(f"""
            SELECT column_name, data_type, column_default 
            FROM information_schema.columns 
            WHERE table_schema = 'public' AND table_name = '{table_name}'
            ORDER BY ordinal_position;
            """)
            
            columns = cursor.fetchall()
            print(f"\nTable: {table_name}")
            print("-" * 30)
            for col in columns:
                print(f"  {col['column_name']} ({col['data_type']}) {col['column_default'] if col['column_default'] else ''}")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    check_tables()
