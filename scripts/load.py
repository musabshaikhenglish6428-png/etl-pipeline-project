from db_connect import get_connection
import pandas as pd
import uuid

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

    df = pd.read_csv(r"C:\Users\DELL\OneDrive\Desktop\Project\data\sales_data.csv")

    print("Run_ID:", run_id)
    print("Rows:", len(df))
    
    print("Connected")

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
    """, (len(df), run_id))

    conn.commit()

    cur.close()
    conn.close()

except Exception as e:

    print("FAILURE LOGIC:", e)

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