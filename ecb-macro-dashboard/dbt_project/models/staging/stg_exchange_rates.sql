{{ config(
    materialized="view",
    tags=["staging"]
) }}

with source as (
    select * from {{ source('raw_ecb', 'exchange_rates') }}
)

, cleaned as (
    select 
        TIME_PERIOD::date as period_date,
        -- Build a human-readable pair label. All ECB EXR rates
        -- are quoted as FOREIGN per 1 EUR, so "EUR/USD" = how many
        -- USD you get for 1 EUR.
        'EUR/' || CURRENCY as currency_pair,
        CURRENCY as currency_code,
        cast(OBS_VALUE as double) as exchange_rate
    from source
    where OBS_VALUE is not null
)

select * from cleaned