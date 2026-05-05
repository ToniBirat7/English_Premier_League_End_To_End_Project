# Project task status

## Completion summary
- **Estimated Completion**: 95%
- Core pipeline is fully operational: data ingestion → validation → feature engineering → model training → MLflow registration → FastAPI prediction service → Django consumption → frontend. All critical path items complete.

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
- [x] Schema.yaml rewrite (EPL columns + FTR target).
- [x] Data validation implementation with column/dtype checks.
- [x] ModelEvaluation component (f1, accuracy, confusion matrix logging).
- [x] FastAPI prediction service (from scratch, full featured).
- [x] Root docker-compose.yml with all services (postgres, mariadb, redis, mlflow, prediction_service).
- [x] Docker networking unified (service-DNS within compose, localhost from host shell).
- [x] Django match_detail endpoint integration with FastAPI prediction service.
- [x] Services layer for Django-to-FastAPI communication with retries and graceful degradation.

## In progress
- (None — all critical path items complete)

## Known TODOs & FIXMEs
- (None — schema, views, docker-compose, and MLflow integration all completed)
- **Future enhancements**: Consider implementing proper StandardScaler persistence in prediction pipeline (currently divides by matchweek as workaround).

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

## Next recommended actions (post-Critical Path)
1. **DVC Remote Setup**: Configure a remote storage backend (S3, GCS, etc.) and push CSVs to enable efficient data versioning.
2. **CI/CD Pipeline**: Populate `.github/workflows/` with automated tests (Airflow, Django, FastAPI, frontend).
3. **Feature Store**: Consider migrating featurizer logic into a shared feature store (Tecton, Feast) to prevent training/serving skew.
4. **Real Data Scraping**: Replace mock possession/shots/cards with actual web-scraped data (Understat, Wyscout).
5. **Kubernetes Migration**: Containerize services with Helm charts for production deployment.
