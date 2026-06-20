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
- Containerized using Docker and Docker Compose

CSV Files
    │
    ▼
Extract Layer (Python)
    │
    ▼
Staging Table (PostgreSQL)
    │
    ▼
Transform Layer
    │
 ┌──┴─────┐
 ▼        ▼
Processed Failed Rows
 Table     Table
    │
    ▼
Run Logs


## Tech Stack

- Python
- PostgreSQL
- pandas
- psycopg2
- Docker
- Docker Compose

## Project Highlights

- Processed 1000+ sales records
- Implemented Run ID based batch tracking
- Built a Dockerized PostgreSQL environment
- Designed staging and processed table architecture
- Added error handling and logging mechanisms
- Followed modular ETL design principles

## Run

python scripts/main.py

## Sprint 6: Completed

Known limitation:
Transform batch metrics are attributed to the first run_id in the batch.

## Future Enhancements

- Apache Airflow orchestration
- Incremental loading
- Slowly Changing Dimensions (SCD)
- Data quality framework
- AWS deployment
- Automated testing pipeline


