{{ config(
    materialized="table",
    tags=["marts"]
    )
}}

with country_inflation as (
    select
        period_month,
        country_code,
        headline,
        core,
        energy,
        food,
        services,
        non_energy_goods
    from {{ ref('int_inflation_pivoted') }}
)

, euro_area as (
    select
        period_month,
        headline as ea_headline
    from {{ ref('int_inflation_pivoted') }}
    where country_code = 'U2'
)

, metadata as (
    select
        country_code,
        country_name
    from {{ ref('country_metadata') }}
)

select 
    ci.period_month,
    ci.country_code,
    m.country_name,
    ci.headline,
    ci.core,
    ci.energy,
    ci.food,
    ci.services,
    ci.non_energy_goods,
    ci.headline - 2.0 as gap_vs_target,
    ci.headline - ea.ea_headline as gap_vs_euro_area
from country_inflation ci
left join euro_area ea
    on ci.period_month = ea.period_month
left join metadata m 
    on ci.country_code = m.country_code
