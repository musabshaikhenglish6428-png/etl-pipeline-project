# ETL_DESIGN.md

## Architecture Decisions

### Staging Table

Raw records are first loaded into the staging table before any transformation occurs. This preserves source data and allows reprocessing when business rules change.

### Processed Table

Validated records are written to the processed table. This ensures downstream consumers only access trusted data.

### Failed Rows Table

Invalid records are routed to failed_rows with a failure reason instead of being dropped. This prevents silent data loss and improves auditability.

### Run Logs

Each pipeline execution generates a unique run_id and stores execution metadata such as status, processed rows, failed rows, timestamps, and source file.

### Batch Processing

The pipeline automatically discovers CSV files in the data directory and processes them sequentially. One failed file does not stop the remaining files from being processed.

### Idempotency

Duplicate records are prevented using database unique constraints and ON CONFLICT DO NOTHING logic. Previously processed files are skipped using run_logs state checks.

### Logging

Pipeline activity is recorded in pipeline.log using Python logging. Execution metrics are additionally stored in run_logs for operational monitoring.

## Known Limitation

Transform batch metrics are currently attributed to the first run_id in a batch. Future versions may process run_ids individually or introduce batch-level tracking.