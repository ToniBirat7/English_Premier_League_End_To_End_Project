from pandas.plotting import scatter_matrix

def get_scatter_matrix(df):
    """
    Generate a scatter matrix for the given dataset.
    
    Parameters:
    dataset2 (pd.DataFrame): The dataset containing the columns to visualize.
    
    Returns:
    None: Displays the scatter matrix plot.
    """
    # Create and return the scatter matrix plot so that we can append it to the list of plots
    return scatter_matrix(df[['HTGD','ATGD','HTP','ATP','DiffFormPts']], figsize=(15,15))

def get_correlation_matrix(df):
    """
    Generate a correlation matrix for the given dataset.
    
    Parameters:
    df (pd.DataFrame): The dataset containing the columns to visualize.
    
    Returns:
    None: Displays the correlation matrix plot.
    """
    # Create and return the correlation matrix plot so that we can append it to the list of plots
    return df.corr().style.background_gradient(cmap='coolwarm').set_precision(2)


