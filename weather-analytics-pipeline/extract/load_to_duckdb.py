"""
load_to_duckdb.py — Loads raw weather data into a DuckDB database.

WHAT THIS SCRIPT DOES:
1. Calls fetch_weather.py to get weather data from the API
2. Creates a DuckDB database file (if it doesn't exist)
3. Creates a raw schema and table
4. Inserts all rows into the table

USAGE:
    python extract/load_to_duckdb.py

    # This will:
    #   1. Fetch data from Open-Meteo API
    #   2. Create data/weather.duckdb
    #   3. Load all rows into raw_weather.daily_weather
"""

import duckdb
import os
# import pandas as pd
from pathlib import Path
from dotenv import load_dotenv

from fetch_weather import fetch_all_cities
from config import RAW_SCHEMA, RAW_TABLE


def get_duckdb_connection():
    """
    Create a connection to the DuckDB database.

    DuckDB is a file-based database. When connect to a path like
    'data/weather.duckdb', it creates that file if it doesn't exist.
    All the tables, schemas, and data live in that single file.
    """

    # Load environment variables from .env file
    project_root = Path(__file__).resolve().parent.parent
    load_dotenv(dotenv_path=project_root / ".env")

    db_path = Path(os.getenv("DUCKDB_PATH", "data/weather.duckdb"))
    if not db_path.is_absolute():
        db_path = project_root / db_path

    # Create the directory if it doesn't exist
    db_path.parent.mkdir(parents=True, exist_ok=True)
    db_path = str(db_path)

    print(f"Connecting to DuckDB at: {db_path}")
    return duckdb.connect(db_path)


def create_raw_table(conn):
    """
    Create the schema and table for raw weather data.

    WHY A RAW SCHEMA?
    Follow the ELT pattern:
      Extract: pull data from API (fetch_weather.py)
      Load: dump it as-is into the warehouse (this script)
      Transform: clean and reshape it (dbt does this next)

    The raw schema holds untouched data. If a dbt transformation
    has a bug, can always go back to the original.
    """

    print(f"Creating schema: {RAW_SCHEMA}")
    conn.execute(f"CREATE SCHEMA IF NOT EXISTS {RAW_SCHEMA}")

    # --------------------------------------------------------
    # DROP and recreate the table on each run (full refresh)
    # --------------------------------------------------------
    # For a first project, full refresh is simpler and less error-prone.
    # Later, can switch to incremental loading (only insert new rows)
    # which is more efficient for large datasets.
    # --------------------------------------------------------

    print(f"Creating table: {RAW_SCHEMA}.{RAW_TABLE}")
    conn.execute(f"DROP TABLE IF EXISTS {RAW_SCHEMA}.{RAW_TABLE}")

    conn.execute(f"""
        CREATE TABLE {RAW_SCHEMA}.{RAW_TABLE} (
            city                        VARCHAR,
            country_code                VARCHAR,
            latitude                    DOUBLE,
            longitude                   DOUBLE,
            date                        DATE,
            temperature_2m_max          DOUBLE,
            temperature_2m_min          DOUBLE,
            temperature_2m_mean         DOUBLE,
            precipitation_sum           DOUBLE,
            rain_sum                    DOUBLE,
            snowfall_sum                DOUBLE,
            windspeed_10m_max           DOUBLE,
            sunrise                     VARCHAR,
            sunset                      VARCHAR,
            daylight_duration           DOUBLE,
            relative_humidity_2m_mean   DOUBLE,
            extracted_at                TIMESTAMP
        )
    """)


def load_data(conn, rows):
    """
    Insert fetched weather data into DuckDB.

    Skip pandas entirely and insert rows directly using
    DuckDB's executemany(). This avoids type detection issues
    between pandas and DuckDB.
    """

    if not rows:
        print("No rows to load. Check extraction.")
        return

    # --------------------------------------------------------
    # Insert rows directly using parameterized SQL.
    # executemany() takes a SQL template and a list of tuples,
    # inserting one row per tuple. This is slower than pandas
    # for millions of rows, but for ~3000 rows it's instant
    # and avoids all type conversion headaches.
    # --------------------------------------------------------
    insert_sql = f"""
        INSERT INTO {RAW_SCHEMA}.{RAW_TABLE}
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """

    tuples = [
        (
            row["city"],
            row["country_code"],
            row["latitude"],
            row["longitude"],
            row["date"],
            row["temperature_2m_max"],
            row["temperature_2m_min"],
            row["temperature_2m_mean"],
            row["precipitation_sum"],
            row["rain_sum"],
            row["snowfall_sum"],
            row["windspeed_10m_max"],
            row["sunrise"],
            row["sunset"],
            row["daylight_duration"],
            row["relative_humidity_2m_mean"],
            row["extracted_at"],
        )
        for row in rows
    ]

    conn.executemany(insert_sql, tuples)

    print(f"Loaded {len(rows)} rows into {RAW_SCHEMA}.{RAW_TABLE}")

def verify_load(conn):
    """
    Run a quick sanity check after loading data.

    Always verify data loads! This catches issues early
    before dbt tries to transform bad data.
    """

    print("\n--- Data Verification ---")

    # Total row count
    result = conn.execute(
        f"SELECT COUNT(*) FROM {RAW_SCHEMA}.{RAW_TABLE}"
    ).fetchone()
    print(f"Total rows: {result[0]}")

    # Rows per city — shows date range and count for each city
    result = conn.execute(f"""
        SELECT
            city,
            COUNT(*) as days,
            MIN(date) as from_date, MAX(date) as to_date
        FROM {RAW_SCHEMA}.{RAW_TABLE}
        GROUP BY city
        ORDER BY city
    """).fetchall()

    print("\nRows per city:")
    for city, count, from_date, to_date in result:
        print(f"  {city}: {count} days ({from_date} to {to_date})")

    # Check for nulls in critical columns
    result = conn.execute(f"""
        SELECT
            COUNT(*) FILTER (WHERE temperature_2m_mean IS NULL) as null_temps,
            COUNT(*) FILTER (WHERE precipitation_sum IS NULL) as null_precip
        FROM {RAW_SCHEMA}.{RAW_TABLE}
    """).fetchone()
    print(f"\nNull checks: temp={result[0]} nulls, precip={result[1]} nulls")
    print("--- Done ---\n")


# ============================================================
# Main execution
# ============================================================

if __name__ == "__main__":
    # Step 1: Fetch data from API
    print("=" * 60)
    print("STEP 1: Fetching weather data from Open-Meteo API")
    print("=" * 60)
    rows = fetch_all_cities()

    # Step 2: Connect to DuckDB and load the data
    print("\n" + "=" * 60)
    print("STEP 2: Loading data into DuckDB")
    print("=" * 60)
    conn = get_duckdb_connection()
    create_raw_table(conn)
    load_data(conn, rows)

    # Step 3: Verify the load
    verify_load(conn)

    # Clean up
    conn.close()
    print("Pipeline complete! Run 'cd dbt_project && dbt run' next.")