import pandas as pd
import pymysql
import os
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()

def generate_create_table_sql(df, table_name="final_dataset"):
    dtype_mapping = {
        'int64': 'INT',
        'float64': 'DOUBLE',
        'object': 'VARCHAR(255)',
        'bool': 'BOOLEAN',
        'datetime64[ns]': 'DATETIME',
    }

    columns = []
    for col, dtype in df.dtypes.items():
        col_type = dtype_mapping.get(str(dtype), 'VARCHAR(255)')
        if col == df.columns[0] and col_type in ['INT', 'BIGINT']:
            columns.append(f"{col} {col_type} PRIMARY KEY")
        else:
            columns.append(f"{col} {col_type}")
    
    columns_sql = ",\n    ".join(columns)
    create_table_sql = f"CREATE TABLE IF NOT EXISTS {table_name} (\n    {columns_sql}\n);"
    return create_table_sql

def main():
    # Load DataFrame
    df = pd.read_csv("./artifacts/data_transformation/transformed_data_final.csv")
    table_name = "final_dataset"

    # Generate CREATE TABLE SQL
    create_table_sql = generate_create_table_sql(df, table_name)

    # Get DB credentials from environment variables
    db_config = {
        "host": os.getenv("main_mariadb_container_host", "localhost"),
        "user": os.getenv("main_mariadb_container_user"),
        "password": os.getenv("main_mariadb_container_password"),
        "database": os.getenv("cleaned_data_database_2"),
        "port": int(os.getenv("main_mariadb_container_port", 3306)),
    }

    # Print environment variables (for debug)
    print("📦 Environment Variables Used:")
    print(f"  Host: {db_config['host']}")
    print(f"  User: {db_config['user']}")
    print(f"  Password: {db_config['password']}")
    print(f"  Port: {db_config['port']}")
    print(f"  Database: {db_config['database']}")

    try:
        # Connect to the DB
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()

        # Create table
        cursor.execute(create_table_sql)
        print(f"✅ Table `{table_name}` created or already exists.")

        # Prepare and execute insert query
        placeholders = ", ".join(["%s"] * len(df.columns))
        insert_query = f"""
            INSERT INTO {table_name} ({', '.join(df.columns)})
            VALUES ({placeholders})
        """
        cursor.executemany(insert_query, df.values.tolist())
        conn.commit()
        print(f"✅ Inserted {len(df)} rows into `{table_name}`")

    except Exception as e:
        print("❌ Error:", e)

    finally:
        if conn:
            conn.close()
            print("🔒 Connection closed.")

if __name__ == "__main__":
    main()
