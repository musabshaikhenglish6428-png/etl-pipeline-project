import json
from db_connect import get_connection
from psycopg2.extras import RealDictCursor
def transform_data():
    conn = None
    cur = None
    run_id = None 
    try:
        print("Transformation Started!!")

        conn = get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)

        cur.execute("""
            SELECT * FROM staging
            """
        )
        rows = cur.fetchall()
        
        print("Rows found : ", len(rows))

        passed = 0
        failed = 0

        if not rows:
            print("No rows found in staging")
            cur.close()
            conn.close()
            return
        cur.execute("TRUNCATE processed")
        cur.execute("TRUNCATE failed_rows")
        run_id = rows[0]["run_id"]

        for row in rows:
            failure_reason = []

            if row["region"]:
                row["region"] = row["region"].strip().title()

            if row["sales_rep"]:
                row["sales_rep"] = row["sales_rep"].strip().title()

            if row["customer_type"]:
                row["customer_type"] = row["customer_type"].strip().title()

            if row["payment_method"]:
                row["payment_method"] = row["payment_method"].strip().title()

            if row["sales_channel"]:
                row["sales_channel"] = row["sales_channel"].strip().title()
            
            if row['sales_amount'] <= 0:
                failure_reason.append("Invalid Sales Amount")
            if row["quantity_sold"] <= 0:
                failure_reason.append("Invalid Quantity")
            if not row["region"]:
                failure_reason.append("Missing Region")
            if failure_reason:
                failed += 1
                cur.execute("""
                INSERT INTO failed_rows (
                    raw_data,
                    failure_reason,
                    run_id
                )
                VALUES (
                    %s,
                    %s,
                    %s
                )
                """, (
                    json.dumps(row, default=str),
                    ", ".join(failure_reason),
                    row["run_id"]
                ))
            else:
                cur.execute("""
                INSERT INTO processed (
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
                    %s,%s,%s,%s,%s,
                    %s,%s,%s,%s,%s,
                    %s,%s,%s,%s,%s
                )
                ON CONFLICT ON CONSTRAINT processed_unique 
                DO NOTHING
                """, (
                    row["product_id"],
                    row["sale_date"],
                    row["sales_rep"],
                    row["region"],
                    row["sales_amount"],
                    row["quantity_sold"],
                    row["product_category"],
                    row["unit_cost"],
                    row["unit_price"],
                    row["customer_type"],
                    row["discount"],
                    row["payment_method"],
                    row["sales_channel"],
                    row["region_and_sales_rep"],
                    row["run_id"]
                ))
                if cur.rowcount == 1:
                    passed += 1
        conn.commit()

        print("Passed Rows :", passed)
        print("Failure Rows :", failed)
        cur.execute("""
        UPDATE run_logs
        SET
            rows_processed = %s,
            rows_failed = %s,
            status = 'SUCCESS',
            end_time = CURRENT_TIMESTAMP
        WHERE run_id = %s
        """, (
            passed,
            failed,
            run_id
        ))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:

        print("Error during transformation:", e)

        if conn:
            conn.rollback()

        if conn and cur and run_id:

            cur.execute("""
            UPDATE run_logs
            SET
                status = 'FAILED',
                end_time = CURRENT_TIMESTAMP
            WHERE run_id = %s
            """, (run_id,))

            conn.commit()

        if cur:
            cur.close()

        if conn:
            conn.close()
if __name__ == "__main__":
    transform_data()