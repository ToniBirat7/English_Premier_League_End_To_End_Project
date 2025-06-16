#!/usr/bin/env python3
"""
Check for specific tables and sequences in PostgreSQL
"""

import psycopg2

# Database configuration
postgres_config = {
    'host': 'localhost',
    'port': 5434,
    'user': 'postgres',
    'password': 'postgres',
    'database': 'weekly_scrapped_data'
}

def check_specific_objects():
    """
    Check for specific tables and sequences in the database
    """
    conn = None
    try:
        # Connect to the database
        print(f"Connecting to PostgreSQL at {postgres_config['host']}:{postgres_config['port']}")
        conn = psycopg2.connect(**postgres_config)
        cursor = conn.cursor()
        
        # Check for PREMIER_LEAGUE_MATCHES_4 table
        cursor.execute("""
        SELECT EXISTS(
            SELECT FROM information_schema.tables 
            WHERE table_schema = 'public' AND table_name = 'premier_league_matches_4'
        )
        """)
        table_4_exists = cursor.fetchone()[0]
        print(f"Table 'premier_league_matches_4' exists: {table_4_exists}")
        
        # Check for PREMIER_LEAGUE_MATCHES_5 table
        cursor.execute("""
        SELECT EXISTS(
            SELECT FROM information_schema.tables 
            WHERE table_schema = 'public' AND table_name = 'premier_league_matches_5'
        )
        """)
        table_5_exists = cursor.fetchone()[0]
        print(f"Table 'premier_league_matches_5' exists: {table_5_exists}")
        
        # Check for sequences
        cursor.execute("""
        SELECT EXISTS(
            SELECT FROM information_schema.sequences 
            WHERE sequence_schema = 'public' AND sequence_name = 'premier_league_matches_4_id_seq'
        )
        """)
        seq_4_exists = cursor.fetchone()[0]
        print(f"Sequence 'premier_league_matches_4_id_seq' exists: {seq_4_exists}")
        
        cursor.execute("""
        SELECT EXISTS(
            SELECT FROM information_schema.sequences 
            WHERE sequence_schema = 'public' AND sequence_name = 'premier_league_matches_5_id_seq'
        )
        """)
        seq_5_exists = cursor.fetchone()[0]
        print(f"Sequence 'premier_league_matches_5_id_seq' exists: {seq_5_exists}")
        
        # List all sequences
        cursor.execute("""
        SELECT sequence_name FROM information_schema.sequences 
        WHERE sequence_schema = 'public'
        ORDER BY sequence_name
        """)
        
        sequences = cursor.fetchall()
        print("\nAll sequences in the database:")
        for seq in sequences:
            print(f"- {seq[0]}")
            
        # List all tables
        cursor.execute("""
        SELECT table_name FROM information_schema.tables 
        WHERE table_schema = 'public'
        ORDER BY table_name
        """)
        
        tables = cursor.fetchall()
        print("\nAll tables in the database:")
        for table in tables:
            print(f"- {table[0]}")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    check_specific_objects()
