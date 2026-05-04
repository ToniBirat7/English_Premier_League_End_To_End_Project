Always use the centralized src_logger from src/__init__.py for all pipeline logging.
Never hardcode 'localhost' for database connections; use the environment variables provided in .env.
When modifying the data schema, update astro_airflow_mlflow/schema.yaml immediately.
All new ML features must be implemented in src/components/data_transformation.py and tested in a notebook first.
Every model training run must be logged to MLflow with a descriptive run name.
Use 'astro dev start' to test Airflow DAG changes locally.
Always run 'dvc status' before and after modifying the Datasets/ directory.
Keep SQL queries inside src/components/ or dags/ using pymysql or PostgresHook.
All Django API views must be registered in Full_Stack_WebApp/Backend/football_api/urls.py.
Use the existing Team and Match models in football_api/models.py — do not create duplicate data structures.
Follow the 'Entity -> Config -> Component -> Pipeline' pattern for all ML tasks.
Maintain uppercase abbreviations (FTR, FTHG, etc.) for match statistics columns in the database.
Check for existing Redis keys before overwriting data in the training pipeline.
Use 'python manage.py load_premier_league_data' to seed the Django database from CSVs.
Always use joblib to save models in the artifacts/models/ directory.
Run 'npm run build' in Full_Stack_WebApp/frontend to verify Next.js types before completing frontend tasks.
Never commit .env files to the repository.
Use 'astro dev pytest' to run tests within the Airflow environment.
Update TASKS.md whenever a significant milestone is reached or tech debt is identified.
Refer to Steps_Done_Self.md for historical context on container setup and manual fixes.
Prefer XGBoost for all EPL match prediction tasks as per project standard.
Ensure all database connections are closed using 'finally' blocks or context managers.
Inside docker compose, use service DNS names (mariadb, redis, mlflow, prediction_service, postgres) for cross-container communication. From host shell or browser, use localhost:<published-port>. Do not hardcode 192.168.x.x host IPs.
Avoid creating raw <button> elements in React; use the design system components if they exist.
Validate all incoming match data using the data_validation component before ingestion.
Keep DAG schedules aligned with the 'daily' scraping and retraining requirement.
Do not modify files in mlruns/ manually; use the MLflow client.
Verify CSV formats match the DVC tracked versions in Datasets/.
Use 'astro-run-dag' utility if available for quick DAG testing.
Always provide type hints for new Python functions and methods.
