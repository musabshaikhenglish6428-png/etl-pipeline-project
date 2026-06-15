import pandas as pd

def extract_data(csv_path):
    """
    Reads source CSV data into a pandas Dataframe
    """

    return pd.read_csv(csv_path)