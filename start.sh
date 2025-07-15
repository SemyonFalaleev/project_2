#!/bin/bash
set -e

echo "Alembic starting..."
poetry run alembic upgrade head

echo "FastAPI starting..."
poetry run uvicorn src.main:app --host 0.0.0.0 --port 8000