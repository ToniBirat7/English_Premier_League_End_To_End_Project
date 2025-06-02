## **Below are the steps that have been completed so far:**

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

```bash
astro dev init
astro dev start
astro dev stop
astro dev logs

```

What we've done is set up a basic Astro project structure. You can now start adding your tasks and workflows to the `astro` directory.

Then, we copied all the folders and files required for the project into the `astro` directory. This includes the `src`, `config`, `params.yaml`, `schema.yaml`, and other necessary files.

**Note:** Now, we will need to give the path relative to the containers path i.e. for `logging` to save the `logs` we will need to give `logs_dirs=/usr/local/airflow/logs` in the sr.

Also, we need to build the `astro` image without the `--no-cache` option to ensure that the latest changes are reflected in the image.

```bash

```

### **Now we will configure all the Entity, Configuration, and Pipeline files**
