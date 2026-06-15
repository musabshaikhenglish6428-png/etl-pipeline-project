# INTERVIEW_NOTES.md

# Project Overview

Production-grade ETL pipeline built using Python, PostgreSQL, pandas and Docker.

Pipeline Flow:

CSV Files
→ Extract
→ Staging
→ Transform
→ Processed / Failed Rows
→ Run Logs

Project Goal:

Build an ETL system that simulates real-world enterprise data workflows including data ingestion, validation, auditing, logging, batch processing, error handling, and idempotent execution.

---

# Architecture Decisions

## Why Staging Exists

Initial Understanding

Just another table before processed.

What I Learned

Staging preserves raw source data before any business rules are applied.

Benefits

* Original data remains untouched
* Reprocessing becomes possible
* Easier debugging
* Clear separation between ingestion and transformation

Interview Answer

Staging acts as the raw landing zone. It separates ingestion from transformation and preserves source data for auditing and reprocessing.

---

## Why Processed Exists

Initial Understanding

Could directly load data into final tables.

What I Learned

Business users should only consume trusted and validated records.

Benefits

* Clean data layer
* Consistent reporting
* Better downstream reliability

Interview Answer

Processed contains only validated records that successfully pass transformation and business rules.

---

## Why Failed Rows Exists

Initial Understanding

Bad records should simply be removed.

What I Learned

Dropping records silently is dangerous because it hides data quality issues.

Benefits

* No silent data loss
* Easier debugging
* Better auditability
* Supports future correction and reprocessing

Interview Answer

Invalid records are quarantined into failed_rows with a failure reason instead of being discarded.

---

## Why Run Logs Exists

Initial Understanding

pipeline.log should be enough.

What I Learned

Logs and metadata solve different problems.

Benefits

* Run tracking
* Monitoring
* SQL-based reporting
* Auditing

Interview Answer

run_logs stores structured execution metadata such as run_id, timestamps, status, row counts, source file, and error information.

---

# pipeline.log vs run_logs

## pipeline.log

Purpose

Human-readable execution history.

Contains

* INFO messages
* WARNING messages
* ERROR messages
* Detailed execution steps

Used For

* Debugging
* Troubleshooting
* Operational investigation

---

## run_logs

Purpose

Structured metadata.

Contains

* run_id
* source_file
* status
* start_time
* end_time
* rows_processed
* rows_failed
* error_message

Used For

* Monitoring
* Reporting
* Auditing
* Operational tracking

Interview Answer

pipeline.log provides detailed execution history while run_logs provides structured metadata that can be queried through SQL.

---

# Why UUID run_id Was Used

Initial Understanding

Could use integers.

What I Learned

Every execution must be uniquely identifiable.

Benefits

* No collision risk
* Better traceability
* Easier auditing

Interview Answer

UUID provides globally unique execution identifiers and simplifies tracking pipeline runs.

---

# ON CONFLICT DO NOTHING

Initial Understanding

Just PostgreSQL syntax.

What I Learned

It is one of the key mechanisms behind idempotency.

Benefits

* Duplicate prevention
* Safe reruns
* Cleaner data

Interview Answer

ON CONFLICT DO NOTHING prevents duplicate inserts when a record already exists according to the unique constraint.

---

# Why Unique Constraints Matter

Initial Understanding

Validation should happen in Python.

What I Learned

The database should also protect data integrity.

Benefits

* Second layer of defense
* Duplicate prevention
* Data quality enforcement

Interview Answer

Unique constraints ensure duplicate records cannot enter the system even if application logic fails.

---

# Idempotency

Initial Understanding

Industry buzzword.

What I Learned

A pipeline should produce the same result even when executed multiple times.

How It Was Achieved

* Database unique constraints
* ON CONFLICT DO NOTHING
* File tracking through run_logs
* Skip already processed files

Interview Answer

The pipeline can be safely rerun without generating duplicate records.

---

# Batch Processing

Initial Understanding

One CSV file is enough.

What I Learned

Production systems process many files regularly.

Implementation

main.py

* Discovers CSV files
* Processes files sequentially
* Generates run_id per file
* Maintains execution history

Benefits

* Scalability
* Automation
* Better operational workflow

Interview Answer

The pipeline supports processing multiple source files in a single execution while maintaining traceability.

---

# File-Level Failure Isolation

Initial Understanding

One error should stop everything.

What I Learned

A single bad file should not block an entire batch.

Implementation

Each file is wrapped in its own try/except block.

Benefits

* Higher reliability
* Partial success
* Better fault tolerance

Interview Answer

Failures are isolated to individual files so the remaining files continue processing successfully.

---

# Why Source File Tracking Was Added

Initial Design

run_logs only tracked run_id.

Problem

Could not determine which file generated a specific run.

Final Design

Added source_file column.

Benefits

* Better auditing
* Easier troubleshooting
* Improved traceability

Interview Answer

Each run can be traced back to its original source file.

---

# Why Skip Logic Was Added

Initial Design

Process every file every time.

Problem

Repeated executions waste resources.

Final Design

Check run_logs before processing.

Benefits

* Faster execution
* Less database work
* Better operational efficiency

Interview Answer

Previously processed files are skipped using run_logs state checks.

---

# Biggest Debugging Sessions

## TRUNCATE Confusion

Problem

I truncated staging and processed tables but the pipeline still skipped files.

Root Cause

run_logs was controlling processing state.

Lesson

Always identify the true source of business logic.

---

## Multi-run_id Confusion

Problem

Three files produced three run_ids but transform displayed only one run_id.

Root Cause

Transform used:

run_id = rows[0]["run_id"]

Lesson

Working code can still contain architectural limitations.

Future Improvement

Process run_ids individually or introduce batch-level tracking.

---

## logging Not Defined Error

Problem

Pipeline failed with:

name 'logging' is not defined

Root Cause

Forgot to import logging.

Lesson

Not all failures are complex. Simple mistakes cause real failures too.

---

## Pull Request Confusion

Problem

Thought creating a pull request automatically merged code.

What I Learned

PR creation and PR merging are separate actions.

Lesson

Understand the Git workflow instead of memorizing commands.

---

# Concepts I Didn't Understand Initially

## Schema

Before

Just table definitions.

After

A contract between application code and the database.

---

## Staging

Before

An extra table.

After

A raw landing zone for preserving source data.

---

## Idempotency

Before

An industry buzzword.

After

The ability to safely rerun pipelines.

---

## Pull Requests

Before

Another Git feature.

After

A code review and collaboration workflow.

---

## Logging

Before

Replacement for print().

After

A critical operational tool for monitoring and debugging.

---

# Decisions I Am Proud Of

* Added batch processing
* Added source_file tracking
* Added UUID run tracking
* Implemented idempotency
* Added structured logging
* Added file-level failure isolation
* Used failed_rows instead of dropping records
* Added run_logs auditing
* Used unique constraints for data protection

---

# Questions Interviewers May Ask

Why use a staging table?

Why store failed records?

Why PostgreSQL?

Why UUID instead of integers?

How is idempotency achieved?

How are duplicates prevented?

How does batch processing work?

What happens when one file fails?

What does run_logs track?

How would you improve the project?

What challenges did you face?

What was the most difficult bug?

Why use structured logging?

How do you ensure data quality?

---

# Questions I Can Ask Interviewers

How does your team validate incoming data?

How do you handle pipeline failures?

How do you manage schema changes?

What orchestration tools do you use?

How do you handle reprocessing historical data?

How do you monitor ETL jobs?

What is your deployment workflow for data pipelines?

---

# If I Rebuilt This Project Today

1. Add foreign key relationships.

2. Process run_ids individually during transformation.

3. Add Docker implementation from the beginning.

4. Introduce environment-specific configuration management.

5. Add automated scheduling.

6. Add CI/CD pipeline integration.

7. Separate business rules from transformation code.

8. Add monitoring dashboards.

9. Add cloud storage integration.

10. Add automated testing earlier in development.

---

# Key Lessons Learned

The biggest lesson from this project is that data engineering is not primarily about writing code.

It is about:

* Data quality
* Reliability
* Traceability
* Auditability
* Recoverability
* Operational visibility

A pipeline that works once is easy.

A pipeline that can be rerun safely, debugged quickly, audited later, and trusted by users is much harder to build.

This project taught me the difference between writing scripts and designing systems.
