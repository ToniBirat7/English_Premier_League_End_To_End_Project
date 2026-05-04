# Project task status

## Completion summary
- **Estimated Completion**: 65%
- The project has a solid data pipeline and model training foundation. The web application has a basic structure but lacks real-time prediction integration and production-grade UI.

## Completed work
- [x] Airflow pipeline structure (Astro).
- [x] Data Ingestion from CSV and MariaDB.
- [x] Data Transformation (EPL-specific feature engineering).
- [x] Model Training with XGBoost and MLflow tracking.
- [x] Redis integration for training data caching.
- [x] Daily Web Scraper (API-based Postgres scraper).
- [x] Django Backend (Basic Team/Match models and API).
- [x] Next.js Frontend Initialization.
- [x] Full Forensic Audit & Codebase Cleanup.
- [x] Ground Truth Initialization (CLAUDE.md, AGENTS.md, .clauderules, etc.).

## In progress
- [/] Real-time prediction service (FastAPI integration).
- [/] Data validation using Great Expectations (currently basic).
- [/] Standings calculation logic in Django (currently uses some mock logic).

## Known TODOs & FIXMEs
- `astro_airflow_mlflow/schema.yaml`: Fix boilerplate Wine Quality schema (High Severity).
- `Full_Stack_WebApp/Backend/football_api/views.py`: Replace mock statistics with real calculations (Medium Severity).
- `astro_airflow_mlflow/docker-compose.override.yml`: Populate with required database services (High Severity).
- `src/components/model_trainer.py`: Implement robust model versioning in MLflow (Medium Severity).

## Missing tests
- No unit tests for `src/components/data_transformation.py`.
- No integration tests for the full DAG lifecycle.
- Frontend testing is initialized but empty.

## Tech debt
- **Boilerplate**: Some files still contain "Wine Quality" references from the initial template.
- **Environment Handling**: Reliance on manual host IP detection for container communication.
- **Data Redundancy**: Data is duplicated across Postgres, MariaDB, and CSVs.

## Blocked / needs decision
- **Prediction Frequency**: Should predictions be updated hourly or once daily before kickoff?
- **UI Design**: Need a final decision on the "SofaScore Clone" aesthetic vs a custom premium design.

## Next recommended actions
1. **Clean Schema**: Update `schema.yaml` with the actual EPL features to fix the validation pipeline.
2. **FastAPI Integration**: Migrate the FastAPI prediction logic from `Docker_Learning_Project` to the main pipeline.
3. **Database Unification**: Create a single `docker-compose.yml` that starts all services with proper health checks.
4. **Validation Logic**: Enhance `data_validation.py` to ensure feature parity between training and prediction.
