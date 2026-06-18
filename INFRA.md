# Infrastructure Overview

## Services

- Python ETL container
- PostgreSQL container

## Docker Volumes

- ./data:/app/data
- ./logs:/logs

## Environment Variables

- LOG_LEVEL
- POSTGRES_USER
- POSTGRES_PASSWORD
- POSTGRES_DB

## Health Check

PostgreSQL health check ensures Python starts only after the database is ready.

## Restart Policy

Python service uses `on-failure:3`.