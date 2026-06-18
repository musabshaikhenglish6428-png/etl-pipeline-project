# ETL Pipeline Project

Production-grade ETL pipeline built using Python, PostgreSQL and Docker.

## Features

- Extract CSV data using pandas
- Load raw data into PostgreSQL staging table
- Transform and validate records
- Route failed records to failed_rows
- Batch processing of multiple CSV files
- Unique run_id tracking
- Structured logging
- Idempotent processing
- File-level failure isolation

## Tech Stack

- Python
- PostgreSQL
- pandas
- psycopg2
- Docker
- Docker Compose

## Pipeline Flow

CSV Files
→ Extract
→ Staging Table
→ Transform
→ Processed Table
→ Failed Rows
→ Run Logs

## Run

python scripts/main.py

## Sprint 6: Complete
Known limitation:
Transform batch metrics are attributed to the first run_id in the batch.