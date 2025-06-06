# model_trainer.py file

from pathlib import Path
from src.entity.config_entity import ModelTrainerConfig
from src.utils.common import create_directories
from src.utils.eda_functions.visualization_methods import *
from src import src_logger as logger
import pandas as pd
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import make_scorer, f1_score
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder


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
    
    def hyperparameter_tuning(self, X_train, y_train, parameters: dict) :

      logger.info("Starting hyperparameter tuning...")

      # TODO: Initialize the classifier
      clf = xgb.XGBClassifier(seed=2)

      # TODO: Make an f1 scoring function using 'make_scorer' 
      f1_scorer = make_scorer(f1_score, pos_label=0)  # 0 corresponds to 'H' in encoded labels

      # TODO: Perform grid search on the classifier using the f1_scorer as the scoring method
      grid_obj = GridSearchCV(clf,
                      scoring=f1_scorer,
                      param_grid=parameters,
                      cv=5)
      
      grid_obj.fit(X_train, y_train)

      logger.info("Hyperparameter tuning completed.")
      logger.info(f"Best parameters found: {grid_obj.best_params_}")
      logger.info(f"Best score achieved: {grid_obj.best_score_}")

      return grid_obj
  
    def split_data(self, data: pd.DataFrame):
          """
          Split the data into training and testing sets.
          """
          logger.info("Splitting data into training and testing sets...")

          X_all = data.drop(columns=['FTR'])
          y_all = data['FTR']

          return X_all, y_all
    
    def split_data_train__test(self, X_all, y_all):
        """
        Split the data into training and testing sets.
        """
        logger.info("Splitting data into training and testing sets...")
        X_train, X_test, y_train, y_test = train_test_split(X_all, y_all,
                                                            test_size=0.3,
                                                            random_state=2,
                                                            stratify=y_all)
        logger.info("Data splitting completed.")
        return X_train, X_test, y_train, y_test
    
    def encode_variable(self, y_train, y_test):
        """
        Encode categorical variables using one-hot encoding.
        """
        label_encoder = LabelEncoder()
        y_train_encoded = label_encoder.fit_transform(y_train)
        y_test_encoded = label_encoder.transform(y_test)
        return y_train_encoded, y_test_encoded
    
    def predict_labels(self,clf, features, target):
      ''' Makes predictions using a fit classifier based on F1 score. '''

      y_pred = clf.predict(features)
      
      return f1_score(target, y_pred, pos_label=0), sum(target == y_pred) / float(len(y_pred))