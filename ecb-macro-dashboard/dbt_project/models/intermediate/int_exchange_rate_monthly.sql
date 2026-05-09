{{ config(
    materialized="view", 
    tags=["intermediate"]
    )
}}

with monthly as (
    select 
        date_trunc('month', period_date)::date as period_month,
        currency_pair,
        avg(exchange_rate) as monthly_avg_rate
    from {{ ref('stg_exchange_rates') }}
    group by 1,2
)

select 
    period_month,
    currency_pair,
    monthly_avg_rate,
    lag(monthly_avg_rate, 1) over (
            partition by currency_pair order by period_month) as prev_month_rate,
    lag(monthly_avg_rate, 12) over (
            partition by currency_pair order by period_month) as year_ago_rate,
    -- MoM % change 
    (monthly_avg_rate - lag(monthly_avg_rate, 1) over (
            partition by currency_pair order by period_month)) 
        / lag(monthly_avg_rate, 1) over (
            partition by currency_pair order by period_month
    ) * 100 as mom_pct_change,
    -- YoY % change
    (monthly_avg_rate - lag(monthly_avg_rate, 12) over (
            partition by currency_pair order by period_month)) 
        / lag(monthly_avg_rate, 12) over (
            partition by currency_pair order by period_month
    ) * 100 as yoy_pct_change
from monthly