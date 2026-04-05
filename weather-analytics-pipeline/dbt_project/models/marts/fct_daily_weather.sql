/*
    Fact table for the dashboard
    Materialized as a table for fast queries
*/

{{ config(
    materialized="table", 
    tags=["marts"]
    ) 
}}

with daily_metrics as (
    select * from {{ ref('int_weather__daily_metrics') }}
)

, city_info as (
    select * from {{ ref('city_metadata') }}
)

, final as (
    select 
        dm.weather_id,
        dm.city,
        dm.country_code,
        dm.date,
        ci.continent,
        ci.climate_zone,
        dm.year,
        dm.month_number,
        dm.month_name,
        dm.day_of_week,
        dm.season,
        dm.temp_max_celsius,
        dm.temp_min_celsius,
        dm.temp_mean_celsius,
        dm.temp_range_celsius,
        dm.precipitation_mm,
        dm.rain_mm,
        dm.snowfall_mm,
        dm.precipitation_category,
        dm.is_rainy_day,
        dm.wind_max_kmh,
        dm.humidity_pct,
        dm.daylight_hours
    from daily_metrics dm
    left join city_info ci 
        on dm.city = ci.city
        and dm.country_code = ci.country_code
)

select * from final