/*
    int_weather__daily_metrics.sql — Derived metrics from daily weather

    This is where business logic lives:
    - Temperature range (max - min)
    - Precipitation categories
    - Season (adjusted for hemisphere)
    - Time dimensions (day of week, month)
*/

{{config(
    materialized="view",
    tags=["intermediate"]
    )
}}

with daily_weather as (
    select * from {{ref('stg_weather__daily')}}
)

, with_metrics as (
    select
        weather_id,
        city,
        country_code,
        latitude,
        longitude,
        date,
        temp_max_celsius,
        temp_min_celsius,
        temp_mean_celsius,
        precipitation_mm,
        rain_mm,
        snowfall_mm,
        wind_max_kmh,
        humidity_pct,
        daylight_hours,

        -- Temperature range: how much did temp swing in one day?
        {{ round_metric('temp_max_celsius - temp_min_celsius') }} as temp_range_celsius,

        -- Precipitation category
        case
            when precipitation_mm = 0 then 'dry'
            when precipitation_mm > 0 and precipitation_mm <= 2.5 then 'light'
            when precipitation_mm > 2.5 and precipitation_mm <= 7.6 then 'moderate'
            when precipitation_mm > 7.6 then 'heavy'
            else 'extreme'
        end as precipitation_category,

        -- Is it a rainy day?
        case
            when precipitation_mm > 0 then true
            else false
        end as is_rainy_day,
        
        -- Season (adjusted for hemisphere)
        case
            when extract(month from date) in (12, 1, 2) then
                case when latitude >= 0 then 'Winter' else 'Summer' end
            when extract(month from date) in (3, 4, 5) then
                case when latitude >= 0 then 'Spring' else 'Autumn' end
            when extract(month from date) in (6, 7, 8) then
                case when latitude >= 0 then 'Summer' else 'Winter' end
            when extract(month from date) in (9, 10, 11) then
                case when latitude >= 0 then 'Autumn' else 'Spring' end
        end as season,

        -- Time dimensions
        dayname(date) as day_of_week,
        monthname(date) as month_name,
        extract(year from date) as year,
        extract(month from date) as month_number

    from daily_weather
)

select * from with_metrics