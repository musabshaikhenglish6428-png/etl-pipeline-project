CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE staging (
    id SERIAL PRIMARY KEY,

    product_id INTEGER,
    sale_date DATE,

    sales_rep TEXT,
    region TEXT,

    sales_amount NUMERIC(12,2),
    quantity_sold INTEGER,

    product_category TEXT,

    unit_cost NUMERIC(12,2),
    unit_price NUMERIC(12,2),

    customer_type TEXT,
    discount NUMERIC(5,2),

    payment_method TEXT,
    sales_channel TEXT,

    region_and_sales_rep TEXT,

    run_id UUID,
    loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ---Alter Table staging ADD CONSTRAINT unique_sale....;
    CONSTRAINT unique_sale UNIQUE (
        product_id,
        sale_date,
        sales_rep,
        sales_amount,
        quantity_sold
    )
);

CREATE TABLE processed (
    id SERIAL PRIMARY KEY,

    product_id INTEGER,
    sale_date DATE,

    sales_rep TEXT,
    region TEXT,

    sales_amount NUMERIC(12,2),
    quantity_sold INTEGER,

    product_category TEXT,

    unit_cost NUMERIC(12,2),
    unit_price NUMERIC(12,2),

    customer_type TEXT,
    discount NUMERIC(5,2),

    payment_method TEXT,
    sales_channel TEXT,

    region_and_sales_rep TEXT,

    run_id UUID,
    processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ---Alter Table processed ADD CONSTRAINT processed_unique....;
    CONSTRAINT processed_unique UNIQUE (
        product_id,
        sale_date,
        sales_rep,
        sales_amount,
        quantity_sold
    )
);

CREATE TABLE failed_rows (
    id SERIAL PRIMARY KEY,

    raw_data JSONB,
    failure_reason TEXT,

    run_id UUID,

    failed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE run_logs (
    run_id UUID PRIMARY KEY,

    start_time TIMESTAMP,
    end_time TIMESTAMP,

    status TEXT,

    rows_processed INTEGER,
    rows_failed INTEGER,

    error_message TEXT
);

ALTER TABLE run_logs
ADD COLUMN source_file TEXT;