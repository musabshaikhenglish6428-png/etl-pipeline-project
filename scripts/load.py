import uuid
import logging
import os

from db_connect import get_connection
from extract import extract_data

def is_file_processed(file_name):
    """
    Checks whether a source file has already
    been processed successfully
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
    SELECT 1
    FROM run_logs
    WHERE source_file = %s
    AND status = 'SUCCESS'
    LIMIT 1
    """, (file_name,))
    result = cur.fetchone()

    cur.close()
    conn.close()

    return result is not None
print(is_file_processed("sales_jan.csv"))

def load_data(csv_path):
    """
    Loads source CSV records into the staging table and
    Tracks execution metadata in run_logs
    """
    conn = None
    cur = None

    run_id = str(uuid.uuid4())

    logging.info("Load Started")
    logging.info(f"Run ID : {run_id}")

    source_file = os.path.basename(csv_path)
    logging.info(f"Source File : {source_file}")
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
        INSERT INTO run_logs (
            run_id,
            source_file,
            start_time,
            status,
            rows_processed,
            rows_failed
        )
        VALUES (
            %s,
            %s,
            CURRENT_TIMESTAMP,
            'RUNNING',
            0,
            0
        )
        """, (run_id, source_file))

        conn.commit()

        df = extract_data(csv_path)

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

        
        logging.info(f"Rows : {len(df)}")
        logging.info("Database Connected")

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
        logging.info(f"Rows Inserted : {rows_inserted}")
        logging.info("All rows loaded into staging")

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

        logging.error(f"Load Failed : {e}")
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

        raise