
"""
extract_and_load.py — Fetch ECB data and load into DuckDB.

For each data domain (inflation, interest rates, exchange rates,
money supply, bond yields):
  1. Build the SDMX series key from config.py
  2. Call the ECB Data Portal API (CSV format)
  3. Save the raw CSV to data/raw/
  4. Load the CSV into DuckDB using read_csv_auto

Usage:
    source venv/bin/activate
    python extract/extract_and_load.py
"""

import os
import requests
import duckdb
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from config import (
    ECB_API_BASE,
    COUNTRIES,
    INFLATION_COMPONENTS,
    INFLATION_SERIES_PATTERN,
    INTEREST_RATE_SERIES,
    EXCHANGE_RATE_SERIES,
    M3_SERIES,
    BOND_YIELD_SERIES,
    MONTHLY_START,
    DAILY_START,
    DUCKDB_PATH,
    RAW_SCHEMA,
    TABLE_NAMES,
)


def _build_session() -> requests.Session:
    """
    Create a requests Session with automatic retries.

    Why retries? The ECB API is reliable, but your home Wi-Fi might
    hiccup, or the server might return a transient 503. Rather than
    crashing on the first glitch, we retry up to 3 times with
    exponential backoff (1s, 2s, 4s wait between retries).
    """
    session = requests.Session()
    retry = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[500, 502, 503, 504],
        allowed_methods=["GET"],
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    return session

def fetch_series(series_key: str, start_period: str, output_file: str) -> None:
    """
    Fetch a single SDMX series (or multi-series with +) from the ECB API
    and save the raw CSV response to disk.

    Args:
        series_key:   The full SDMX key, e.g. "ICP.M.DE+FR.N.000000.4.ANR"
        start_period: Start date — "2000-01" for monthly, "2000-01-01" for daily
        output_file:  Where to save the CSV, e.g. "data/raw/inflation.csv"
    """
    # The series key contains the dataflow as the first segment.
    # e.g., "ICP.M.DE.N.000000.4.ANR" → dataflow = "ICP"
    # But the URL needs it separated: /service/data/ICP/M.DE.N.000000.4.ANR
    # So we split on the first dot.
    dataflow, key_remainder = series_key.split(".", 1)

    url = f"{ECB_API_BASE}/{dataflow}/{key_remainder}"
    params = {
        "startPeriod": start_period,
        "detail": "dataonly",
        "format": "csvdata",
    }

    print(f"  Fetching {output_file}...")
    session = _build_session()
    response = session.get(url, params=params, timeout=60)
    response.raise_for_status()

    # Build absolute path relative to the project root (one level up from extract/)
    project_root = os.path.join(os.path.dirname(__file__), "..")
    abs_output_file = os.path.join(project_root, output_file)

    os.makedirs(os.path.dirname(abs_output_file), exist_ok=True)
    with open(abs_output_file, "w") as f:
        f.write(response.text)

    # Count rows for feedback (subtract 1 for the header)
    row_count = response.text.count("\n") - 1
    print(f"    Saved {row_count} rows to {output_file}")


def fetch_inflation() -> None:
    """
    Fetch HICP inflation data for all countries and components.

    Uses the "+" operator to request all countries in one call per component.
    E.g., ICP.M.DE+FR+ES+IT+NL+U2.N.000000.4.ANR fetches headline
    inflation for all 6 countries at once.
    """
    # Join country codes with "+" for a multi-country request
    country_group = "+".join(COUNTRIES)

    # Similarly, join all component codes with "+"
    item_group = "+".join(INFLATION_COMPONENTS.values())

    # Build the full series key using the pattern from config.py
    series_key = INFLATION_SERIES_PATTERN.format(
        country=country_group,
        item=item_group,
    )

    fetch_series(series_key, MONTHLY_START, f"data/raw/{TABLE_NAMES['inflation']}.csv")


def fetch_interest_rates() -> None:
    """
    Fetch ECB key interest rates (MRR, DFR, MLFR).

    Each rate is a separate series key, but we can combine them with "+"
    by extracting the varying part. However, the full keys have different
    structures, so it's simpler to fetch them separately and concatenate.

    Actually — looking at the keys:
      FM.D.U2.EUR.4F.KR.MRR_RT.LEV
      FM.D.U2.EUR.4F.KR.DFR_RT.LEV
      FM.D.U2.EUR.4F.KR.MLFR_RT.LEV

    The only varying dimension is the rate code (position 7). We can use:
      FM.D.U2.EUR.4F.KR.MRR_RT+DFR_RT+MLFR_RT.LEV
    """
    # Extract the rate codes from the full series keys
    # "FM.D.U2.EUR.4F.KR.MRR_RT.LEV" → we want "MRR_RT"
    rate_codes = []
    for full_key in INTEREST_RATE_SERIES.values():
        parts = full_key.split(".")
        rate_codes.append(parts[6])  # 7th position (0-indexed)

    # Build combined key: FM.D.U2.EUR.4F.KR.MRR_RT+DFR_RT+MLFR_RT.LEV
    parts = list(INTEREST_RATE_SERIES.values())[0].split(".")
    parts[6] = "+".join(rate_codes)
    combined_key = ".".join(parts)

    fetch_series(combined_key, DAILY_START, f"data/raw/{TABLE_NAMES['interest_rates']}.csv")


def fetch_exchange_rates() -> None:
    """
    Fetch daily EUR exchange rates for all configured currencies.

    Same "+" trick: EXR.D.USD+GBP+JPY+CHF+PLN.EUR.SP00.A
    """
    currency_codes = list(EXCHANGE_RATE_SERIES.keys())

    # All keys share the same pattern, only the currency varies (position 3)
    parts = list(EXCHANGE_RATE_SERIES.values())[0].split(".")
    parts[2] = "+".join(currency_codes)
    combined_key = ".".join(parts)

    fetch_series(combined_key, DAILY_START, f"data/raw/{TABLE_NAMES['exchange_rates']}.csv")


def fetch_money_supply() -> None:
    """
    Fetch euro area M3 money supply growth (single series).
    """
    fetch_series(M3_SERIES, MONTHLY_START, f"data/raw/{TABLE_NAMES['money_supply']}.csv")


def fetch_bond_yields() -> None:
    """
    Fetch 2Y and 10Y euro area government bond yields.

    Combined: YC.B.U2.EUR.4F.G_N_A.SV_C_YM.SR_2Y+SR_10Y
    """
    tenor_codes = []
    for full_key in BOND_YIELD_SERIES.values():
        parts = full_key.split(".")
        tenor_codes.append(parts[7])  # last position

    parts = list(BOND_YIELD_SERIES.values())[0].split(".")
    parts[7] = "+".join(tenor_codes)
    combined_key = ".".join(parts)

    fetch_series(combined_key, MONTHLY_START, f"data/raw/{TABLE_NAMES['bond_yields']}.csv")

def load_all_to_duckdb() -> None:
    """
    Load all raw CSVs into DuckDB tables.

    Uses CREATE OR REPLACE TABLE + read_csv_auto — this is a full refresh
    every run. DuckDB's read_csv_auto automatically detects column names,
    types, and delimiters from the CSV file.

    Why full refresh (not incremental)?
    - Simpler: no need to track "what's new since last run"
    - Safe: if the ECB revises historical data, we pick up the revision
    - Fast enough: 25 years of monthly data is only ~thousands of rows
    """
    # Use absolute path so it works regardless of working directory
    db_path = os.path.join(os.path.dirname(__file__), "..", DUCKDB_PATH)
    conn = duckdb.connect(db_path)

    # Create the raw schema if it doesn't exist
    conn.execute(f"CREATE SCHEMA IF NOT EXISTS {RAW_SCHEMA}")

    print(f"\nLoading CSVs into DuckDB ({DUCKDB_PATH})...")

    for domain, table_name in TABLE_NAMES.items():
        csv_path = os.path.join(os.path.dirname(__file__), "..", "data", "raw", f"{table_name}.csv")

        # read_csv_auto: DuckDB scans the file, infers column types,
        # and loads everything in one shot. No Python parsing needed.
        conn.execute(f"""
            CREATE OR REPLACE TABLE {RAW_SCHEMA}.{table_name} AS
            SELECT * FROM read_csv_auto('{csv_path}', header=true)
        """)

        row_count = conn.execute(
            f"SELECT COUNT(*) FROM {RAW_SCHEMA}.{table_name}"
        ).fetchone()[0]
        print(f"  {RAW_SCHEMA}.{table_name}: {row_count} rows loaded")

    conn.close()
    print("Done loading into DuckDB.")

def main():
    """Run the full extract-and-load pipeline."""
    print("=" * 60)
    print("ECB Data Extraction")
    print("=" * 60)

    # Step 1: Fetch all data from the ECB API
    print("\n[1/2] Fetching data from ECB API...")
    print("-" * 40)
    fetch_inflation()
    fetch_interest_rates()
    fetch_exchange_rates()
    fetch_money_supply()
    fetch_bond_yields()

    # Step 2: Load all CSVs into DuckDB
    print("\n[2/2] Loading into DuckDB...")
    print("-" * 40)
    load_all_to_duckdb()

    print("\n" + "=" * 60)
    print("Extraction complete.")
    print("=" * 60)


if __name__ == "__main__":
    main()
