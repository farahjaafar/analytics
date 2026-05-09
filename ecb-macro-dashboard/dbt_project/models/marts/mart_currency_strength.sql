{{ config(
    materialized="table",
    tags=["marts"]
    )
}}

with fx as (
    select
        period_month,
        currency_pair,
        monthly_avg_rate,
        mom_pct_change,
        yoy_pct_change
    from {{ ref('int_exchange_rate_monthly') }}
)

select 
    period_month,
    currency_pair,
    monthly_avg_rate,
    mom_pct_change,
    yoy_pct_change,
    {{ calc_rolling_average('monthly_avg_rate', 'currency_pair', 'period_month', 3) }} as ma_3m,
    {{ calc_rolling_average('monthly_avg_rate', 'currency_pair', 'period_month', 6) }} as ma_6m,
    {{ calc_rolling_average('monthly_avg_rate', 'currency_pair', 'period_month', 12) }} as ma_12m
from fx