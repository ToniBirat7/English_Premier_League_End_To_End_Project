# data_transformation.py file

from src.entity.config_entity import DataTransformationConfig
from src.utils.common import create_directories, read_yaml
from src.utils.eda_functions.eda_methods import *
from datetime import datetime as dt
from src import src_logger
from pathlib import Path
import os

class DataTransformation:
    def __init__(self, config: DataTransformationConfig) -> None:
        self.config = config
        create_directories([self.config.root_dir])

    def get_dataframes(self) -> list:
        """
        Transforms the dataset by applying necessary transformations.
        Returns:
            list: A list of pandas DataFrames containing the data from all CSV files in the dataset path.
        """

        dataframes = [] # List to hold all dataframes

        src_logger.info(f"Transforming data from {self.config.dataset_path}")

        # Get all File Paths from the dataset path
        src_logger.info("Fetching all file names from the dataset path")
        file_name_list = get_filename_list(self.config.dataset_path)

        # Get Dataframe from the dataset path
        src_logger.info(f"Found {len(file_name_list)} CSV files in the dataset path")

        for file_name in file_name_list:
            df = get_dataframe_from_csv(os.path.join(self.config.dataset_path, file_name))

            if df is not None:
                src_logger.info(f"Data loaded from {file_name}")
                dataframes.append(df)
            else:
                src_logger.error(f"Failed to load data from {file_name}")

        return dataframes
    
    def get_stats_dataframe(self):
        """
        Transforms the data by applying necessary transformations.
        """

        stats_dataframes = []  # List to hold statistics dataframes

        dataframes = self.get_dataframes()
        src_logger.info(f"Number of dataframes fetched: {len(dataframes)}")

        if not dataframes:
            src_logger.error("No dataframes to transform.")
            return

        for i, df in enumerate(dataframes):
            src_logger.info(f"Processing dataframe {i+1}/{len(dataframes)}")
            # Get basic statistics for the dataframe
            stats_df = get_stats_for_dataframe(df)

            if stats_df is not None:
                src_logger.info(f"Statistics for dataframe {i+1} processed successfully.")
                stats_dataframes.append(stats_df)
            else:
                src_logger.error(f"Failed to process statistics for dataframe {i+1}")

        src_logger.info("All dataframes processed for statistics.")

        return stats_dataframes
    
    def get_goal_scored_conceded_dataframe(self):
        """
        Transforms the data by calculating goals scored and conceded at the end of the match week for each team.
        Returns:
            list: A list of DataFrames containing goals scored and conceded for each team.
        """
        src_logger.info("Calculating goals scored and conceded for each team")

        dataframes = self.get_stats_dataframe()
        goal_scored_conceded_dfs = []

        if not dataframes:
            src_logger.error("No dataframes to process for goals scored and conceded.")
            return goal_scored_conceded_dfs

        for i, df in enumerate(dataframes):
            src_logger.info(f"Processing dataframe {i+1}/{len(dataframes)} for goals scored and conceded")
            goals_df = get_gsc(df) # This function should be defined in eda_methods.py

            if goals_df is not None:
                src_logger.info(f"Goals scored and conceded for dataframe {i+1} processed successfully.")
                goal_scored_conceded_dfs.append(goals_df)
            else:
                src_logger.error(f"Failed to process goals scored and conceded for dataframe {i+1}")

        return goal_scored_conceded_dfs
    
    def get_aggregated_points_dataframe(self):
        """
        Transforms the data by calculating aggregated points for each team.
        Returns:
            list: A list of DataFrames containing aggregated points for each team.
        """
        src_logger.info("Calculating aggregated points for each team")

        dataframes = self.get_goal_scored_conceded_dataframe() # This function should return a list of DataFrames with goals scored and conceded
        aggregated_points_dfs = []

        if not dataframes:
            src_logger.error("No dataframes to process for aggregated points.")
            return aggregated_points_dfs

        for i, df in enumerate(dataframes):
            src_logger.info(f"Processing dataframe {i+1}/{len(dataframes)} for aggregated points")
            agg_points_df = get_agg_points(df)

            if agg_points_df is not None:
                src_logger.info(f"Aggregated points for dataframe {i+1} processed successfully.")
                aggregated_points_dfs.append(agg_points_df)
            else:
                src_logger.error(f"Failed to process aggregated points for dataframe {i+1}")

        return aggregated_points_dfs
  
    def get_team_form_dataframe(self):
        """
        Transforms the data by calculating team form based on the last 5 matches.
        Returns:
            list: A list of DataFrames containing team form for each team.
        """
        src_logger.info("Calculating team form based on the last 5 matches")

        dataframes = self.get_aggregated_points_dataframe()
        team_form_dfs = []

        if not dataframes:
            src_logger.error("No dataframes to process for team form.")
            return team_form_dfs

        for i, df in enumerate(dataframes):
            src_logger.info(f"Processing dataframe {i+1}/{len(dataframes)} for team form")
            form_df = add_form_df(df) # This function should be defined in eda_methods.py

            if form_df is not None:
                src_logger.info(f"Team form for dataframe {i+1} processed successfully.")
                team_form_dfs.append(form_df)
            else:
                src_logger.error(f"Failed to process team form for dataframe {i+1}")

        return team_form_dfs
    
    def get_rearranged_dataframe(self):
        """
        Transforms the data by rearranging the DataFrame with the specified columns.
        Returns:
            list: A list of DataFrames with rearranged columns.
        """
        src_logger.info("Rearranging DataFrame columns")

        dataframes = self.get_team_form_dataframe()
        rearranged_dfs = []

        if not dataframes:
            src_logger.error("No dataframes to rearrange.")
            return rearranged_dfs

        for i, df in enumerate(dataframes):
            src_logger.info(f"Processing dataframe {i+1}/{len(dataframes)} for rearrangement")
            rearranged_df = rearrange_columns(df)

            if rearranged_df is not None:
                src_logger.info(f"DataFrame {i+1} rearranged successfully.")
                rearranged_dfs.append(rearranged_df)
            else:
                src_logger.error(f"Failed to rearrange DataFrame {i+1}")
        return rearranged_dfs

    def get_match_week_dataframe(self):
        """
        Transforms the data by adding match week information to the DataFrame.
        Returns:
            list: A list of DataFrames with match week information added.
        """
        src_logger.info("Adding match week information to DataFrame")

        dataframes = self.get_rearranged_dataframe()
        match_week_dfs = []

        if not dataframes:
            src_logger.error("No dataframes to process for match week.")
            return match_week_dfs

        for i, df in enumerate(dataframes):
            src_logger.info(f"Processing dataframe {i+1}/{len(dataframes)} for match week")
            match_week_df = get_mw(df)

            if match_week_df is not None:
                src_logger.info(f"Match week for dataframe {i+1} processed successfully.")
                match_week_dfs.append(match_week_df)
            else:
                src_logger.error(f"Failed to process match week for dataframe {i+1}")
        return match_week_dfs
    
    def transform_data(self) -> bool:
        """
        Transforms the data by applying all necessary transformations.
        Returns:
            bool: True if transformation is successful, False otherwise.
        """
        src_logger.info("Starting data transformation process")
        
        match_week_dfs = self.get_match_week_dataframe()
        
        if not match_week_dfs:
            src_logger.error("No match week DataFrames to process.")
            return False
        
        # Concatenate all match week DataFrames into a single DataFrame
        src_logger.info(f"Concatenating {len(match_week_dfs)} match week DataFrames")
        single_dataframe = pd.concat(match_week_dfs, ignore_index=True)

        single_dataframe['HTFormPtsStr'] = single_dataframe['HM1'] + single_dataframe['HM2'] + single_dataframe['HM3'] + single_dataframe['HM4'] + single_dataframe['HM5']
        single_dataframe['ATFormPtsStr'] = single_dataframe['AM1'] + single_dataframe['AM2'] + single_dataframe['AM3'] + single_dataframe['AM4'] + single_dataframe['AM5']

        single_dataframe['HTFormPts'] = single_dataframe['HTFormPtsStr'].apply(get_form_points)
        single_dataframe['ATFormPts'] = single_dataframe['ATFormPtsStr'].apply(get_form_points)

        single_dataframe['HTWinStreak3'] = single_dataframe['HTFormPtsStr'].apply(get_3game_ws)
        single_dataframe['HTWinStreak5'] = single_dataframe['HTFormPtsStr'].apply(get_5game_ws)
        single_dataframe['HTLossStreak3'] = single_dataframe['HTFormPtsStr'].apply(get_3game_ls)
        single_dataframe['HTLossStreak5'] = single_dataframe['HTFormPtsStr'].apply(get_5game_ls)

        single_dataframe['ATWinStreak3'] = single_dataframe['ATFormPtsStr'].apply(get_3game_ws)
        single_dataframe['ATWinStreak5'] = single_dataframe['ATFormPtsStr'].apply(get_5game_ws)
        single_dataframe['ATLossStreak3'] = single_dataframe['ATFormPtsStr'].apply(get_3game_ls)
        single_dataframe['ATLossStreak5'] = single_dataframe['ATFormPtsStr'].apply(get_5game_ls)

        src_logger.info(f"Current Columns : {single_dataframe.keys()}")

        # Get Goal Diff

        single_dataframe['HTGD'] = single_dataframe['HTGS'] - single_dataframe['HTGC']
        single_dataframe['ATGD'] = single_dataframe['ATGS'] - single_dataframe['ATGC']

        # Diff in points
        single_dataframe['DiffPts'] = single_dataframe['HTP'] - single_dataframe['ATP']
        single_dataframe['DiffFormPts'] = single_dataframe['HTFormPts'] - single_dataframe['ATFormPts']

        # Scale DiffPts , DiffFormPts, HTGD, ATGD by Matchweek.
        cols = ['HTGD','ATGD','DiffPts','DiffFormPts','HTP','ATP']
        single_dataframe.MW = single_dataframe.MW.astype(float)

        for col in cols:
            single_dataframe[col] = single_dataframe[col] / single_dataframe.MW

        single_dataframe['FTR'] = single_dataframe.FTR.apply(only_hw)

        # Remove the unnecessary columns
        new_single_dataframe = single_dataframe.copy().drop(columns =['Date', 'HomeTeam', 'AwayTeam', 'FTHG', 'FTAG',
          'HTGS', 'ATGS', 'HTGC', 'ATGC',
          'HM4', 'HM5','AM4', 'AM5', 'MW', 'HTFormPtsStr',
          'ATFormPtsStr', 'HTFormPts', 'ATFormPts', 'HTWinStreak3',
          'HTWinStreak5', 'HTLossStreak3', 'HTLossStreak5', 'ATWinStreak3',
          'ATWinStreak5', 'ATLossStreak3', 'ATLossStreak5',
          'DiffPts'])
        
        # Log some of the Analytics 

        # Total number of matches.
        n_matches = new_single_dataframe.shape[0]

        # Calculate number of features. -1 because we are saving one as the target variable (win/lose/draw)
        n_features = new_single_dataframe.shape[1] - 1

        # Calculate matches won by home team.
        n_homewins = len(new_single_dataframe[new_single_dataframe.FTR == 'H'])

        # Calculate win rate for home team.
        win_rate = (float(n_homewins) / (n_matches)) * 100

        # Print the results
        src_logger.info("Total number of matches: {}".format(n_matches))
        src_logger.info("Number of features: {}".format(n_features))
        src_logger.info("Number of matches won by home team: {}".format(n_homewins))
        src_logger.info("Win rate of home team: {:.2f}%".format(win_rate))

        # Separate into feature set and target variable
        #FTR = Full Time Result (H=Home Win, D=Draw, A=Away Win)
        X_all = new_single_dataframe.drop(columns=['FTR'])
        y_all = new_single_dataframe['FTR']

        # Standardising the data.
        from sklearn.preprocessing import scale

        #Center to the mean and component wise scale to unit variance.
        cols = ['HTGD','ATGD','HTP','ATP']
        for col in cols:
            X_all[col] = scale(X_all[col])

        #last 3 wins for both sides
        X_all.HM1 = X_all.HM1.astype('str')
        X_all.HM2 = X_all.HM2.astype('str')
        X_all.HM3 = X_all.HM3.astype('str')
        X_all.AM1 = X_all.AM1.astype('str')
        X_all.AM2 = X_all.AM2.astype('str')
        X_all.AM3 = X_all.AM3.astype('str')

        x_all = preprocess_features(X_all)
        src_logger.info("Processed feature columns ({} total features):\n{}".format(len(X_all.columns), list(X_all.columns)))

        # Combine the processed features and target variable into a single DataFrame
        new_single_dataframe = pd.concat([x_all, y_all], axis=1)
        src_logger.info(f"Transformed DataFrame shape: {new_single_dataframe.shape}")
        src_logger.info(f"Transformed DataFrame columns: {new_single_dataframe.columns.tolist()}")
    
        # Save the transformed data to a CSV file
        is_saved = self.save_transformed_data(new_single_dataframe)

        if is_saved:
            src_logger.info("Transformed data saved successfully.")
            return True
        else:
            src_logger.error("Failed to save transformed data.")
            return False

    def save_transformed_data(self, transformed_data: pd.DataFrame) -> bool:
        """
        Saves the transformed data to the specified path in the configuration.
        Args:
            transformed_data (pd.DataFrame): The transformed data to be saved.
        """
        output_file_path = os.path.join(self.config.root_dir, f"transformed_data_final.csv")

        # If the directory does not exist, create it
        src_logger.info(f"Directory exists: {os.path.exists(self.config.root_dir)}")

        src_logger.info(f"Saving transformed data to {output_file_path}")
        try:
            transformed_data.to_csv(output_file_path, index=False)
            return True
        except Exception as e:
            src_logger.error(f"Error saving transformed data to {output_file_path}: {e}")
            return False
        
    def check_validation_status(self) -> bool:
        """
        Checks the validation status of the transformed data.
        """
        status_file_path = self.config.status_file
        if not os.path.exists(status_file_path):
            src_logger.error(f"Status file {status_file_path} does not exist.")
            return False
        status_dict = read_yaml(status_file_path)
        return status_dict['Validation']

    def get_dataset_path(self) -> Path:
        return Path(self.config.dataset_path)