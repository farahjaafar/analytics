{{ config(
    materialized="view", 
    tags=["intermediate"]
    ) 
}}

with inflation_long as (
    select * from {{ ref('stg_inflation') }}
)

select 
    period_month,
    country_code,
    max(case when component = 'headline' then inflation_rate end) as headline,
    max(case when component = 'core' then inflation_rate end) as core,
    max(case when component = 'energy' then inflation_rate end) as energy,
    max(case when component = 'food' then inflation_rate end) as food,
    max(case when component = 'services' then inflation_rate end) as services,
    max(case when component = 'non_energy_goods' then inflation_rate end) as non_energy_goods
from inflation_long
group by period_month, country_code