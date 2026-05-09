---
title: Inflation
---

How euro area prices are moving against the ECB's 2% target, and where individual member states sit within the bloc.

> **About these numbers.** All values are **year-over-year percent change** in the Harmonised Index of Consumer Prices (HICP). The ECB's mandate is to keep medium-term inflation **at 2%** — above is too hot, below 0% is deflation. "Core" strips out volatile food + energy.

## Latest snapshot

```sql ea_latest
select
  round(headline, 1) as headline,
  round(core, 1) as core,
  round(gap_vs_target, 1) as gap_vs_target,
  strftime(period_month, '%b %Y') as month_label
from ecb.mart_inflation_comparison
where (country_code in ('U2', 'EA') or country_name ilike '%euro area%')
  and period_month = (select max(period_month) from ecb.mart_inflation_comparison)
limit 1
```

```sql extremes
with latest as (
  select * from ecb.mart_inflation_comparison
  where period_month = (select max(period_month) from ecb.mart_inflation_comparison)
    and country_code not in ('U2', 'EA')
    and (country_name not ilike '%euro area%' or country_name is null)
)
select
  (select country_name        from latest order by headline desc limit 1) as highest_country,
  (select round(headline, 1)  from latest order by headline desc limit 1) as highest_value,
  (select country_name        from latest order by headline asc  limit 1) as lowest_country,
  (select round(headline, 1)  from latest order by headline asc  limit 1) as lowest_value
```

<Grid cols=3>
  <BigValue data={ea_latest} value=headline       title="Euro area headline (%)" fmt="#,##0.0"/>
  <BigValue data={ea_latest} value=core           title="Euro area core (%)"     fmt="#,##0.0"/>
  <BigValue data={ea_latest} value=gap_vs_target  title="Gap vs 2% target (pp)"  fmt="#,##0.0"/>
</Grid>

**Latest data: {ea_latest[0].month_label}**

- Euro area **headline** at **{ea_latest[0].headline}%**, **core** at **{ea_latest[0].core}%**
- Gap vs ECB 2% target: **{ea_latest[0].gap_vs_target} pp**
- Hottest member state: **{extremes[0].highest_country}** at **{extremes[0].highest_value}%**
- Coolest member state: **{extremes[0].lowest_country}** at **{extremes[0].lowest_value}%**

## Country comparison — headline over time

> **Showing major euro-area economies + the bloc aggregate.** All other tracked countries are still in the [Full monthly history](#full-monthly-history) table at the bottom of the page.

```sql country_headline_trend
select
  period_month,
  country_name,
  headline
from ecb.mart_inflation_comparison
where country_code in ('U2', 'EA', 'DE', 'FR', 'IT', 'ES', 'NL')
   or country_name ilike '%euro area%'
order by period_month, country_name
```

<LineChart
  data={country_headline_trend}
  x=period_month
  y=headline
  series=country_name
  title="Headline inflation — major economies (% YoY)"
  yFmt="#,##0.0"
/>

> **Reading this chart.** Each line is one country (or the euro area aggregate). Look for the **2022 spike** — Germany and France peaked nearer 10%, while Italy and Spain followed similar paths. The convergence back toward 2% from 2024 onward shows how the ECB's tightening cycle worked through the bloc.

## Gap vs ECB 2% target — latest month

```sql gap_latest
select
  country_name,
  round(gap_vs_target, 1) as gap_vs_target,
  case when gap_vs_target > 0 then 'above target'
       when gap_vs_target < 0 then 'below target'
       else 'at target'
  end as direction
from ecb.mart_inflation_comparison
where period_month = (select max(period_month) from ecb.mart_inflation_comparison)
order by gap_vs_target
```

```sql gap_summary
with latest as (
  select * from ecb.mart_inflation_comparison
  where period_month = (select max(period_month) from ecb.mart_inflation_comparison)
)
select
  count(*) filter (where gap_vs_target > 0) as above_count,
  count(*) filter (where gap_vs_target < 0) as below_count,
  count(*) filter (where gap_vs_target = 0) as at_count,
  count(*) as total_count,
  strftime(max(period_month), '%b %Y') as month_label
from latest
```

<BarChart
  data={gap_latest}
  x=country_name
  y=gap_vs_target
  series=direction
  title="Gap vs ECB 2% target (percentage points)"
  swapXY=true
/>

> **Reading this chart.** Each bar is one country's gap from the ECB's 2% target in **{gap_summary[0].month_label}**. Bars **right of zero** are running hot; **left of zero** are below target. Of **{gap_summary[0].total_count}** entities tracked, **{gap_summary[0].above_count}** are above target and **{gap_summary[0].below_count}** are below.

## Euro area — what's driving the headline number

```sql ea_components
with ea as (
  select * from ecb.mart_inflation_comparison
  where country_code in ('U2', 'EA') or country_name ilike '%euro area%'
)
select period_month, 'headline' as component, headline as value from ea union all
select period_month, 'core'     as component, core               from ea union all
select period_month, 'energy'   as component, energy             from ea union all
select period_month, 'food'     as component, food               from ea union all
select period_month, 'services' as component, services           from ea
order by period_month, component
```

<LineChart
  data={ea_components}
  x=period_month
  y=value
  series=component
  title="Euro area inflation — by component (% YoY)"
  yFmt="#,##0.0"
/>

> **Reading this chart.** **Headline** is what households experience. **Core** strips out the two most volatile pieces (food + energy) — it's what the ECB watches because it's stickier. **Energy** spiked hardest in 2022 (Russia/Ukraine), pulling headline far above core. **Services** is the slowest to turn — it lags goods inflation by 6–12 months, so it's often the last component to come back to target.

This is the inflation that drove the ECB's tightening cycle — every Governing Council decision is on the [Monetary policy](/monetary-policy) page.

## Full monthly history

```sql full_inflation
select
  strftime(period_month, '%Y-%m-%d') as period_month,
  country_name,
  round(headline, 2)      as headline,
  round(core, 2)          as core,
  round(energy, 2)        as energy,
  round(food, 2)          as food,
  round(services, 2)      as services,
  round(gap_vs_target, 2) as gap_vs_target
from ecb.mart_inflation_comparison
order by period_month desc, country_name
```

<DataTable data={full_inflation} rows=20 search=true />

## Related

- [← Back to overview](/)
- [Monetary policy](/monetary-policy) — how the ECB responded to these prints
- [Currency & external](/currency) — the FX side of the inflation story
- [Pipeline Health](/pipeline) — data freshness and sources
