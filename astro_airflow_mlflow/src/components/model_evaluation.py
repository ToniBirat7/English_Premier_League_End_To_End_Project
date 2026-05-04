# model_evaluation.py file

from src.entity.config_entity import ModelTrainerConfig
from src import src_logger as logger
from sklearn.metrics import confusion_matrix, classification_report, f1_score


class ModelEvaluation:
    def __init__(self, config: ModelTrainerConfig) -> None:
        self.config = config

    def evaluate(self, model, X_train, y_train_encoded, X_test, y_test_encoded) -> dict:
        """Run train + test evaluation against a fitted model.

        Returns a dict ready for mlflow.log_metric / log_text:
          - train_f1, train_accuracy, test_f1, test_accuracy (floats)
          - confusion_matrix (str), classification_report (str)
        Mirrors the inline metrics block in
        dags/load_and_test_best_model.py so DAGs delegate to a single source.
        """
        logger.info("Starting model evaluation")

        y_train_pred = model.predict(X_train)
        y_test_pred = model.predict(X_test)

        train_f1 = float(f1_score(y_train_encoded, y_train_pred, pos_label=0))
        train_accuracy = float(sum(y_train_encoded == y_train_pred) / len(y_train_pred))
        test_f1 = float(f1_score(y_test_encoded, y_test_pred, pos_label=0))
        test_accuracy = float(sum(y_test_encoded == y_test_pred) / len(y_test_pred))

        cm = confusion_matrix(y_test_encoded, y_test_pred)
        cr = classification_report(y_test_encoded, y_test_pred)

        logger.info(f"Train F1: {train_f1}, Train Accuracy: {train_accuracy}")
        logger.info(f"Test F1: {test_f1}, Test Accuracy: {test_accuracy}")
        logger.info(f"Confusion Matrix:\n{cm}")
        logger.info(f"Classification Report:\n{cr}")

        return {
            "train_f1": train_f1,
            "train_accuracy": train_accuracy,
            "test_f1": test_f1,
            "test_accuracy": test_accuracy,
            "confusion_matrix": str(cm),
            "classification_report": str(cr),
        }
