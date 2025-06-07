# **MVP Version: 1.0.0**

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

We've included the `.env` file in the Dockerfile, but it's not recommended to use it for sensitive information. Instead, pass the environment variables directly when running the container.

```bash
docker run --env main_mariadb_container_password=NewStrongPasswordHere --env scrapped_data_database_1=scrapped_data_database_1 your-airflow-image
```

Or

Use the `docker-compose.yml` file to define the environment variables for the Airflow container.

Or

Use the Airflow Connection API to set the environment variables from the `UI`
then catch them inside the DAG using the `Variable.get()` method.

### **Start the MariaDB Container From the Airflow DAG**

**For Now we'are manually starting the MariaDB container.**

To automate the process of starting the MariaDB container from within an Airflow DAG, you can use the `DockerOperator`. This operator allows you to run Docker containers as tasks in your Airflow DAG.

Create a DAG task to start the MariaDB container using the `DockerOperator`. This will ensure that the container is started before any other tasks that depend on it.

Install `pip install docker`

```Python
(.venv) toni-birat@tonibirat:/media/toni-birat/New Volume/English_Premier_League_Complete_Project/astro_airflow_mlflow$ sudo usermod -aG docker $USER
(.venv) toni-birat@tonibirat:/media/toni-birat/New Volume/English_Premier_League_Complete_Project/astro_airflow_mlflow$
```

### **Connection between the two containers (Astro and Mariadb)**

Use the `docker-compose.yml` file to define the connection between the two containers. This will allow the Airflow container to connect to the MariaDB container using the service name defined in the `docker-compose.yml` file.

Use Astro’s docker-compose or Kubernetes manifests to start MariaDB before Airflow starts.

In local dev: add main-mariadb as a service in docker-compose.override.yml in your Astro project.

```yaml
version: "3"
services:
  main-mariadb:
    image: mariadb:latest
    container_name: main-mariadb
    restart: unless-stopped
    ports:
      - "3306:3306"
    environment:
      MYSQL_ROOT_PASSWORD: NewStrongPasswordHere
      MYSQL_DATABASE: cleaned_data_database_2

  webserver:
    depends_on:
      - main-mariadb
    environment:
      main_mariadb_container_host: main-mariadb
      main_mariadb_container_user: root
      main_mariadb_container_password: NewStrongPasswordHere
      main_mariadb_container_database: cleaned_data_database_2
      main_mariadb_container_port: 3306
```

Either copy the `.env` file to the Airflow container.

We've used this method in the Dockerfile to copy the `.env` file to the Airflow container, but it's not recommended for sensitive information.

```Dockerfile
FROM astrocrpublic.azurecr.io/runtime:3.0-2

# Set working directory
WORKDIR /usr/local/airflow

# Copy essential project files for logging test
COPY src ./src
COPY config ./config
COPY params.yaml ./params.yaml
COPY schema.yaml ./schema.yaml
COPY .env ./.env

# Create logs directory (instead of copying to avoid Docker issues)
RUN mkdir -p logs

# Copy project requirements if it exists
COPY project_requirements.txt ./project_requirements.txt

# Install project-specific Python packages
RUN pip install --no-cache-dir -r project_requirements.txt || echo "No additional requirements to install"

# Set environment variables for the project
ENV PYTHONPATH="${PYTHONPATH}:/usr/local/airflow"
ENV PROJECT_ROOT="/usr/local/airflow"
```

Or

Pass the ENVs using the Airflow Connection API or the Airflow Variable API.

**But when we use the `.env` file, the `localhost` will not work in the Airflow container because `localhost` will point to the address of the container, but we need our host machine's address. Therefore, we need to find the IP `ip route | grep default` and use that IP in the host name of the `.env` file**

We will need to use the `source` IP address of the host machine in the `.env` file.

```bash
(.venv) toni-birat@tonibirat:/media/toni-birat/New Volume/English_Premier_League_Complete_Project/astro_airflow_mlflow$ ip route | grep default
default via 192.168.1.254 dev wlp4s0 proto dhcp src 192.168.1.79 metric 600
(.venv) toni-birat@tonibirat:/media/toni-birat/New Volume/English_Premier_League_Complete_Project/astro_airflow_mlflow$

main_mariadb_container_host=192.168.1.254
```

### **Fetch the Data for Model Training**

- Check Redis Connection : Done

First, find all the Dependencies and Model Parameters (HyperParameter Tuning Ranges) that we will need for the model training.

First, configure all the Entities, Configuration, and Pipeline files to fetch the data from the MariaDB database.

**Then Visualize everything in the `MLFLow` as well.**

- Encountered, this issue ERROR - Failed to import Git (the Git executable is probably not on your PATH), so Git SHA is not available.
  ERROR - All git commands will error until this is rectified.
- Resolved by installing `git` in the Airflow container using the command `apt-get install git`. Updated the Dockerfile to include this installation step.

Some Python code or library (likely in your Airflow DAGs or MLflow-related code) is trying to get the Git SHA using a command like git rev-parse HEAD, but can't find the Git binary.

The PATH environment variable doesn't include Git, simply because Git isn't installed in the container at all.

`apt-get install -y git` installs the Git CLI in your container.

After installation, the Git executable `(/usr/bin/git)` becomes available on the system PATH for all users.

So now when Python code tries to run a git command, it succeeds.

- Store the Train, Test DataFrame in the Redis database for quick access.

- Fetch from the Redis database if the data is already present, otherwise fetch from the MariaDB database.

- Perform the Hyperparameter Tuning using the `MLFLow` and `Optuna` or `Ray Tune`.

- Train the Model with the Parameters and Dependencies fetched from the MariaDB database.

- Save the Best Model

Start the MLflow server locally `mlflow server --host 0.0.0.0 --port 5000`

Below should be the ENVs

```bash
MLFLOW_TRACKING_URI=http://192.168.1.79:5000/
MLFLOW_EXPERIMENT_NAME=EPL_Experiment
```

### **FAST API Model Access**

Minimal FastAPI application to access the model and make predictions.

### **Power BI Dashboard**

- Fetch the data from the MariaDB database and visualize it in Power BI.

### **Implement Scraping Simulation and Add the Necessary DAGs in the Pipeline**

### **Web Application**

Complete Web Application with React and Django.

# **MVP Version: 2.0.0**

**Use Docker Compose to manage the containers**

- Create a `docker-compose.yml` file to define the services and their configurations.

- Add Mariadb Services in the `docker-compose.yml` file.

- Add Redis Services in the `docker-compose.yml` file.

- Add MLflow Services in the `docker-compose.yml` file.

- Host the MLflow server in DAGs Hub.

```yaml
version: "3"
services:
  main-mariadb:
    image: mariadb:latest
    container_name: main-mariadb
    restart: unless-stopped
    ports:
      - "3306:3306"
    environment:
      MYSQL_ROOT_PASSWORD: NewStrongPasswordHere
      MYSQL_DATABASE: cleaned_data_database_2

  webserver:
    depends_on:
      - main-mariadb
    environment:
      main_mariadb_container_host: main-mariadb
      main_mariadb_container_user: root
      main_mariadb_container_password: NewStrongPasswordHere
      main_mariadb_container_database: cleaned_data_database_2
      main_mariadb_container_port: 3306
```

### **Scrapping and Psotgres**

```bash
toni-birat@tonibirat:~$ docker run --name epl_postgres -e POSTGRES_USER=postgres   -e POSTGRES_PASSWORD=postgres   -e POSTGRES_DB=epl_scrapped   -p 5434:5432   -d postgres:15-alpine
```

