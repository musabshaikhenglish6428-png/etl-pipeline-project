from db_connect import get_connection
import pandas as pd 
import uuid 

df = pd.read_csv(r"C:\Users\DELL\OneDrive\Desktop\Project\data\sales_data.csv")

run_id = str(uuid.uuid4())

print("Run_ID : ",run_id)
print("COlumns : ",len(df))

conn = get_connection()
cur = conn.cursor()
print("connected")
row = df.iloc[0]

for _, row in df.iterrows():

    cur.execute("""
    INSERT INTO staging (
        product_id,
        sale_date,
        sales_rep,
        region,
        sales_amount,
        quantity_sold,
        product_category,
        unit_cost,
        unit_price,
        customer_type,
        discount,
        payment_method,
        sales_channel,
        region_and_sales_rep,
        run_id
    )
    VALUES (
        %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s
    )
    """, (
        int(row["Product_ID"]),
        row["Sale_Date"],
        row["Sales_Rep"],
        row["Region"],
        float(row["Sales_Amount"]),
        int(row["Quantity_Sold"]),
        row["Product_Category"],
        float(row["Unit_Cost"]),
        float(row["Unit_Price"]),
        row["Customer_Type"],
        float(row["Discount"]),
        row["Payment_Method"],
        row["Sales_Channel"],
        row["Region_and_Sales_Rep"],
        run_id
    ))

conn.commit()

print("All rows loaded into staging")

cur.close()
conn.close()