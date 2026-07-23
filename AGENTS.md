# Project Overview

This project is a production-style AWS Data Engineering pipeline.

## Tech Stack

- Python 3.13.9
- AWS Lambda
- Amazon S3
- EventBridge
- Snowflake
- PySpark
- Docker
- GitHub

## Coding Standards

- Use Python type hints.
- Use logging instead of print().
- Never hardcode secrets.
- Read configuration from environment variables.
- Keep functions small and focused.
- Handle exceptions with meaningful log messages.
- Follow PEP 8.
- Add docstrings for public functions.
- Write modular, reusable code.
- Prefer pathlib over os.path where practical.

## Architecture

API
→ Lambda
→ S3
→ PySpark
→ Snowflake
→ Power BI

## When making changes

- Do not break existing functionality.
- Explain architectural changes before implementing them.
- Keep code production-ready.
- Prefer readability over clever code.
