{{ config(
    materialized="table"
    ) 
}}

with daily_metrics as (
    select * from {{ ref('int_weather__daily_metrics') }}
)

, city_info as (
    select * from {{ ref('city_metadata') }}
)

, city_stats as (
    select 
        city,
        country_code,
        latitude,
        longitude,
        min(date) as data_from,
        max(date) as data_to,
        count(*) as total_days,

        -- Temperature
        {{ round_metric('avg(temp_mean_celsius)') }} as avg_temp_celsius,
        {{ round_metric('min(temp_min_celsius)') }} as coldest_temp_celsius,
        {{ round_metric('max(temp_max_celsius)') }} as hottest_temp_celsius,

        -- Precipitation
        {{ round_metric('sum(precipitation_mm)') }} as total_precipitation_mm,
        {{ round_metric('avg(precipitation_mm)') }} as avg_daily_precipitation_mm,
        count(*) filter (where is_rainy_day) as total_rainy_days,

        -- Humidity
        {{ round_metric('avg(humidity_pct)') }} as avg_humidity_pct,

        -- Wind
        {{ round_metric('avg(wind_max_kmh)') }} as avg_wind_max_kmh,

        -- Daylight
        {{ round_metric('avg(daylight_hours)') }} as avg_daylight_hours

    from daily_metrics
    group by city, country_code, latitude, longitude
)

, final as (
    select 
        cs.*,
        ci.continent,
        ci.climate_zone,
        {{ round_metric('cs.total_rainy_days * 100.0 / nullif(cs.total_days, 0)') }} as pct_rainy_days

    from city_stats cs
    left join city_info ci 
        on cs.city = ci.city
        and cs.country_code = ci.country_code
)

select * from final