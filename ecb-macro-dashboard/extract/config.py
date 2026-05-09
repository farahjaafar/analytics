"""
config.py — Central configuration for ECB data extraction.

All series keys, country codes, date ranges, and database settings
live here. Change something once, and every downstream script picks it up.
"""

# ---------------------------------------------------------------
# ECB Data Portal API
# ---------------------------------------------------------------
# The ECB exposes macroeconomic data via a REST API using the SDMX standard.
# No API key needed — it's free and public.
# Adding "?format=csvdata" to the URL returns CSV instead of XML.
# ---------------------------------------------------------------
ECB_API_BASE = "https://data-api.ecb.europa.eu/service/data"

# ---------------------------------------------------------------
# Countries
# ---------------------------------------------------------------
# These are the countries we fetch inflation (HICP) data for.
# "U2" is the ECB's code for the Euro Area aggregate — it's not a real
# country code, but a special SDMX dimension value meaning "all of the
# euro zone combined."
# ---------------------------------------------------------------
COUNTRIES = ["DE", "FR", "ES", "IT", "NL", "U2"]

# ---------------------------------------------------------------
# Inflation (HICP) components
# ---------------------------------------------------------------
# HICP = Harmonised Index of Consumer Prices — the ECB's official
# inflation measure. Each "component" breaks down what's driving
# inflation: is it energy? food? services?
#
# The keys are human-readable names we'll use in dbt.
# The values are SDMX "ICP_ITEM" codes — cryptic but stable identifiers.
# ---------------------------------------------------------------
INFLATION_COMPONENTS = {
    "headline":          "000000",   # All items combined (the number in the news)
    "core":              "XEF000",   # Excluding energy and food (less volatile)
    "energy":            "NRGY00",   # Energy prices (oil, gas, electricity)
    "food":              "FOOD00",   # Food including alcohol and tobacco
    "services":          "SERV00",   # Services (rent, transport, healthcare)
    "non_energy_goods":  "IGXE00",   # Industrial goods excluding energy
}

# ---------------------------------------------------------------
# SDMX series key pattern for HICP
# ---------------------------------------------------------------
# An SDMX series key is a dot-separated string where each position
# is a "dimension." For HICP inflation, the pattern is:
#
#   ICP.M.{country}.N.{item}.4.ANR
#    │   │     │     │   │    │  │
#    │   │     │     │   │    │  └─ ANR = Annual Rate of change (year-over-year %)
#    │   │     │     │   │    └──── 4 = index type
#    │   │     │     │   └───────── item code (from INFLATION_COMPONENTS)
#    │   │     │     └───────────── N = Neither seasonally nor working-day adjusted
#    │   │     └─────────────────── country code (from COUNTRIES)
#    │   └───────────────────────── M = Monthly frequency
#    └───────────────────────────── ICP = the HICP dataflow
#
# Note: The HICP dataset transitioned in Feb 2026. The dataflow name
# may be "ICP" or "HICP" — try both if one fails.
# ---------------------------------------------------------------
INFLATION_SERIES_PATTERN = "ICP.M.{country}.N.{item}.4.ANR"

# ---------------------------------------------------------------
# ECB key interest rates
# ---------------------------------------------------------------
# These are the three policy rates the ECB sets at each monetary
# policy meeting. The series keys come from the FM (Financial Markets)
# dataflow.
#
# Series key pattern: FM.D.U2.EUR.4F.KR.{rate_code}.LEV
#   FM = Financial Markets dataflow
#   D = Daily frequency (but rates only change on decision days)
#   U2 = Euro Area
#   EUR = Euro
#   4F = ECB key rates category
#   KR = Key Rate
#   LEV = Level (not change)
# ---------------------------------------------------------------
INTEREST_RATE_SERIES = {
    "main_refinancing":    "FM.D.U2.EUR.4F.KR.MRR_RT.LEV",
    "deposit_facility":    "FM.D.U2.EUR.4F.KR.DFR.LEV",
    "marginal_lending":    "FM.D.U2.EUR.4F.KR.MLFR.LEV",
}

# ---------------------------------------------------------------
# EUR exchange rates
# ---------------------------------------------------------------
# Daily EUR exchange rates from the EXR (Exchange Rate) dataflow.
#
# Series key pattern: EXR.D.{currency}.EUR.SP00.A
#   EXR = Exchange Rate dataflow
#   D = Daily
#   {currency} = target currency (e.g., USD)
#   EUR = base currency
#   SP00 = spot rate
#   A = average
# ---------------------------------------------------------------
EXCHANGE_RATE_SERIES = {
    "USD": "EXR.D.USD.EUR.SP00.A",
    "GBP": "EXR.D.GBP.EUR.SP00.A",
    "JPY": "EXR.D.JPY.EUR.SP00.A",
    "CHF": "EXR.D.CHF.EUR.SP00.A",
    "PLN": "EXR.D.PLN.EUR.SP00.A",
}

# ---------------------------------------------------------------
# Money supply (M3)
# ---------------------------------------------------------------
# M3 is the broadest measure of money supply in the euro area.
# It includes cash, bank deposits, money market funds, and short-term
# debt securities. The ECB watches M3 growth as a signal of future
# inflation — more money chasing the same goods = rising prices.
#
# BSI = Balance Sheet Items dataflow
# M.U2.Y = Monthly, Euro Area, Year-over-year
# V.M30.A.1.U2.2300.Z01.E = specific M3 aggregate definition
# ---------------------------------------------------------------
M3_SERIES = "BSI.M.U2.Y.V.M30.X.I.U2.2300.Z01.A"

# ---------------------------------------------------------------
# Government bond yields
# ---------------------------------------------------------------
# Euro area benchmark bond yields for 2-year and 10-year maturities.
# The spread between them (10Y - 2Y) is the "yield curve."
#
# When this spread goes negative (10Y < 2Y), the yield curve is
# "inverted" — historically one of the strongest recession predictors.
#
# YC = Yield Curve dataflow
# B.U2.EUR.4F.G_N_A.SV_C_YM = Euro area government bond composite
# ---------------------------------------------------------------
BOND_YIELD_SERIES = {
    "2Y":  "YC.B.U2.EUR.4F.G_N_A.SV_C_YM.SR_2Y",
    "10Y": "YC.B.U2.EUR.4F.G_N_A.SV_C_YM.SR_10Y",
}

# ---------------------------------------------------------------
# Date ranges
# ---------------------------------------------------------------
# How far back to fetch data. Monthly series use YYYY-MM format;
# daily series use YYYY-MM-DD format. The ECB API handles this
# distinction automatically based on the dataflow's native frequency.
# ---------------------------------------------------------------
MONTHLY_START = "2000-01"
DAILY_START = "2000-01-01"

# ---------------------------------------------------------------
# DuckDB database settings
# ---------------------------------------------------------------
# All raw data lands in the "raw_ecb" schema. Each dataflow gets
# its own table within that schema.
# ---------------------------------------------------------------
DUCKDB_PATH = "data/ecb_analytics.duckdb"
RAW_SCHEMA = "raw_ecb"

TABLE_NAMES = {
    "inflation":      "inflation",
    "interest_rates": "interest_rates",
    "exchange_rates": "exchange_rates",
    "money_supply":   "money_supply",
    "bond_yields":    "bond_yields",
}
