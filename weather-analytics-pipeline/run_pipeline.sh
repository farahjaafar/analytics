#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")" && pwd)"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

# Activate virtual environment
source "$PROJECT_ROOT/venv/bin/activate"

log "=== Weather Analytics Pipeline starting ==="

# Step 1: Extract and load into DuckDB
log "--- Step 1: Extracting and loading into DuckDB ---"
cd "$PROJECT_ROOT"
python3 extract/load_to_duckdb.py
log "--- Step 1: Extract + load complete ---"

# Step 2: Run dbt build (models + tests)
log "--- Step 2: Running dbt build ---"
cd "$PROJECT_ROOT/dbt_project"
dbt build
log "--- Step 2: dbt build complete ---"

log "=== Pipeline finished successfully ==="
