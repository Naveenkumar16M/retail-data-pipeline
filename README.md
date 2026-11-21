# Retail Data ETL Pipeline

## Project Overview

A Python-based ETL pipeline that extracts retail order data from CSV, validates data quality, separates rejected records, and loads valid transactions into a SQLite database.

## Technologies Used

- Python
- Pandas
- SQLite
- Python Logging
- Git and GitHub

## ETL Workflow

1. **Extract:** Read raw retail orders from `data/order.csv`.
2. **Validate:** Identify missing quantities, missing customer IDs, negative prices, and duplicate order IDs.
3. **Transform:** Separate valid and rejected records and record validation failure reasons.
4. **Load:** Insert valid records into SQLite using `executemany()`.
5. **Verify:** Check database row counts and prevent duplicate primary-key inserts.
6. **Error Handling:** Use exception handling, logging, transactions, and rollback.

## Sample Results

| Metric | Count |
|---|---:|
| Source records | 11 |
| Valid records | 7 |
| Rejected records | 4 |
| Records stored in SQLite | 7 |

## How to Run

Install the required dependency:

```bash
python -m pip install pandas
```

From the project root, execute:

```bash
python src/pipeline.py
```

The pipeline generates validated CSV files, loads valid records into SQLite, and writes execution logs to `logs/etl.log`.

## Key Features

- Data quality validation
- Rejected record tracking
- Bulk SQLite loading
- Duplicate prevention on reruns
- Transaction rollback
- Error logging
- Automated extraction and loading

## Future Improvements

- Automated unit testing
- Configurable file paths
- More comprehensive data validation
- Cloud-based data storage