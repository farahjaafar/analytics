"""
fetch_weather.py — Extracts weather data from the Open-Meteo API.

WHAT THIS SCRIPT DOES:
1. Loops through each city defined in config.py
2. Calls the Open-Meteo API to get daily weather data
3. Saves the raw JSON responses as a list of dictionaries
4. Returns the data so load_to_duckdb.py can store it

USAGE:
    # Test mode: fetch one city, print the result
    python extract/fetch_weather.py --test

    # Full run: fetch all cities (called by load_to_duckdb.py)
    python extract/fetch_weather.py
"""

import requests
import sys
from datetime import datetime, timedelta
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from config import (
    CITIES,
    DAILY_VARIABLES,
    ARCHIVE_API_URL,
    HISTORICAL_DAYS,
)


def _build_session() -> requests.Session:
    """
    Create a requests Session with automatic retries on transient errors.
    Retries up to 3 times with exponential backoff (2s, 4s, 8s) on
    connection errors, timeouts, and 5xx responses.
    """
    session = requests.Session()
    retry = Retry(
        total=3,
        backoff_factor=2,
        status_forcelist=[500, 502, 503, 504],
        allowed_methods=["GET"],
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    return session


def fetch_weather_for_city(
    city_name: str,
    country_code: str,
    latitude: float,
    longitude: float,
    start_date: str,
    end_date: str,
) -> list[dict]:
    """
    Fetch daily weather data for a single city.

    The API returns data in COLUMNAR format:
        {"daily": {"time": ["2024-01-01", ...], "temperature_2m_max": [5.2, ...]}}

    We convert it to ROW format (one dict per day) because
    that's how databases store data — one row per observation.
 
    Args:
        city_name:    Human-readable city name (e.g., "Berlin")
        country_code: ISO country code (e.g., "DE")
        latitude:     City latitude coordinate
        longitude:    City longitude coordinate
        start_date:   Start date in YYYY-MM-DD format
        end_date:     End date in YYYY-MM-DD format

    Returns:
        A list of dictionaries, one per day, like:
        [
            {
                "city": "Berlin",
                "country_code": "DE",
                "latitude": 52.52,
                "longitude": 13.41,
                "date": "2024-01-01",
                "temperature_2m_max": 5.2,
                "temperature_2m_min": -1.3,
                ...
            },
            ...
        ]
   """

    # --------------------------------------------------------
    # Build the API request
    # --------------------------------------------------------
    # The "daily" parameter takes a comma-separated list of variables.
    # Full docs: https://open-meteo.com/en/docs
    # --------------------------------------------------------

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "daily": ",".join(DAILY_VARIABLES),
        "start_date": start_date,
        "end_date": end_date,
        "timezone": "auto",
    }

    # --------------------------------------------------------
    # Make the API call
    # --------------------------------------------------------
    # requests.get() sends an HTTP GET request.
    # The API returns JSON with this structure:
    # {
    #   "daily": {
    #     "time": ["2024-01-01", "2024-01-02", ...],
    #     "temperature_2m_max": [5.2, 3.1, ...],
    #     ...
    #   }
    # }
    # --------------------------------------------------------

    print(f"  Fetching data for {city_name} ({start_date} to {end_date})...")

    # Make the HTTP GET request to Open-Meteo (with retry session)
    session = _build_session()
    response = session.get(ARCHIVE_API_URL, params=params, timeout=60)

    # If the API returns an error, raise an exception immediately
    # instead of silently continuing with bad data
    response.raise_for_status()

    data = response.json()

    # Convert columnar response to rows
    daily_data = data.get("daily", {})
    dates = daily_data.get("time", [])

    rows = []
    for i, date in enumerate(dates):
        row = {
            "city": city_name,
            "country_code": country_code,
            "latitude": latitude,
            "longitude": longitude,
            "date": date,
            "extracted_at": datetime.utcnow().isoformat(),
        }

        # Add each weather variable for this day
        for variable in DAILY_VARIABLES:
            row[variable] = daily_data.get(variable, [None])[i]

        rows.append(row)

    print(f"    Got {len(rows)} days of data")
    return rows

def fetch_all_cities() -> list[dict]:
    """
    Fetch weather data for ALL cities defined in config.py.

    Returns:
        A single flat list of all rows across all cities.
        If you have 7 cities x 365 days, you get 2,555 rows.
    """

    # --------------------------------------------------------
    # Calculate the date range
    # --------------------------------------------------------
    # We fetch from (today - HISTORICAL_DAYS) to yesterday.
    # We use yesterday as the end date because today's data
    # might not be complete yet.
    # --------------------------------------------------------

    end_date = (datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d")
    start_date = (
        datetime.today() - timedelta(days=HISTORICAL_DAYS)
    ).strftime("%Y-%m-%d")

    print(f"Fetching weather data from {start_date} to {end_date}")
    print(f"Cities: {len(CITIES)}")
    print("-" * 50)

    all_rows = []
    for city_name, country_code, lat, lon in CITIES:
        rows = fetch_weather_for_city(
            city_name=city_name,
            country_code=country_code,
            latitude=lat,
            longitude=lon,
            start_date=start_date,
            end_date=end_date,
        )
        all_rows.extend(rows)

    print("-" * 50)
    print(f"Total rows fetched: {len(all_rows)}")
    return all_rows


# ============================================================
# Run this file directly for testing
# ============================================================

if __name__ == "__main__":
    if "--test" in sys.argv:
        # Test mode: only fetch Berlin, last 7 days
        print("=== TEST MODE ===\n")
        end = (datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d")
        start = (datetime.today() - timedelta(days=7)).strftime("%Y-%m-%d")

        rows = fetch_weather_for_city(
            "Berlin", "DE", 52.52, 13.41, start, end
        )

        print("\nSample output (first 2 rows):")
        for row in rows[:2]:
            for key, value in row.items():
                print(f"  {key}: {value}")
            print()
    else:
        fetch_all_cities()
