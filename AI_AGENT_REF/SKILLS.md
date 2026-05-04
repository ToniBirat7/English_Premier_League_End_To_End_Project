# Agent skills

## Add a new Feature to the ML Pipeline
### When to use
Use this when you need to calculate a new statistic (e.g., xG, player injuries) to improve model accuracy.
### Files to read first
- `astro_airflow_mlflow/src/components/data_transformation.py`
- `astro_airflow_mlflow/schema.yaml`
### Step-by-step process
1. Add the feature calculation logic to `DataTransformation` in `data_transformation.py`.
2. Update `schema.yaml` to include the new column.
3. Update `params.yaml` if the new feature requires specific hyperparameters.
4. Run the transformation DAG to verify the new CSV output.
### Verification checklist
- Check `logs/logging.log` for transformation errors.
- Verify the new column exists in the output CSV in `artifacts/data_transformation/`.

## Add a new API endpoint to the Django Backend
### When to use
Use this when the frontend needs new data (e.g., Player stats, Head-to-head records).
### Files to read first
- `Full_Stack_WebApp/Backend/football_api/models.py`
- `Full_Stack_WebApp/Backend/football_api/views.py`
- `Full_Stack_WebApp/Backend/football_api/urls.py`
### Step-by-step process
1. Define the model in `models.py` if new data storage is needed.
2. Create a serializer in `serializers.py`.
3. Add a ViewSet or action in `views.py`.
4. Register the route in `urls.py`.
5. Run migrations: `python manage.py makemigrations` and `python manage.py migrate`.

## Train and Log a New Model
### When to use
Use this when hyperparameter tuning or feature engineering is complete.
### Files to read first
- `astro_airflow_mlflow/dags/model_train.py`
- `astro_airflow_mlflow/src/components/model_trainer.py`
### Step-by-step process
1. Trigger the `model_train` DAG via Airflow.
2. Monitor MLflow at `localhost:5000`.
3. Verify the best model is saved to `artifacts/models/`.
### Verification checklist
- F1 score and Accuracy logged in MLflow.
- Model signature matches the input features.

## Update the Web Scraper
### When to use
Use this when the target website structure changes or a new season starts.
### Files to read first
- `astro_airflow_mlflow/Scrapping_Scripts/web_scraper.py`
### Step-by-step process
1. Modify the selector logic or API URL in `web_scraper.py`.
2. Test the connection: `python Scrapping_Scripts/test_api_connectivity.py`.
3. Run the scraper: `python Scrapping_Scripts/web_scraper.py`.
