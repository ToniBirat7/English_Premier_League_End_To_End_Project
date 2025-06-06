# model_trainer.py file

from pathlib import Path
from src.entity.config_entity import ModelTrainerConfig
from src.utils.common import create_directories
from src.utils.eda_functions.visualization_methods import *
from src import src_logger as logger
import pandas as pd

class ModelTrainer:
    def __init__(self, config: ModelTrainerConfig) -> None:
        self.config = config

        create_directories([self.config.model_path, self.config.train_dir, self.config.test_dir])

    def return_visualize_data(self, data: pd.DataFrame) -> None:
        """
        Visualize the data using matplotlib or seaborn.
        This method can be extended to include more visualizations as needed.
        """
        # Call the visualization functions and then append the plots to the list
        plots_created = []

        # Example visualizations