"""
Configuration for the weather data extraction.

This file defines:
- Which cities to pull weather data for
- What weather variables to request from the API
- Date ranges for historical data

WHY THESE CITIES?
We picked a mix of cities across different climates and continents.
This makes the dashboard more interesting and shows you can handle
multi-dimensional data. Feel free to add or remove cities.
"""

# ============================================================
# Cities to fetch weather data for
# ============================================================
# Each city needs: name, country code, latitude, longitude
# You can find coordinates at: https://www.latlong.net/
#
# Format: (city_name, country_code, latitude, longitude)
# ============================================================

CITIES = [
    ("Berlin", "DE", 52.52, 13.41),
    ("London", "GB", 51.51, -0.13),
    ("New York", "US", 40.71, -74.01),
    ("Tokyo", "JP", 35.68, 139.69),
    ("Cape Town", "ZA", -33.93, 18.42),
    ("Sydney", "AU", -33.87, 151.21),
    ("São Paulo", "BR", -23.55, -46.63),
    ("Kuala Lumpur", "MY", 3.14, 101.69),
    ("Auckland", "NZ", -36.85, 174.76),
]

# ============================================================
# Weather variables to request from Open-Meteo
# ============================================================
# Full list of available variables:
# https://open-meteo.com/en/docs
#
# We're requesting daily aggregates (not hourly) to keep data
# volume manageable and dashboard-friendly.
# ============================================================

DAILY_VARIABLES = [
    "temperature_2m_max",        # Highest temperature of the day (°C)
    "temperature_2m_min",        # Lowest temperature of the day (°C)
    "temperature_2m_mean",       # Average temperature of the day (°C)
    "precipitation_sum",         # Total rainfall/snowfall (mm)
    "rain_sum",                  # Total rainfall only (mm)
    "snowfall_sum",              # Total snowfall (cm)
    "windspeed_10m_max",         # Maximum wind speed at 10m height (km/h)
    "sunrise",                   # Sunrise time (ISO 8601)
    "sunset",                    # Sunset time (ISO 8601)
    "daylight_duration",         # Total daylight in seconds
    "relative_humidity_2m_mean", # Average relative humidity (%)
]

# ============================================================
# API settings
# ============================================================

# Open-Meteo provides historical data via a separate endpoint.
# The "forecast" endpoint gives you ~16 days ahead + recent past.
# The "archive" endpoint gives you years of historical data.

# We use the archive API for historical backfill
ARCHIVE_API_URL = "https://archive-api.open-meteo.com/v1/archive"

# And the forecast API for recent/current data
FORECAST_API_URL = "https://api.open-meteo.com/v1/forecast"

# How many days of historical data to fetch on first run
# 365 = one full year. Adjust based on how much data you want.
HISTORICAL_DAYS = 365

# ============================================================
# Database settings
# ============================================================

# Schema name for raw (unprocessed) data in DuckDB
RAW_SCHEMA = "raw_weather"

# Table name for the daily weather data
RAW_TABLE = "daily_weather"
