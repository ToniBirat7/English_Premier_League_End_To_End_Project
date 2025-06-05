import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from datetime import datetime as dt
from pathlib import Path
from src import src_logger
import os
import itertools

def get_dataframe_from_csv(file_path):
    """
    Load a CSV file into a pandas DataFrame.
    
    Args:
        file_path (str): Path to the CSV file.
        
    Returns:
        pd.DataFrame: DataFrame containing the data from the CSV file.
    """   
    src_logger.info(f"Processing file: {file_path}")
    if not os.path.exists(file_path):
        src_logger.error(f"File {file_path} does not exist.")
        return None
    try:
        df = pd.read_csv(file_path)
        src_logger.info(f"Loaded data from {file_path} successfully.")
        return df
    except Exception as e:
        src_logger.error(f"Error loading data from {file_path}: {e}")
        return None

def get_filename_list(directory_path):
    """
    Get a list of all CSV files in the specified directory.
    
    Args:
        directory_path (str): Path to the directory containing CSV files.
        
    Returns:
        list: A list of file names (without extensions) of all CSV files in the directory.
    """

    file_name_list = [file for file in os.listdir(directory_path) if file.endswith('.csv')]

    return file_name_list

def get_stats_for_dataframe(df):
    """
    Get basic statistics for a pandas DataFrame.
    
    Args:
        df (pd.DataFrame): The DataFrame to analyze.
        
    Returns:
        dict: A dictionary containing basic statistics of the DataFrame.
    """
    columns_req = ['Date','HomeTeam','AwayTeam','FTHG','FTAG','FTR']

    stats = df[columns_req]
    return stats

# Gets the goals scored agg arranged by teams and matchweek

def get_goals_scored(playing_stat):
    # Create a dictionary with team names as keys
    teams = {}
    for i in playing_stat['HomeTeam'].unique():
        teams[i] = []
    
    # the value corresponding to keys is a list containing the match location.
    for i in range(len(playing_stat)):
        HTGS = playing_stat.iloc[i]['FTHG']
        ATGS = playing_stat.iloc[i]['FTAG']
        teams[playing_stat.iloc[i].HomeTeam].append(HTGS)
        teams[playing_stat.iloc[i].AwayTeam].append(ATGS)
    
    # Calculate number of matchweeks based on total matches and teams
    num_teams = len(playing_stat['HomeTeam'].unique())
    matches_per_team = len(teams[list(teams.keys())[0]])
    
    # Create a dataframe for goals scored where rows are teams and cols are matchweek.
    GoalsScored = pd.DataFrame(data=teams, index = [i for i in range(1, matches_per_team + 1)]).T
    GoalsScored[0] = 0
    # Aggregate to get uptil that point
    for i in range(2, matches_per_team + 1):
        GoalsScored[i] = GoalsScored[i] + GoalsScored[i-1]
    return GoalsScored

# Gets the goals conceded agg arranged by teams and matchweek
def get_goals_conceded(playing_stat):
    # Create a dictionary with team names as keys
    teams = {}
    for i in playing_stat['HomeTeam'].unique():
        teams[i] = []
    
    # the value corresponding to keys is a list containing the match location.
    for i in range(len(playing_stat)):
        ATGC = playing_stat.iloc[i]['FTHG']
        HTGC = playing_stat.iloc[i]['FTAG']
        teams[playing_stat.iloc[i].HomeTeam].append(HTGC)
        teams[playing_stat.iloc[i].AwayTeam].append(ATGC)
    
    # Calculate number of matchweeks based on total matches and teams
    num_teams = len(playing_stat['HomeTeam'].unique())
    matches_per_team = len(teams[list(teams.keys())[0]])
    
    # Create a dataframe for goals conceded where rows are teams and cols are matchweek.
    GoalsConceded = pd.DataFrame(data=teams, index = [i for i in range(1, matches_per_team + 1)]).T
    GoalsConceded[0] = 0
    # Aggregate to get uptil that point
    for i in range(2, matches_per_team + 1):
        GoalsConceded[i] = GoalsConceded[i] + GoalsConceded[i-1]
    return GoalsConceded
    
def get_gsc(playing_stat):
    GC = get_goals_conceded(playing_stat)
    GS = get_goals_scored(playing_stat)
   
    j = 0
    HTGS = []
    ATGS = []
    HTGC = []
    ATGC = []

    num_teams = len(playing_stat['HomeTeam'].unique())
    matches_per_round = num_teams // 2
    total_matches = len(playing_stat)

    for i in range(total_matches):
        ht = playing_stat.iloc[i].HomeTeam
        at = playing_stat.iloc[i].AwayTeam
        HTGS.append(GS.loc[ht][j])
        ATGS.append(GS.loc[at][j])
        HTGC.append(GC.loc[ht][j])
        ATGC.append(GC.loc[at][j])
        
        if ((i + 1) % matches_per_round) == 0:
            j = j + 1
        
    playing_stat['HTGS'] = HTGS
    playing_stat['ATGS'] = ATGS
    playing_stat['HTGC'] = HTGC
    playing_stat['ATGC'] = ATGC
    
    return playing_stat

# Gets the points for each match result
# 'W' for win, 'D' for draw, 'L' for loss
# Returns 3 points for win, 1 point for draw, and 0 points for loss
# This function is used to calculate cumulative points for each team in the league

def get_points(result):
    if result == 'W':
        return 3
    elif result == 'D':
        return 1
    else:
        return 0
    
def get_cuml_points(matchres):
    matchres_points = matchres.applymap(get_points)
    # Get the actual number of columns (matchweeks) in the data
    num_matchweeks = len(matchres.columns)
    for i in range(2, num_matchweeks + 1):
        matchres_points[i] = matchres_points[i] + matchres_points[i-1]
    
    # Get the number of teams from the matchres DataFrame
    num_teams = len(matchres)
    matchres_points.insert(column=0, loc=0, value=[0 for i in range(num_teams)])
    return matchres_points

def get_matchres(playing_stat):
    # Create a dictionary with team names as keys
    teams = {}
    for i in playing_stat['HomeTeam'].unique():
        teams[i] = []

    # the value corresponding to keys is a list containing the match result
    for i in range(len(playing_stat)):
        if playing_stat.iloc[i].FTR == 'H':
            teams[playing_stat.iloc[i].HomeTeam].append('W')
            teams[playing_stat.iloc[i].AwayTeam].append('L')
        elif playing_stat.iloc[i].FTR == 'A':
            teams[playing_stat.iloc[i].AwayTeam].append('W')
            teams[playing_stat.iloc[i].HomeTeam].append('L')
        else:
            teams[playing_stat.iloc[i].AwayTeam].append('D')
            teams[playing_stat.iloc[i].HomeTeam].append('D')
    
    # Calculate the actual number of matchweeks based on matches per team
    num_teams = len(playing_stat['HomeTeam'].unique())
    matches_per_team = len(teams[list(teams.keys())[0]])
    
    # Create a dataframe for match results where rows are teams and cols are matchweek
    matchres = pd.DataFrame(data=teams, index=[i for i in range(1, matches_per_team + 1)]).T
    return matchres

def get_agg_points(playing_stat):
    matchres = get_matchres(playing_stat)
    cum_pts = get_cuml_points(matchres)
    HTP = []
    ATP = []
    j = 0
    
    # Calculate matches per round dynamically
    num_teams = len(playing_stat['HomeTeam'].unique())
    matches_per_round = num_teams // 2
    total_matches = len(playing_stat)
    
    for i in range(total_matches):
        ht = playing_stat.iloc[i].HomeTeam
        at = playing_stat.iloc[i].AwayTeam
        HTP.append(cum_pts.loc[ht][j])
        ATP.append(cum_pts.loc[at][j])

        if ((i + 1) % matches_per_round) == 0:
            j = j + 1
            
    playing_stat['HTP'] = HTP
    playing_stat['ATP'] = ATP
    return playing_stat

# Get Team Form 

def get_form(playing_stat,num):
    form = get_matchres(playing_stat)
    form_final = form.copy()
    
    # Calculate the actual number of matchweeks dynamically
    num_teams = len(playing_stat['HomeTeam'].unique())
    matches_per_team = len(playing_stat) // num_teams
    max_matchweeks = matches_per_team + 1  # +1 because we start from matchweek 1
    
    for i in range(num, max_matchweeks):
        form_final[i] = ''
        j = 1
        while j <= num:
            if (i-j) in form.columns:  # Check if column exists
                form_final[i] += form[i-j]
            j += 1           
    return form_final

def add_form(playing_stat,num):
    form = get_form(playing_stat,num)
    
    # Calculate matches per round dynamically
    num_teams = len(playing_stat['HomeTeam'].unique())
    matches_per_round = num_teams // 2
    total_matches = len(playing_stat)
    
    h = ['M' for i in range(num * matches_per_round)]  # since form is not available for n MW
    a = ['M' for i in range(num * matches_per_round)]
    
    j = num
    for i in range((num * matches_per_round), total_matches):
        ht = playing_stat.iloc[i].HomeTeam
        at = playing_stat.iloc[i].AwayTeam
        
        past = form.loc[ht][j]               # get past n results
        if len(past) >= num:
            h.append(past[0])                    # 0 index is most recent (first character)
        else:
            h.append('M')
        
        past = form.loc[at][j]               # get past n results.
        if len(past) >= num:
            a.append(past[0])                   # 0 index is most recent (first character)
        else:
            a.append('M')
        
        if ((i + 1) % matches_per_round) == 0:
            j = j + 1

    playing_stat['HM' + str(num)] = h                 
    playing_stat['AM' + str(num)] = a

    return playing_stat

def add_form_df(playing_statistics):
    playing_statistics = add_form(playing_statistics,1)
    playing_statistics = add_form(playing_statistics,2)
    playing_statistics = add_form(playing_statistics,3)
    playing_statistics = add_form(playing_statistics,4)
    playing_statistics = add_form(playing_statistics,5)
    return playing_statistics

# Rearrange the Columns with the new Columns

def rearrange_columns(df):
    """
    Rearranges the columns of the DataFrame to include new columns for goals scored, goals conceded, points, and form.
    
    Args:
        df (pd.DataFrame): The DataFrame to rearrange.
        
    Returns:
        pd.DataFrame: The rearranged DataFrame with new columns.
    """
    
    cols = ['Date', 'HomeTeam', 'AwayTeam', 'FTHG', 'FTAG', 'FTR', 'HTGS', 'ATGS', 'HTGC', 'ATGC', 'HTP', 'ATP', 'HM1', 'HM2', 'HM3',
        'HM4', 'HM5', 'AM1', 'AM2', 'AM3', 'AM4', 'AM5' ]
    
    new_df = df[cols]
    
    return new_df

# Get Match Week

def get_mw(playing_stat):
    j = 1
    MatchWeek = []
    num_matches = len(playing_stat)
    matches_per_week = 10  # Premier League typically has 10 matches per week
    
    for i in range(num_matches):
        MatchWeek.append(j)
        if ((i + 1) % matches_per_week) == 0:
            j = j + 1
    playing_stat['MW'] = MatchWeek
    return playing_stat

# Identify Win/Loss Streaks if any.

def get_3game_ws(string):
    if string[-3:] == 'WWW':
        return 1
    else:
        return 0
    
def get_5game_ws(string):
    if string == 'WWWWW':
        return 1
    else:
        return 0
    
def get_3game_ls(string):
    if string[-3:] == 'LLL':
        return 1
    else:
        return 0
    
def get_5game_ls(string):
    if string == 'LLLLL':
        return 1
    else:
        return 0
    
# Get the form Points

def get_form_points(string):
    sum = 0
    for letter in string:
        sum += get_points(letter)
    return sum

# Only Home Win

def only_hw(string):
    if string == 'H':
        return 'H'
    else:
        return 'NH'
    
def generate_create_table_sql(df, table_name="final_dataset"):
    dtype_mapping = {
        'int64': 'INT',
        'float64': 'DOUBLE',
        'object': 'VARCHAR(255)',
        'bool': 'BOOLEAN',
        'datetime64[ns]': 'DATETIME',
    }

    columns = []
    for col, dtype in df.dtypes.items():
        col_type = dtype_mapping.get(str(dtype), 'VARCHAR(255)')
        if col == df.columns[0] and col_type in ['INT', 'BIGINT']:
            columns.append(f"{col} {col_type} PRIMARY KEY")
        else:
            columns.append(f"{col} {col_type}")
    
    columns_sql = ",\n    ".join(columns)
    create_table_sql = f"CREATE TABLE IF NOT EXISTS {table_name} (\n    {columns_sql}\n);"
    return create_table_sql