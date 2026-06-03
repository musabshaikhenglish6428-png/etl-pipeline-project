from db_connect import get_connection
import pandas as pd
import uuid
from extract import extract_data

conn = None
cur = None

run_id = str(uuid.uuid4())

try:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
    INSERT INTO run_logs (
        run_id,
        start_time,
        status,
        rows_processed,
        rows_failed
    )
    VALUES (
        %s,
        CURRENT_TIMESTAMP,
        'RUNNING',
        0,
        0
    )
    """, (run_id,))

    conn.commit()

    df = extract_data()

    required_columns = [
    "Product_ID",
    "Sale_Date",
    "Sales_Rep",
    "Region",
    "Sales_Amount",
    "Quantity_Sold",
    "Product_Category",
    "Unit_Cost",
    "Unit_Price",
    "Customer_Type",
    "Discount",
    "Payment_Method",
    "Sales_Channel",
    "Region_and_Sales_Rep"
]
    missing_columns = []

    for column in required_columns:
        if column not in df.columns:
            missing_columns.append(column)
    if missing_columns:
        raise Exception(f"Missing columns: {missing_columns}")
    print("Run_ID:", run_id)
    print("Rows:", len(df))
    
    print("Connected")
    rows_inserted = 0
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
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s
        )
        ON CONFLICT (
            product_id,
            sale_date,
            sales_rep,
            sales_amount,
            quantity_sold
        )
        DO NOTHING
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
    
    rows_inserted += cur.rowcount    
    conn.commit()

    cur.execute("""
    UPDATE run_logs
    SET
        end_time = CURRENT_TIMESTAMP,
        status = 'SUCCESS'
    WHERE run_id = %s
    """, (run_id,))

    conn.commit()

    print("All rows loaded into staging")

    cur.execute("""
    UPDATE run_logs
    SET
        end_time = CURRENT_TIMESTAMP,
        status = 'SUCCESS',
        rows_processed = %s
    WHERE run_id = %s
    """, (rows_inserted ,run_id))

    conn.commit()

    cur.close()
    conn.close()

except Exception as e:

    print("FAILURE LOGIC:", e)
    if conn:
        conn.rollback()
        
    if conn and cur:

        cur.execute("""
        UPDATE run_logs
        SET
            end_time = CURRENT_TIMESTAMP,
            status = 'FAILED',
            rows_failed = 1
        WHERE run_id = %s
        """, (run_id,))

        conn.commit()

        cur.close()
        conn.close()