{{ config(
    materialized="table", 
    tags=["marts"]
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
        headline as headline_inflation,
        core as core_inflation,
        energy as energy_inflation
    from {{ ref('int_inflation_pivoted') }}
    where country_code = 'U2'
)

, money as (
    select 
        period_month,
        m3_growth_yoy
    from {{ ref('stg_money_supply') }}
)

, yields as (
    select
        period_month,
        yield_2Y,
        yield_10Y,
        spread as yield_curve_spread,
        is_inverted
    from {{ ref('int_yield_curve_spread') }}
)

, fx as (
    select 
        period_month,
        monthly_avg_rate as eur_usd
    from {{ ref('int_exchange_rate_monthly') }}
    where currency_pair = 'EUR/USD'
)

, real_rate as (
    select 
        period_month,
        real_rate
    from {{ ref('int_real_interest_rate') }}
)

select 
    r.period_month,
    r.deposit_rate,
    i.headline_inflation,
    i.core_inflation,
    i.energy_inflation,
    rr.real_rate,
    m.m3_growth_yoy,
    y.yield_2Y,
    y.yield_10Y,
    yield_curve_spread,
    y.is_inverted,
    f.eur_usd
from rates r 
left join inflation i
    on r.period_month = i.period_month
left join money m
    on r.period_month = m.period_month
left join yields y
    on r.period_month = y.period_month
left join fx f
    on r.period_month = f.period_month
left join real_rate rr
    on r.period_month = rr.period_month