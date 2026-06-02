import pandas as pd 

df = pd.read_csv(r"C:\Users\DELL\OneDrive\Desktop\Project\data\sales_data.csv")

print(df.shape)
print(df.isnull().sum())
print(df.info())
print("Rows:", len(df))
print("Columns:", len(df.columns))
print("COlumns : " ,df.columns.tolist())
