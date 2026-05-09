{{ config(
    materialized="view", 
    tags=["intermediate"]
    )
}}

with rates as (
    select
        period_month,
        rate_value as deposit_rate
    from {{ ref('int_interest_rates_monthly') }}
    where rate_type = 'deposit_facility'     
)

, inflation as (
    select
        period_month,
        headline as headline_inflation
    from {{ ref('int_inflation_pivoted') }}
    where country_code = 'U2'
)

select 
    r.period_month,
    r.deposit_rate,
    i.headline_inflation,
    r.deposit_rate - i.headline_inflation as real_rate
from rates r
left join inflation i
    on r.period_month = i.period_month