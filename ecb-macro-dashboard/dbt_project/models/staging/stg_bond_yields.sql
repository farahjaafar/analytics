{{ config(
    materialized="view",
    tags=["staging"]
) }}

with source as (
    select * from {{ source('raw_ecb', 'bond_yields') }}
)

, cleaned as (
    select
        TIME_PERIOD::date as period_date,
        case 
            when DATA_TYPE_FM like '%SR_2Y%' then '2Y'
            when DATA_TYPE_FM like '%SR_10Y%' then '10Y'
        end as maturity,
        cast(OBS_VALUE as double) as yield_pct
    from source
    where OBS_VALUE is not null
)

select * from cleaned
where maturity is not null