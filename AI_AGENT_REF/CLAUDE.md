# English Premier League Prediction (EPL-P)

## Project overview
An end-to-end machine learning and data engineering pipeline designed to predict English Premier League (EPL) match outcomes and betting probabilities. The system automates the entire lifecycle: from daily web scraping and data ingestion into PostgreSQL/MariaDB, through ETL and validation using Great Expectations, to model training/tracking with MLflow and deployment via a Django/Next.js web application.

The project is designed to run entirely on containerized local infrastructure, ensuring data sovereignty and reproducibility without relying on cloud-managed services.

## Tech stack
| Component | Technology |
|-----------|------------|
| **Languages** | Python 3.12 (Pipeline), TypeScript (Frontend), Python 3.11+ (Backend) |
| **Orchestration** | Apache Airflow (Astro CLI) |
| **Frontend** | Next.js, React, Styled Components |
| **Backend** | Django REST Framework, FastAPI (planned for prediction) |
| **Databases** | MariaDB (ETL), PostgreSQL (Scraping), Redis (Caching) |
| **ML/Data Ops** | XGBoost, Scikit-learn, MLflow, DVC, Great Expectations |
| **Infrastructure** | Docker, Docker Compose |

## Repository structure
- `astro_airflow_mlflow/`: Core orchestration and ML pipeline logic.
  - `dags/`: Airflow Directed Acyclic Graphs.
  - `src/`: Custom Python packages for ETL and Model training.
  - `include/`: SQL and additional scripts.
- `Full_Stack_WebApp/`: Production web interface.
  - `Backend/`: Django REST API.
  - `frontend/`: Next.js UI.
- `Datasets/`: DVC-tracked CSV files (Match history from 2000-2020+).
- `Scrapping_Scripts/`: Postgres-based scraping utilities.
- `Docker_Learning_Project/`: Side-project/Reference for multi-container setup.

## Getting started
1. **Initialize Astro**: `cd astro_airflow_mlflow && astro dev start`
2. **Setup DVC**: `dvc pull` (if remote is configured)
3. **Start Databases**: Run the MariaDB and Postgres containers via Docker (see `Steps_Done_Self.md`).
4. **Backend Setup**: `cd Full_Stack_WebApp/Backend && pip install -r requirements.txt && python manage.py migrate`
5. **Frontend Setup**: `cd Full_Stack_WebApp/frontend && npm install && npm run dev`

## Environment variables
| Variable | Description | Example |
|----------|-------------|---------|
| `main_mariadb_container_host` | MariaDB service hostname | `mariadb` (compose) / `localhost` (host shell) |
| `main_mariadb_container_user` | MariaDB username | `root` |
| `main_mariadb_container_password` | MariaDB password | `your_password` |
| `MLFLOW_TRACKING_URI` | MLflow server URL | `http://localhost:5000` |
| `REDIS_HOST` | Redis container host | `localhost` |

## Architecture overview
1. **Scraping**: `web_scraper.py` fetches data -> PostgreSQL (`epl_scrapped`).
2. **ETL**: Airflow DAGs move data from Postgres/CSV -> MariaDB (`scrapped_data_database_1`).
3. **Validation**: Great Expectations validates schema/quality.
4. **Transformation**: Feature engineering (Form, Goals, etc.) -> MariaDB (`cleaned_data_database_2`).
5. **Training**: Data cached in Redis -> XGBoost training -> Tracked in MLflow.
6. **Serving**: Best model saved to `artifacts/` -> Served via API (FastAPI/Django).

## Key conventions
- **Naming**: Snake_case for Python files/functions, PascalCase for React components.
- **Data Flow**: Always validate data before transformation using the `data_validation` component.
- **ML Logging**: Every training run must be logged to MLflow with a unique `run_name`.
- **Database Schema**: Column names in scraped databases often use uppercase abbreviations (e.g., `FTHG`, `FTR`).

## Database
- **MariaDB**: Main ETL store. `scrapped_data_database_1` (Raw), `cleaned_data_database_2` (Transformed).
- **PostgreSQL**: Daily scraping landing zone. `epl_scrapped`.
- **Redis**: Stores parquet-encoded DataFrames for fast ML training access.

## Testing
- Run Airflow tests: `astro dev pytest`
- Django tests: `python manage.py test`
- **Coverage**: Current coverage is low; new features should include unit tests in `tests/` directories.

## Do not touch
- `mlruns/` and `mlartifacts/`: Managed by MLflow.
- `.dvc/`: Internal DVC metadata.
- `Full_Stack_WebApp/Models/`: Production model binaries (handled by deployment pipeline).

## Known issues & gotchas
- **Host Networking**: Inside `docker compose`, services reach each other by service-DNS names (`mariadb`, `redis`, `mlflow`, `prediction_service`, `postgres`). From the host shell or browser, use `localhost:<published-port>`. Do not hardcode `192.168.x.x`.
