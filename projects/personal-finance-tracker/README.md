# Personal Finance Tracker

A command-line personal finance tracker built with Python and SQLite. It records income and expenses, categorises transactions, and produces a date-independent category summary.

## Features
- Add income and expense transactions with validation.
- List recent transactions.
- View totals and category breakdowns.
- Store data locally in SQLite (no account or cloud service required).

## Requirements
Python 3.10+; no third-party packages.

## Run
```bash
python -m finance_tracker --help
python -m finance_tracker add --kind expense --amount 85.50 --category Transport --note "Taxi"
python -m finance_tracker add --kind income --amount 2500 --category Allowance --note "Monthly allowance"
python -m finance_tracker list
python -m finance_tracker summary
```

The database is created at `finance.db` in the current working directory. Use `--db path/to/file.db` to choose another location.

## Tests
```bash
python -m unittest discover -s tests -v
```

This is an educational local tracker, not a bank integration, accounting system or financial advice.
