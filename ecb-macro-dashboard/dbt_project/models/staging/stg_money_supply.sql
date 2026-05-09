{{ config(
    materialized="view",
    tags=["staging"]
) }}

with source as (
    select * from {{ source('raw_ecb', 'money_supply') }}
)

, cleaned as (
    select
        (TIME_PERIOD || '-01')::date as period_month,
        cast(OBS_VALUE as double) as m3_growth_yoy
    from source
    where OBS_VALUE is not null
)

select * from cleaned