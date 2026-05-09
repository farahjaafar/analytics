{{ config(
    materialized="view", 
    tags=["staging"]
) }}

with source as (
    select * from {{ source('raw_ecb', 'inflation') }}
)

, cleaned as (
    select 
        (TIME_PERIOD || '-01')::date as period_month,
        REF_AREA as country_code,
        case ICP_ITEM
            when '000000' then 'headline'
            when 'XEF000' then 'core'
            when 'NRGY00' then 'energy'
            when 'FOOD00' then 'food'
            when 'SERV00' then 'services'
            when 'IGXE00' then 'non_energy_goods'
            end as component,
        cast(OBS_VALUE as double) as inflation_rate
    from source
    where OBS_VALUE is not null
)

select * from cleaned