---
title: Pipeline Health
---

Freshness, row counts, and provenance for each mart that powers this dashboard.

> **How to read this page.** The dashboard is rebuilt weekly by GitHub Actions: extract from upstream APIs → load into DuckDB → dbt transformations → CSV export → Evidence build on Vercel. Each mart below has a different upstream cadence, so the "freshness" varies by metric.

## Mart freshness

```sql freshness
with bounds as (
  select 'mart_macro_overview'           as mart, min(period_month)::date as earliest, max(period_month)::date as latest from ecb.mart_macro_overview union all
  select 'mart_inflation_comparison'     as mart, min(period_month)::date,             max(period_month)::date            from ecb.mart_inflation_comparison union all
  select 'mart_monetary_policy_timeline' as mart, min(decision_date)::date,            max(decision_date)::date           from ecb.mart_monetary_policy_timeline union all
  select 'mart_currency_strength'        as mart, min(period_month)::date,             max(period_month)::date            from ecb.mart_currency_strength
)
select
  mart,
  earliest,
  latest,
  date_diff('day', latest, current_date) as days_old,
  case
    when date_diff('day', latest, current_date) <= 35  then '🟢 fresh'
    when date_diff('day', latest, current_date) <= 90  then '🟡 aging'
    else                                                    '🔴 stale'
  end as status
from bounds
order by mart
```

<DataTable data={freshness} />

> **Status thresholds.** 🟢 fresh = updated within 35 days · 🟡 aging = 36–90 days old · 🔴 stale = older than 90 days. Two marts are currently stale by design: `mart_monetary_policy_timeline` is sourced from a hand-curated seed CSV (last decision: Mar 2025), and `mart_inflation_comparison` is bounded by Eurostat country-HICP release lag — both are tracked in `FUTURE.local.md`.

## Row counts

```sql row_counts
select 'mart_macro_overview'           as mart, count(*) as rows from ecb.mart_macro_overview union all
select 'mart_inflation_comparison'     as mart, count(*)         from ecb.mart_inflation_comparison union all
select 'mart_monetary_policy_timeline' as mart, count(*)         from ecb.mart_monetary_policy_timeline union all
select 'mart_currency_strength'        as mart, count(*)         from ecb.mart_currency_strength
order by mart
```

<DataTable data={row_counts} />

## Mart descriptions & sources

| Mart | What it is | Upstream source | Refresh cadence |
|---|---|---|---|
| `mart_macro_overview` | One row per month with the full macro picture: inflation, deposit rate, real rate, 2Y/10Y yields, EUR/USD | ECB SDW + Eurostat (joined) | Monthly |
| `mart_inflation_comparison` | One row per country-month with HICP headline, core, and components (energy, food, services) plus gap vs 2% target | Eurostat HICP API | Monthly (2–3 weeks after month-end) |
| `mart_monetary_policy_timeline` | One row per ECB Governing Council rate decision with old/new rate, change in bps, and the macro snapshot at that moment | Hand-curated seed CSV | Manual (when ECB decides) |
| `mart_currency_strength` | One row per FX pair-month with monthly average, MoM/YoY change, and 3/6/12-month rolling averages for EUR vs USD/GBP/JPY/CHF/PLN | ECB SDW FX rates | Daily upstream, aggregated monthly |

## Related

- [← Back to overview](/)
- [Inflation](/inflation)
- [Monetary policy](/monetary-policy)
- [Currency & external](/currency)
