{{ config(
    materialized="view", 
    tags=["intermediate"]
)}}

with date_spine as (
    select
        unnest(
            generate_series(date '2000-01-01', current_date, interval '1 month') 
            )::date as period_month
)

, rate_changes as (
    select 
        date_trunc('month', period_date)::date as change_month,
        rate_type,
        rate_value
    from {{ ref('stg_interest_rates') }}
)

-- for months with multiple changes, we take only the last change in each month
, last_change_per_month as (
    select
        change_month,
        rate_type,
        last(rate_value order by change_month) as rate_value
    from rate_changes
    group by change_month, rate_type
)

, spine_by_rate_type as (
    select
        d.period_month,
        rt.rate_type,
    from date_spine d
    cross join (select distinct rate_type from last_change_per_month) rt
)

, joined as (
    select
        s.period_month,
        s.rate_type,
        c.rate_value
    from spine_by_rate_type s
    left join last_change_per_month c
        on s.period_month = c.change_month
        and s.rate_type = c.rate_type
)

select 
    period_month,
    rate_type,
    last_value(rate_value ignore nulls) over (
        partition by rate_type
        order by period_month
        rows between unbounded preceding and current row 
    ) as rate_value
from joined
qualify rate_value is not null
