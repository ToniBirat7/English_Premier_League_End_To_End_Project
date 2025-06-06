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

    def get_visualized_data(self, data: pd.DataFrame) :
        """
        Visualize the data using matplotlib or seaborn.
        This method can be extended to include more visualizations as needed.
        """
        # Call the visualization functions and then append the plots to the list

        plots_created = []

        try:
            # Scatter plot for numerical features
            scatter_plot = get_scatter_matrix(data)
            plots_created.append(scatter_plot)
            logger.info("Scatter matrix plot created successfully.")

            # Convert boolean columns to integers for correlation analysis
            df_numeric = data.copy()
            bool_cols = df_numeric.select_dtypes(include=['bool']).columns
            df_numeric[bool_cols] = df_numeric[bool_cols].astype(int)
            # Remove non-numeric columns that can't be converted to numeric
            df_numeric = df_numeric.select_dtypes(include=['int64', 'float64'])
            # Fix the correlation matrix styling issue
            corr_styled = df_numeric.corr().style.background_gradient(cmap='coolwarm').format(precision=2)
            plots_created.append(corr_styled)
            logger.info("Correlation matrix plot created successfully.")

            plots_created.append(get_team_points_comparison(data))
            logger.info("Team points comparison plot created successfully.")

            plots_created.append(get_goal_difference_distribution(data))
            logger.info("Goal difference distribution plot created successfully.")
            
            plots_created.append(get_form_points_analysis(data))
            logger.info("Form points analysis plot created successfully.")

            plots_created.append(get_recent_form_heatmap(data))
            logger.info("Recent form heatmap plot created successfully.")

            plots_created.append(get_feature_correlation_heatmap(data))
            logger.info("Feature correlation heatmap plot created successfully.")

            # Fix target distribution function to handle actual FTR values
            plots_created.append(get_target_distribution_fixed(data))
            logger.info("Target distribution plot created successfully.")

            plots_created.append(get_feature_importance_boxplots(data))
            logger.info("Feature importance boxplots created successfully.")

            plots_created.append(get_temporal_trends(data))
            logger.info("Temporal trends plot created successfully.")
            
            return plots_created

        except Exception as e:
            logger.error(f"Error in visualizing data: {e}")
            return None