#!/usr/bin/env python3
"""
Simple PostgreSQL connection test
"""

import psycopg2

# Try to connect with simple parameters
try:
    print("Attempting to connect to PostgreSQL...")
    conn = psycopg2.connect(
        host="localhost",
        port=5434,
        user="postgres",
        password="postgres",
        database="weekly_scrapped_data"
    )
    print("Connection successful!")
    conn.close()
    print("Connection closed.")
except Exception as e:
    print(f"Connection error: {e}")
