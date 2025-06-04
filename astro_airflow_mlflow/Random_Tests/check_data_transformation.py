# We will check the data transformation

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.config.configuration import ConfigurationManager
from src.components.data_transformation import DataTransformation
from src.constants import *
from src import src_logger

obj = DataTransformation(
    config=ConfigurationManager(
        config_file_path=CONFIG_FILE_PATH,
        params_file_path=PARAMS_FILE_PATH,
        schema_file_path=SCHEMA_FILE_PATH
    ).get_data_transformation_config()
)

src_logger.info("Initialized DataTransformation\n")

data_set_path = obj.get_dataset_path()
src_logger.info(f"We are reading dataset from {data_set_path}\n")

is_saved = obj.transform_data()
print(is_saved)