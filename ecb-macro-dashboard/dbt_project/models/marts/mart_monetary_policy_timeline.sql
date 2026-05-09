{{ config(
    materialized="table",
    tags=["marts"]
    )
}}

with decisions as (
    select 
        decision_date::date as decision_date,
        rate_type,
        old_rate,
        new_rate,
        change_bps,
        context_note
    from {{ ref('ecb_rate_decisions') }}
)

, inflation as (
    select 
        period_month,
        headline as headline_inflation,
        core as core_inflation
    from {{ ref('int_inflation_pivoted') }}
    where country_code = 'U2'
)

, yields as (
    select
        period_month,
        spread as yield_curve_spread,
        is_inverted
    from {{ ref('int_yield_curve_spread') }}
)

, fx as (
    select
        period_month,
        monthly_avg_rate as eur_usd,
    from {{ ref('int_exchange_rate_monthly') }}
    where currency_pair = 'EUR/USD'
)

, money as (
    select
        period_month,
        m3_growth_yoy
    from {{ ref('stg_money_supply') }}
)

select
    d.decision_date,
    d.rate_type,
    d.old_rate,
    d.new_rate,
    d.change_bps,
    d.context_note,
    i.headline_inflation,
    i.core_inflation,
    y.yield_curve_spread,
    y.is_inverted,
    f.eur_usd,
    m.m3_growth_yoy
from decisions d
left join inflation i
    on date_trunc('month', d.decision_date)::date = i.period_month
left join yields y
    on date_trunc('month', d.decision_date)::date = y.period_month
left join fx f
    on date_trunc('month', d.decision_date)::date = f.period_month
left join money m
    on date_trunc('month', d.decision_date)::date = m.period_month