# Weather Analytics Pipeline

![CI](https://github.com/farahjaafar/analytics/actions/workflows/ci.yml/badge.svg)

An end-to-end ELT pipeline that ingests historical and recent weather data for 8 global cities, transforms it with dbt, and surfaces insights through an interactive Evidence.dev dashboard — all running on a fully local, file-based stack.

> Part of the [Analytics monorepo](../README.md).

---

## Project Overview

| Attribute | Detail |
|-----------|--------|
| **Data source** | [Open-Meteo API](https://open-meteo.com/) — free, no API key required |
| **Cities** | 8 cities across 6 continents |
| **Date range** | Rolling 365 days |
| **Row count** | ~2,920 rows (8 cities × 365 days) |
| **Warehouse** | DuckDB (local file) |
| **Transformation** | dbt Core (3-layer architecture) |
| **Dashboard** | Evidence.dev (markdown + SQL) |
| **CI/CD** | GitHub Actions |

This project is a portfolio piece demonstrating analytics engineering best practices: modular ELT code, layered dbt modelling, data quality testing, and a self-contained BI layer — all wired into automated CI.

---

## Architecture

```
┌─────────────────────────────────────────────────────┐
│  EXTRACT                                            │
│  Open-Meteo API (historical + forecast endpoints)   │
│       ↓  fetch_weather.py  (requests)               │
│  8 cities × 365 days  →  list of row dicts          │
└─────────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────────┐
│  LOAD                                               │
│  load_to_duckdb.py  (duckdb)                        │
│       ↓  full-refresh                               │
│  raw_weather.daily_weather  (DuckDB file)           │
└─────────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────────┐
│  TRANSFORM  (dbt build)                             │
│                                                     │
│  staging/   stg_weather__daily          (view)      │
│       ↓  clean, rename, surrogate key               │
│  intermediate/  int_weather__daily_metrics (view)   │
│       ↓  temp range, precip categories, seasons     │
│  marts/  fct_daily_weather              (table)     │
│          dim_cities                     (table)     │
└─────────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────────┐
│  VISUALISE                                          │
│  CSV export  →  Evidence.dev dashboard              │
│  pages/index.md  (KPIs · trends · city stats)      │
└─────────────────────────────────────────────────────┘
```

---

## Tech Stack

| Layer | Tool | Version |
|-------|------|---------|
| Extraction | Python | 3.11 |
| HTTP client | requests | 2.31.0 |
| Environment | python-dotenv | 1.0.1 |
| Warehouse | DuckDB | 1.1.0 |
| Transformation | dbt Core | 1.8.0 |
| dbt adapter | dbt-duckdb | 1.8.0 |
| dbt utilities | dbt_utils | 1.3.3 |
| Visualisation | Evidence.dev | 40.1.8 |
| CI/CD | GitHub Actions | — |

---

## Repository Structure

```
weather-analytics-pipeline/
│
├── extract/                          # E + L layer (Python)
│   ├── config.py                     # Cities list, API config, weather variables
│   ├── fetch_weather.py              # Open-Meteo API client
│   ├── load_to_duckdb.py             # Orchestrates fetch → DuckDB load
│   └── export_to_parquet.py          # Optional CSV/Parquet export
│
├── dbt_project/                      # T layer (dbt)
│   ├── dbt_project.yml               # Project config & materialisation strategy
│   ├── profiles.yml                  # DuckDB connection profile
│   ├── packages.yml                  # dbt_utils dependency
│   ├── seeds/
│   │   └── city_metadata.csv         # Dimension data: continent, climate zone
│   ├── models/
│   │   ├── staging/
│   │   │   ├── stg_weather__daily.sql
│   │   │   └── _stg__models.yml      # Column docs + tests
│   │   ├── intermediate/
│   │   │   ├── int_weather__daily_metrics.sql
│   │   │   └── _int__models.yml
│   │   └── marts/
│   │       ├── fct_daily_weather.sql
│   │       ├── dim_cities.sql
│   │       └── _marts__models.yml
│   └── macros/
│       ├── round_metric.sql          # Reusable rounding macro
│       └── test_temperature_range.sql # Custom schema test
│
├── evidence_dashboard/               # V layer (Evidence.dev)
│   ├── evidence.config.yaml          # Plugin config (CSV datasource)
│   ├── package.json
│   ├── pages/
│   │   └── index.md                  # Dashboard page (markdown + SQL)
│   └── sources/
│       └── weather/
│           ├── connection.yaml       # CSV source definition
│           ├── fct_daily_weather.csv # Exported fact data
│           └── dim_cities.csv        # Exported dimension data
│
├── data/
│   └── weather.duckdb                # DuckDB warehouse file (~1.5 MB)
│
├── run_pipeline.sh                   # Full pipeline runner (EL + dbt build)
├── requirements.txt                  # Python dependencies
├── .env.example                      # Environment variable template
└── handover.md                       # Project notes & next steps
```

---

## Cities Covered

| City | Country | Continent | Climate Zone |
|------|---------|-----------|--------------|
| Berlin | Germany | Europe | Temperate |
| London | United Kingdom | Europe | Temperate Oceanic |
| New York | United States | North America | Humid Continental |
| Tokyo | Japan | Asia | Humid Subtropical |
| Cape Town | South Africa | Africa | Mediterranean |
| Sydney | Australia | Oceania | Humid Subtropical |
| São Paulo | Brazil | South America | Tropical |
| Kuala Lumpur | Malaysia | Asia | Tropical Rainforest |

---

## Data Pipeline — Layer by Layer

### Extract & Load (Python)

**`extract/config.py`**
- Defines the 8 target cities with coordinates and country codes
- Lists 11 daily weather variables fetched from the API: `temperature_2m_max`, `temperature_2m_min`, `temperature_2m_mean`, `precipitation_sum`, `relative_humidity_2m_mean`, `wind_speed_10m_max`, `daylight_duration`, `sunrise`, `sunset`, `wind_gusts_10m_max`, `precipitation_hours`
- Configures API base URLs (Archive for historical data, Forecast for recent data)

**`extract/fetch_weather.py`**
- Calls the Open-Meteo API for each city
- Merges Archive (historical) and Forecast (recent) responses to cover the full 365-day window
- Converts columnar API response format into a flat list of row dictionaries
- Can be run standalone in test mode: `python extract/fetch_weather.py --test` (fetches 7 days for Berlin only)

**`extract/load_to_duckdb.py`**
- Connects to the DuckDB file at `data/weather.duckdb`
- Drops and recreates the `raw_weather.daily_weather` table on every run (full-refresh pattern)
- Inserts all fetched rows
- Runs post-load verification: row counts per city, date ranges, null checks

**`extract/export_to_parquet.py`**
- Optional script to export dbt mart tables to CSV files consumed by the Evidence dashboard
- Writes `fct_daily_weather.csv` and `dim_cities.csv` to `evidence_dashboard/sources/weather/`

---

### Transform (dbt — 3-layer architecture)

Materialisation strategy defined in `dbt_project.yml`:
- `staging/` → **views** (lightweight wrappers over raw data)
- `intermediate/` → **views** (business logic, not queried by the dashboard)
- `marts/` → **tables** (pre-computed, dashboard-ready)

#### Staging: `stg_weather__daily` (view)

Input: `raw_weather.daily_weather`

Transformations applied:
- Surrogate key: `generate_surrogate_key(['city', 'date'])` from `dbt_utils`
- Column renames to readable names (e.g. `temperature_2m_max` → `temp_max_celsius`)
- Metric rounding via the `round_metric()` macro (1 decimal place by default)
- Null filter: removes rows where `date` is null

Tests: `unique` + `not_null` on `weather_id`; custom `test_temperature_range` (−60°C to +60°C) on all temperature columns.

#### Intermediate: `int_weather__daily_metrics` (view)

Input: `stg_weather__daily`

Business logic added:
- **Temperature range**: `temp_max - temp_min` (daily swing in °C)
- **Precipitation category**: `dry` (0 mm) / `light` (< 2.5 mm) / `moderate` (< 7.6 mm) / `heavy` (< 50 mm) / `extreme` (≥ 50 mm)
- **Rainy day flag**: boolean, `precipitation_mm > 0`
- **Season**: hemisphere-aware — Northern and Southern hemisphere cities get opposite seasons based on latitude and month
- **Time dimensions**: `day_of_week`, `month_name`, `month_number`, `year`

Tests: `unique` + `not_null` on `weather_id`; `accepted_values` on `precipitation_category` and `season`.

#### Marts

**`fct_daily_weather`** (table)
- One row per city per day (~2,920 rows)
- All columns from `int_weather__daily_metrics` enriched with `continent` and `climate_zone` from the `city_metadata` seed (left join)
- Primary key: `weather_id`

**`dim_cities`** (table)
- One row per city (8 rows)
- Aggregates from `int_weather__daily_metrics` joined with `city_metadata`:
  - Date range: `data_from`, `data_to`
  - Temperature: `avg_temp_celsius`, `coldest_temp_celsius`, `hottest_temp_celsius`
  - Precipitation: `total_precip_mm`, `avg_daily_precip_mm`, `rainy_days`, `pct_rainy_days`
  - Humidity & wind: `avg_humidity_pct`, `avg_wind_max_kmh`
  - Daylight: `avg_daylight_hours`

#### Macros

**`round_metric(value, decimals=1)`**
```sql
round({{ value }}, {{ decimals }})
```
Used throughout models to standardise rounding; default is 1 decimal place.

**`test_temperature_range`**
Custom schema test that validates a column falls within a physically plausible range. Configured with `min_value=-60` and `max_value=60` on all temperature columns in the staging layer.

---

### Visualise (Evidence.dev)

Evidence.dev renders a standard markdown file (`pages/index.md`) as an interactive dashboard. SQL queries are embedded inline and execute against the CSV data sources.

#### Dashboard Sections

**1. KPIs (8 BigValue cards)**
```sql
select
    count(distinct city)           as cities,
    count(*)                       as total_days,
    round(avg(temp_mean_celsius))  as avg_temp,
    round(avg(humidity_pct))       as avg_humidity,
    count(distinct climate_zone)   as climate_zones,
    round(avg(daylight_hours))     as avg_daylight,
    round(max(temp_max_celsius))   as hottest_temp,
    round(min(temp_min_celsius))   as coldest_temp
from weather.fct_daily_weather
```
Displays: cities tracked, days of data, global average temperature, average humidity, number of climate zones, average daylight hours, record high and record low temperatures.

**2. Temperature Trends (LineChart)**
Multi-series line chart showing `temp_mean_celsius` over time for all 8 cities. X-axis: date; Y-axis: °C.

**3. City Overview (DataTable + 3 BarCharts)**
- DataTable: all city statistics from `dim_cities`, sorted by `avg_temp_celsius` descending
- Bar chart 1: Average temperature by city
- Bar chart 2: Average humidity by city
- Bar chart 3: % rainy days by city

**4. Seasonal Patterns (2 BarCharts + Dropdown filter)**
- Multi-select dropdown to filter by city (defaults to all 8)
- Bar chart 1: Average temperature by season for selected cities
- Bar chart 2: Average precipitation by season for selected cities
- Note: tropical and arid cities (Kuala Lumpur, São Paulo) show less seasonal variation — this is expected given the hemisphere-aware season logic

---

## Getting Started

### Prerequisites

- Python 3.9+
- Node.js 18+
- Git

### Setup

```bash
# 1. Clone the repo and enter the project
git clone https://github.com/farahjaafar/analytics.git
cd analytics/weather-analytics-pipeline

# 2. Create and activate a Python virtual environment
python3 -m venv venv
source venv/bin/activate        # macOS/Linux
# venv\Scripts\activate         # Windows

# 3. Install Python dependencies
pip install -r requirements.txt

# 4. Install dbt packages
cd dbt_project
dbt deps
cd ..

# 5. Configure environment variables
cp .env.example .env
# Edit .env if you want to change the DuckDB path or use MotherDuck
```

### Run the Pipeline

```bash
# Full pipeline (extract → load → dbt build)
bash run_pipeline.sh
```

Or run each step individually:

```bash
# Extract & load only
python extract/load_to_duckdb.py

# dbt transform only
cd dbt_project && dbt build

# Export CSVs for the dashboard
python extract/export_to_parquet.py
```

### Run the Dashboard

```bash
cd evidence_dashboard
npm install
npm run dev
# Open http://localhost:3000
```

### Test Extraction (quick sanity check)

```bash
# Fetches 7 days of data for Berlin only — no database writes
python extract/fetch_weather.py --test
```

---

## Environment Variables

Defined in `.env` (copy from `.env.example`):

| Variable | Default | Description |
|----------|---------|-------------|
| `DUCKDB_PATH` | `data/weather.duckdb` | Path to the DuckDB warehouse file |
| `OPEN_METEO_BASE_URL` | `https://api.open-meteo.com/v1/forecast` | Open-Meteo API base URL |
| `MOTHERDUCK_TOKEN` | _(empty)_ | Optional MotherDuck cloud token |

---

## CI/CD

File: [`.github/workflows/ci.yml`](../.github/workflows/ci.yml)

**Triggers:**
- Push to `main`
- Pull requests targeting `main`
- Daily schedule at **06:00 UTC**
- Manual trigger via `workflow_dispatch`

**Steps:**
1. Checkout repository
2. Set up Python 3.11
3. `pip install -r requirements.txt`
4. `dbt deps` (install dbt packages)
5. `python extract/load_to_duckdb.py` (fetch from API, load to DuckDB)
6. `dbt build` (run all models + all tests)

---

## dbt Testing Strategy

Tests are defined in `_stg__models.yml`, `_int__models.yml`, and `_marts__models.yml`.

| Test type | Where applied | What it checks |
|-----------|---------------|----------------|
| `unique` | All surrogate keys (`weather_id`) and `city` in `dim_cities` | No duplicate rows |
| `not_null` | All surrogate keys, temperatures, dates | No missing values on critical columns |
| `accepted_values` | `precipitation_category`, `season` | Only valid category strings present |
| `test_temperature_range` | All temperature columns in staging | Values fall within −60°C to +60°C |

Run tests independently:

```bash
cd dbt_project

# Run all tests
dbt test

# Run tests for a specific model
dbt test --select stg_weather__daily

# Run a specific test type
dbt test --select test_type:not_null
```
