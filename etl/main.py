from db_connect import get_connection

conn = get_connection()
cur = conn.cursor()

cur.execute("""
insert into staging(
	customer_name,
	amount,
	purchased_date,
	run_id
)
values (
    'ShIfa',
	29000,
	'2026-05-22',
	gen_random_uuid()
);
""")

conn.commit()

print("Row inserted successfully")

cur.close()
conn.close()
