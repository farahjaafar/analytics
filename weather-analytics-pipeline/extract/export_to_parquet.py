import duckdb
import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
db_path = PROJECT_ROOT / os.getenv("DUCKDB_PATH", "data/weather.duckdb")
output_dir = PROJECT_ROOT / "evidence_dashboard" / "sources" / "weather"
output_dir.mkdir(parents=True, exist_ok=True)

con = duckdb.connect(str(db_path), read_only=True)

tables = ["fct_daily_weather", "dim_cities"]
for table in tables:
    df = con.execute(f"SELECT * FROM main_marts.{table}").fetchdf()
    out = output_dir / f"{table}.csv"
    df.to_csv(out, index=False)
    print(f"Exported {table}: {len(df)} rows")

con.close()
print("Done.")