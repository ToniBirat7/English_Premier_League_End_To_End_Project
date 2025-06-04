# Data Validation Pipeline
from src.config.configuration import ConfigurationManager
from src.components.data_validation import DataValidation
from src.constants import CONFIG_FILE_PATH, PARAMS_FILE_PATH, SCHEMA_FILE_PATH

class DataValidationPipeline:
    def __init__(self) -> None:
        pass

    def main(self):
        # Implement the main logic for the data validation pipeline
        config = ConfigurationManager(
            config_file_path=CONFIG_FILE_PATH,
            params_file_path=PARAMS_FILE_PATH,
            schema_file_path=SCHEMA_FILE_PATH
        )

        data_validation = DataValidation(config=config.get_data_validation_config())
        is_valid = data_validation.validate_data()
        data_validation.save_validation_status(is_valid)


if __name__ == '__main__':
    try:
        print(">>> Starting Data Validation Pipeline <<<")
        obj = DataValidationPipeline()
        obj.main()
        print(">>> Data Validation Pipeline Completed Successfully <<<")
    except Exception as e:
        print(f"Error in Data Validation Pipeline: {e}")
        raise e