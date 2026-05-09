import duckdb
import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
db_path = PROJECT_ROOT / os.getenv("DUCKDB_PATH", "data/ecb_analytics.duckdb")
output_dir = PROJECT_ROOT / "evidence_dashboard" / "sources" / "ecb"
output_dir.mkdir(parents=True, exist_ok=True)

con = duckdb.connect(str(db_path), read_only = True)

tables = [
    "mart_macro_overview",
    "mart_inflation_comparison",
    "mart_monetary_policy_timeline",
    "mart_currency_strength"
]

for table in tables:
    out = output_dir / f"{table}.csv"
    con.execute(f"COPY (SELECT * FROM marts.{table}) TO '{out}' (FORMAT CSV, HEADER)")
    row_count = con.execute(f"SELECT count(*) FROM marts.{table}").fetchone()[0]
    print(f"Exported {table}: {row_count} rows")

con.close()
print("Done.")
