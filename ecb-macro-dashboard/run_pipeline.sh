#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")" && pwd)"
source "$PROJECT_ROOT/venv/bin/activate"

echo "[1/2] Extracting and loading ECB data..."
cd "$PROJECT_ROOT"
python extract/extract_and_load.py

echo "[2/2] Running dbt build..."
cd "$PROJECT_ROOT/dbt_project"
dbt build

echo "Pipeline complete."
