import mlflow
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# MLflow config
MLFLOW_TRACKING_URI = "http://192.168.1.79:5000"
REGISTERED_MODEL_NAME = "Best_XGBoost_Model"
MODEL_VERSION = "2"  # Load version 2 explicitly

def load_model_from_registry():
    logger.info("Setting MLflow tracking URI...")
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

    model_uri = f"models:/{REGISTERED_MODEL_NAME}/{MODEL_VERSION}"
    logger.info(f"Loading model from MLflow Registry: {model_uri}")

    model = mlflow.pyfunc.load_model(model_uri)
    logger.info("Model successfully loaded from MLflow Registry.")
    return model

def main():
    try:
        model = load_model_from_registry()
        logger.info("Running predictions...")

        print(model)

    except Exception as e:
        logger.exception("An error occurred during model testing.")

if __name__ == "__main__":
    main()
