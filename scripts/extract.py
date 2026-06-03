import pandas as pd
import os

def extract_data():

    csv_path = os.path.join(
        os.path.dirname(__file__),
        "..",
        "data",
        "sales_data.csv"
    )

    return pd.read_csv(csv_path)