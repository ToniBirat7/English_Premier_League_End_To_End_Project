import pandas as pd
import pymysql
from dotenv import load_dotenv
import os

# Load environment variables from .env (optional, here you hardcoded creds)
load_dotenv()

def create_and_store_small_df():
    # Connection parameters - using correct environment variable names from .env
    host = os.getenv("main_mariadb_container_host", "localhost")  # This exists in .env
    user = os.getenv("main_mariadb_container_user", "birat-gautam")  # This exists in .env
    password = os.getenv("main_mariadb_container_password", "")  # This exists in .env
    port = int(os.getenv("main_mariadb_container_port", "3306"))  # This exists in .env
    database = os.getenv("scrapped_data_database_1", "scrapped_data_database_1")  # This exists in .env

    print(f"\nConnecting to MariaDB:")
    print(f"  Host: {host}")
    print(f"  User: {user}")
    print(f"  Password: {'***' if password else 'EMPTY'}")
    print(f"  Port: {port}")
    print(f"  Database: {database}\n")

    # Sample DataFrame
    data = {
        'id': [1, 2, 3, 4, 5],
        'name': ['Arsenal', 'Chelsea', 'Liverpool', 'Man City', 'Man United'],
        'points': [78, 65, 82, 89, 73],
        'goals_scored': [68, 45, 75, 89, 57]
    }
    df = pd.DataFrame(data)
    print("Sample DataFrame:")
    print(df)

    conn = None
    try:
        # Connect to MariaDB
        conn = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database
        )
        print("\n✅ Connected to MariaDB successfully!\n")

        with conn.cursor() as cursor:
            table_name = 'sample_epl_data'

            # Create table if not exists
            create_table_sql = f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                id INT PRIMARY KEY,
                name VARCHAR(50),
                points INT,
                goals_scored INT
            )
            """
            cursor.execute(create_table_sql)

            # Clear existing data in table
            cursor.execute(f"DELETE FROM {table_name}")

            # Insert DataFrame rows into table
            insert_sql = f"INSERT INTO {table_name} (id, name, points, goals_scored) VALUES (%s, %s, %s, %s)"
            data_to_insert = df.values.tolist()
            cursor.executemany(insert_sql, data_to_insert)

            conn.commit()
            print(f"✅ Successfully inserted {len(df)} rows into `{table_name}`")

            # Fetch and print to verify
            cursor.execute(f"SELECT * FROM {table_name}")
            results = cursor.fetchall()

        print("\n✅ Data fetched from MariaDB:")
        for row in results:
            print(row)

    except Exception as e:
        print(f"\n❌ Error: {e}")

    finally:
        if conn:
            conn.close()
        print("\n🔒 Connection closed.")

if __name__ == "__main__":
    create_and_store_small_df()
