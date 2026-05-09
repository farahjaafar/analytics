{{ config(
    materialized="view", 
    tags=["intermediate"]   
    )
}}

with monthly_yields as (
    select
        date_trunc('month', period_date)::date as period_month,
        maturity,
        avg(yield_pct) as avg_yield
    from {{ ref('stg_bond_yields') }}
    group by 1,2
)

select 
    period_month,
    max(case when maturity = '2Y' then avg_yield end) as yield_2Y,
    max(case when maturity = '10Y' then avg_yield end) as yield_10Y,
    max(case when maturity = '10Y' then avg_yield end) 
        - max(case when maturity = '2Y' then avg_yield end) as spread,
    (max(case when maturity = '10Y' then avg_yield end) 
        < max(case when maturity = '2Y' then avg_yield end)) as is_inverted
from monthly_yields
group by period_month