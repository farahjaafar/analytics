# Weather Analytics Pipeline — Claude Code Handover

## What this project is

A portfolio project demonstrating analytics engineering skills using a modern data stack. It pulls weather data from an API, loads it into a warehouse, transforms it with dbt, and will ultimately be visualized with Evidence.dev and deployed to Vercel. The goal is to showcase dbt + warehouse proficiency for Farah's transition into analytics engineering roles.

## Tech stack

- **Extraction:** Python script hitting the Open-Meteo API
- **Warehouse:** DuckDB (local, file-based)
- **Transformation:** dbt Core via dbt-fusion CLI (not dbt-core CLI)
- **Dashboard:** Evidence.dev (planned)
- **Deployment:** Vercel (planned)
- **CI:** GitHub Actions (planned)

## Current state — what's done

Everything below is built and passing:

- **Python extraction script:** Pulls daily weather data from the Open-Meteo API for 8 cities (including Kuala Lumpur). Covers 365 days of historical data. Includes humidity as a metric.
- **DuckDB load:** Extraction output is loaded into a local DuckDB database.
- **dbt models — all passing:**
  - `staging/` — raw source cleanup
  - `intermediate/` — business logic transformations
  - `marts/` — final analytical models
- **Seeds:** Loaded and referenced in models.
- **Tests:** Generic dbt tests configured and passing.

**Important:** This project uses `dbt-fusion` as the CLI, not the standard `dbt-core` CLI. Commands are the same syntax (`dbt build`, `dbt test`, etc.) but run through dbt-fusion. Check the project's README or installed packages if unsure.

## What's left — in order

Work through these sequentially. Each step should be committed separately with a clear commit message.

### 1. dbt macro

Write a reusable dbt macro. Pick something that genuinely reduces repetition in the existing models. Good candidates:
- A `convert_temperature` macro if models do Celsius/Fahrenheit conversion
- A `date_spine` or `generate_date_series` macro if date gap-filling is needed
- A metric rounding/formatting macro used across marts

Look at the existing models first. Find repeated SQL patterns and extract one into a macro under `macros/`. Then refactor the models to use it. Run `dbt build` to confirm nothing breaks.

### 2. Custom dbt test

Write a custom schema test (not just a generic `unique`/`not_null`). It should test a real data quality concern, for example:
- `test_temperature_range` — assert temperatures fall within physically plausible bounds (e.g., -60°C to 60°C)
- `test_humidity_range` — assert humidity is between 0 and 100
- `test_no_future_dates` — assert no dates are in the future

Place it in `tests/` (singular test) or `macros/` (reusable schema test). Add it to the relevant model's `.yml` file. Run `dbt test` to confirm it passes.

### 3. Orchestration script

Write a Python or shell script that runs the full pipeline end-to-end:
1. Run the extraction script (pull fresh data from Open-Meteo)
2. Load into DuckDB
3. Run `dbt build` (which runs models + tests)

Keep it simple. A single `run_pipeline.sh` or `orchestrate.py` at the project root. Include basic logging (timestamps, step names, pass/fail). Exit with a non-zero code if any step fails.

### 4. GitHub Actions CI

Create `.github/workflows/ci.yml` that:
- Triggers on push to `main` and on pull requests
- Sets up Python and installs dependencies
- Installs dbt-fusion (check how it's installed — likely pip or a binary)
- Runs the orchestration script or at minimum `dbt build`
- Fails the workflow if tests fail

Keep the workflow minimal. No caching or matrix builds needed — this is a portfolio project.

### 5. Evidence.dev dashboard

Set up Evidence.dev to connect to the DuckDB file and build a dashboard. The dashboard should show:
- Temperature trends over time across cities
- Humidity comparisons
- Any interesting aggregations from the marts models

Evidence uses markdown files with SQL blocks. Set it up in a subfolder (e.g., `dashboard/` or `reports/`). Make sure it reads from the same DuckDB file that dbt writes to.

### 6. Vercel deployment

Deploy the Evidence.dev dashboard to Vercel. This is the final step — a live URL Farah can link to on her resume/portfolio.

## Project location

The project lives at `~/Documents/Projects/weather-analytics-pipeline` on Farah's local machine.

## Working style

- Explain the steps.
- Show the code, run it, confirm it works. 
- Commit after each completed step with a descriptive message.
- If something breaks, fix it before moving on.
- Ask before making structural changes to existing models.
- Always suggest best practices