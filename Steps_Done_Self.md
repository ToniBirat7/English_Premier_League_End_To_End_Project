## **Below are the steps that have been completed so far:**

**Note:** Do not copy `.env` file while creating Docker image. It contains sensitive information. Rather use environment variables to pass sensitive information to the container. Or pass the `.env` file while running the container using `--env-file` option.

- **Created MariaDB**

```bash

docker pull mariadb/columnstore

docker run -p 3306:3306 --name main-mariadb mariadb/columnstore

docker exec main-mariadb mariadb -e "GRANT ALL PRIVILEGES ON *.* TO 'birat-gautam'@'localhost' IDENTIFIED BY '';"

mariadb -u birat-gautam -p

MariaDB [(none)]> GRANT ALL PRIVILEGES ON your_database.* TO 'birat-gautam'@'%' IDENTIFIED BY 'Admin123@Birat';
ERROR 1044 (42000): Access denied for user 'birat-gautam'@'localhost' to database 'your_database'

```

### **Create all the Required MariadB Databases**

**Initial Database(Store One Big Table)**

We will store the `OBT` table in this database. The data will be fetched from the `SQL` database and stored in this database.

```bash

MariaDB [(none)]> CREATE DATABASE scrapped_data_database_1;
Query OK, 1 row affected (0.001 sec)

MariaDB [(none)]> CREATE DATABASE cleaned_data_database_2;
Query OK, 1 row affected (0.001 sec)

```

### **Store and Fetch Data from the Database**

```Python

# Store a DataFrame into a MariaDB table using pymysql

#import pymysql
import pandas as pd

# Step 1: Create a simple DataFrame
df = pd.DataFrame({
    'sepal_length': [5.1, 4.9, 4.7],
    'sepal_width': [3.5, 3.0, 3.2],
    'petal_length': [1.4, 1.4, 1.3],
    'petal_width': [0.2, 0.2, 0.2],
    'species': ['setosa', 'setosa', 'setosa']
})

# Step 2: Connect to MariaDB
conn = pymysql.connect(
    host='localhost',
    user='birat-gautam',
    password='Admin123@Birat',
    database='scrapped_data_database_1'
)
cursor = conn.cursor()

# Step 3: Create table (if not exists)
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Iris (
        sepal_length FLOAT,
        sepal_width FLOAT,
        petal_length FLOAT,
        petal_width FLOAT,
        species VARCHAR(20)
    )
""")

# Step 4: Insert all rows from DataFrame
for row in df.itertuples(index=False):
    cursor.execute("""
        INSERT INTO Iris (sepal_length, sepal_width, petal_length, petal_width, species)
        VALUES (%s, %s, %s, %s, %s)
    """, tuple(row))

# Step 5: Commit and close
conn.commit()
conn.close()

```

```Python
# Fetch data from the MariaDB table into a DataFrame

# Retrieve the data back to verify
import pymysql
import pandas as pd

# Connect to MariaDB
conn = pymysql.connect(
    host='localhost',
    user='birat-gautam',
    password='Admin123@Birat',
    database='scrapped_data_database_1'
)

# Use pandas to read the SQL table into a DataFrame
df_retrieved = pd.read_sql("SELECT * FROM Iris", conn)

conn.close()

# Show the DataFrame
df_retrieved.head()

```

### **Create a Redis Database**

````bash

docker pull redis

docker run --name main-redis -p 6379:6379 -d redis

docker exec -it main-redis bash

redis-cli

%pip install redis

%pip install pyarrow

```-

If the container is closed then the data will be lost. To persist the data, we can use a volume.

### **Create a Production Ready Project Structure**

```Python

# Automated Script for a complete end-to-end ML project

from pathlib import Path
import logging
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

list_of_files = [
  ".github/workflows/.gitkeep",
  f"src/__init__.py",
  f"src/components/__init__.py",
  f"src/components/data_ingestion.py",
  f"src/components/data_validation.py",
  f"src/components/data_transformation.py",
  f"src/components/model_trainer.py",
  f"src/components/model_evaluation.py",
  f"src/components/model_pusher.py",
  f"src/utils/__init__.py",
  f"src/utils/common.py",
  f"src/utils/logger.py",
  f"src/config/__init__.py",
  f"src/config/configuration.py",
  f"src/pipeline/__init__.py",
  f"src/entity/__init__.py",
  f"src/entity/config_entity.py",
  f"src/constants/__init__.py",
  "config/config.yaml",
  "params.yaml",
  "schema.yaml",
  "main.py",
  "Dockerfile",
  "setup.py",
  "research/research.ipynb",
  "templates/index.html",
  "requirements.txt",
  "README.md",
  ".gitignore",
]

for filepath in list_of_files:
    filepath = Path(filepath)
    filedir,filename = os.path.split(filepath)
    print(f"Processing file: {filedir}, {filename}")
    print(f"Type of file: {type(filedir)}")
    if not os.path.exists(filedir):
        if (not filedir):
            logging.info(f"File directory is empty, creating in current directory.")
        else:
          logging.info(f"Creating directory: {filedir}")
          os.makedirs(filedir,exist_ok=True)
    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        logging.info(f"Creating file: {filepath}")
        with open(filepath, 'w') as f:
          logging.info(f"Writing to file: {filepath}")
          # Write a comment or placeholder content based on the file type
          if filename == "__init__.py":
              f.write("# This is an init file for the package\n")
          if filename == "config.yaml":
              f.write("# Configuration file for the project\n")
          elif filename == "params.yaml":
              f.write("# Parameters for the project\n")
          elif filename == "schema.yaml":
              f.write("# Schema for the project\n")
          elif filename == "main.py":
              f.write("# Main entry point for the project\n")
          elif filename == "Dockerfile":
              f.write("# Dockerfile for the project\n")
          elif filename == "setup.py":
              f.write("# Setup script for the project\n")
          else:
              f.write(f"# {filename} file\n")
    else:
        logging.info(f"File already exists and is not empty: {filepath}")
````

### **Initialize Git Repository**

```bash
git init
git add .
git commit -m "Initial commit with project structure"
```

### **Full_Stack_WebApp Initialized**

```bash

django-admin startproject Backend_WebApp


```

**Backend_WebApp** is the name of the Django project. You can change it to whatever you prefer.

**Flask_App** is the name of the Flask application. You can change it to whatever you prefer.

**Frontend_WebApp** is the name of the React application. You can change it to whatever you prefer.

Setup the `Next.js` application in the `Frontend_WebApp` directory.

```bash

npx create-next-app@latest

No tailwind

```

### **DVC Initialized**

```bash
dvc init
dvc add Datasets/
git add Datasets.dvc .gitignore
git commit -m "Add Datasets folder to DVC tracking"
```

### **Configure All the Files**

### **Configure Logger**

```Python

```

### **Configure utils/common.py**

```Python

```

### **AstroCLI Initialized**

First install the Astro CLI if you haven't already:

```bash
curl -sSL install.astronomer.io | sudo bash -s
```

Then, create a new Astro project:

````bash
astro dev init
astro dev start
astro dev stop
astro dev logs

```docker build -t your-dockerhub-username/your-image-name .
docker push your-dockerhub-username/your-image-name
**Note:** Now, we will need to give the path relative to the containers path i.e. for `logging` to save the `logs` we will need to give `logs_dirs=/usr/local/airflow/logs` in the sr.

Also, we need to build the `astro` image without the `--no-cache` option to ensure that the latest changes are reflected in the image.

```bash

````

### **Now we will configure all the Entity, Configuration, and Pipeline files**

### **Data Validation**

But, before that have an idea about the Dataset. Visualize the data using `pandas` and `matplotlib` to understand the data better.

Identify the final columns that you want to keep in the final dataset. This will help in data validation and transformation steps.

```Python

```

### **SofaScore Clone**

Either clone or embed the whole website

### **MariadB Connection**

**Direct Declartion of the Values**

If not set the `envs` as `export main_mariadb_container_password=NewStrongPasswordHere`
then you can directly declare the values in the code.

```bash
export main_mariadb_container_password=NewStrongPasswordHere scrapped_data_database_1=scrapped_data_database_1
```

Always clear the Environment Variables after use to avoid any security issues.

```Python
# import pandas as pd
# import pymysql
# from dotenv import load_dotenv
# import os

# # Clear previous env vars if necessary
# for var in [
#     "main_mariadb_container_host",
#     "main_mariadb_container_port",
#     "main_mariadb_container_user",
#     "main_mariadb_container_password",
#     "scrapped_data_database_1",
#     "cleaned_data_database_2",
# ]:
#     os.environ.pop(var, None)

# # Load environment variables from .env in current directory
# env_loaded = load_dotenv(override=True)
# print(f".env loaded: {env_loaded}")

# def create_and_store_small_df():
#     host = os.getenv("main_mariadb_container_host")
#     user = os.getenv("main_mariadb_container_user")
#     password = os.getenv("main_mariadb_container_password")
#     port = int(os.getenv("main_mariadb_container_port", "3306"))
#     database = os.getenv("cleaned_data_database_2")

#     print("Loaded env vars:")
#     print("HOST:", host)
#     print("USER:", user)
#     print("PASSWORD:", password)
#     print("PORT:", port)
#     print("DB:", database)

#     print("\nTypes of loaded env vars:")
#     print("HOST type:", type(host))
#     print("USER type:", type(user))
#     print("PASSWORD type:", type(password))
#     print("PORT type:", type(port))
#     print("DB type:", type(database))

#     # Sample DataFrame
#     data = {
#         'id': [1, 2, 3, 4, 5],
#         'name': ['Arsenal', 'Chelsea', 'Liverpool', 'Man City', 'Man United'],
#         'points': [78, 65, 82, 89, 73],
#         'goals_scored': [68, 45, 75, 89, 57]
#     }
#     df = pd.DataFrame(data)
#     print("Sample DataFrame:")
#     print(df)

#     conn = None
#     try:
#         # Connect to MariaDB
#         conn = pymysql.connect(
#             host=host,
#             port=port,
#             user=user,
#             password=password,
#             database=database
#         )
#         print("\n✅ Connected to MariaDB successfully!\n")

#         with conn.cursor() as cursor:
#             table_name = 'sample_epl_data'

#             # Create table if not exists
#             create_table_sql = f"""
#             CREATE TABLE IF NOT EXISTS {table_name} (
#                 id INT PRIMARY KEY,
#                 name VARCHAR(50),
#                 points INT,
#                 goals_scored INT
#             )
#             """
#             cursor.execute(create_table_sql)

#             # Clear existing data in table
#             cursor.execute(f"DELETE FROM {table_name}")

#             # Insert DataFrame rows into table
#             insert_sql = f"INSERT INTO {table_name} (id, name, points, goals_scored) VALUES (%s, %s, %s, %s)"
#             data_to_insert = df.values.tolist()
#             cursor.executemany(insert_sql, data_to_insert)

#             conn.commit()
#             print(f"✅ Successfully inserted {len(df)} rows into `{table_name}`")

#             # Fetch and print to verify
#             cursor.execute(f"SELECT * FROM {table_name}")
#             results = cursor.fetchall()

#         print("\n✅ Data fetched from MariaDB:")
#         for row in results:
#             print(row)

#     except Exception as e:
#         print(f"\n❌ Error: {e}")

#     finally:
#         if conn:
#             conn.close()
#         print("\n🔒 Connection closed.")

# if __name__ == "__main__":
#     create_and_store_small_df()

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
```

### **Accessing the ENVs in the Airflow Container**

Do not rely on the `.env` file to pass the environment variables to the Airflow container. Instead, use the `docker run` command with the `--env` option or use a `.env` file with the `--env-file` option.

```bash
docker run --env main_mariadb_container_password=NewStrongPasswordHere --env scrapped_data_database_1=scrapped_data_database_1 your-airflow-image
```

Or

Use the `docker-compose.yml` file to define the environment variables for the Airflow container.

Or

Use the Airflow Conncetion API to set the environment variables from the `UI`
then catch them inside the DAG using the `Variable.get()` method.
