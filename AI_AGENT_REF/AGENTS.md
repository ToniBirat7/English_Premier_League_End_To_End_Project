# Agent guidelines

## Agent roles
- **Data Engineer Agent**: Responsible for Airflow DAGs, scraping scripts, and database schema migrations.
- **ML Engineer Agent**: Focuses on `src/components/model_trainer.py`, MLflow integration, and hyperparameter tuning.
- **Full-Stack Agent**: Handles Django backend (`football_api`) and Next.js frontend.

## Allowed operations
- Create and modify Python, TypeScript, and SQL files.
- Run `astro dev` commands for local pipeline testing.
- Run `python manage.py` for Django maintenance.
- Install new Python packages via `project_requirements.txt`.
- Execute database queries for debugging.

## Restricted operations
- **Never** delete DVC metadata files without backup.
- **Never** modify production model binaries in `Full_Stack_WebApp/Models/` manually.
- **Do not** change the core orchestration logic in `astro_airflow_mlflow/` without verifying local container connectivity.

## Tool usage
- **Package Manager**: Use `pip` for Python and `npm` for the frontend.
- **ORM**: Use Django Migrations for `Full_Stack_WebApp` and `pymysql`/`psycopg2` for pipeline scripts.
- **Test Runner**: Use `pytest` for Airflow/ML logic and `python manage.py test` for Django.

## Workflow
1. **Analyze**: Read `CLAUDE.md` and `ARCHITECTURE.md` to understand the component boundaries.
2. **Plan**: Draft changes in a plan artifact.
3. **Develop**: Implement changes, ensuring logging via `src/utils/logger.py`.
4. **Verify**: Run relevant tests and check MLflow for experiment tracking if applicable.
5. **Document**: Update `TASKS.md` and `Steps_Done_Self.md`.

## How to run the project
1. **Infrastructure**: Start MariaDB and Postgres containers (see `Steps_Done_Self.md`).
2. **Pipeline**: `cd astro_airflow_mlflow && astro dev start`.
3. **Backend**: `cd Full_Stack_WebApp/Backend && python manage.py runserver 8000`.
4. **Frontend**: `cd Full_Stack_WebApp/frontend && npm run dev`.

## How to verify work
- **Pipeline**: Trigger DAGs via Airflow UI (`localhost:8080`) and verify task success.
- **ML**: Check MLflow UI (`localhost:5000`) for new runs and metrics.
- **Web**: Verify API endpoints via `localhost:8000/api/` and UI via `localhost:3000`.

## Code style rules
- **Python**: Follow PEP 8; use Type Hints where possible.
- **Logging**: Use the centralized `src_logger` from `src`.
- **Database**: Use context managers for DB connections to ensure they are always closed.
- **Components**: Follow the modular structure (Entity -> Config -> Component -> Pipeline).

## Commit conventions
- Use descriptive prefixes: `feat:`, `fix:`, `chore:`, `docs:`.
- Reference specific components: `feat(ml): add optuna tuning`.

## Context files to always read before starting work
- `CLAUDE.md`
- `ARCHITECTURE.md`
- `Steps_Done_Self.md`
- `astro_airflow_mlflow/config/config.yaml`
