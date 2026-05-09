{{ config(
    materialized="view",
    tags=["staging"]
) }}

with source as (
    select * from {{ source('raw_ecb', 'interest_rates') }}
)

, cleaned as (
    select 
        TIME_PERIOD::date as period_date,
        case 
            when PROVIDER_FM_ID like '%MRR_RT%' then 'main_refinancing'
            when PROVIDER_FM_ID like '%DFR%' then 'deposit_facility'
            when PROVIDER_FM_ID like '%MLFR%' then 'marginal_lending'
        end as rate_type,
        cast(OBS_VALUE as double) as rate_value
    from source
    where OBS_VALUE is not null
)

select * from cleaned
where rate_type is not null