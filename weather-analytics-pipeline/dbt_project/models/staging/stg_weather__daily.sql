/*
    stg_weather__daily.sql — Staging model for daily weather data

    RULES FOR STAGING MODELS:
    1. One staging model per raw source table
    2. Only light transformations:
       - Rename columns to be consistent
       - Cast data types
       - Filter junk rows
       - Add a surrogate key
    3. NO business logic (that goes in intermediate/)
    4. NO joins (that goes in intermediate/)
*/

{{ config(
    materialized="view",
    tags=["staging"],
    )
}}

with raw_weather as ( /*defined in _staging_models.yml*/
    select * from {{ source('raw_weather', 'daily_weather') }}
)

, cleaned as (
    select
        {{ dbt_utils.generate_surrogate_key(['city', 'date']) }} as weather_id,
        city,
        country_code,
        latitude,
        longitude,
        cast(date as date)                  as date,

        -- Temperature
        {{ round_metric('temperature_2m_max') }}        as temp_max_celsius,
        {{ round_metric('temperature_2m_min') }}        as temp_min_celsius,
        {{ round_metric('temperature_2m_mean') }}       as temp_mean_celsius,

        -- Precipitation
        {{ round_metric('precipitation_sum') }}         as precipitation_mm,
        {{ round_metric('rain_sum') }}                  as rain_mm,
        {{ round_metric('snowfall_sum') }}              as snowfall_mm,

        -- Wind
        {{ round_metric('windspeed_10m_max') }}         as wind_max_kmh,

        -- Humidity
        {{ round_metric('relative_humidity_2m_mean') }} as humidity_pct,

        -- Daylight (convert seconds to hours)
        sunrise,
        sunset,
        {{ round_metric('daylight_duration / 3600.0', 2) }} as daylight_hours,

        -- Metadata
        extracted_at

    from raw_weather
    where date is not null
)

select * from cleaned