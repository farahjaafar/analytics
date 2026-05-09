---
title: Monetary Policy
---

Every Deposit Facility Rate (DFR) decision in our dataset, with a snapshot of inflation and the yield curve at each decision moment.

> **About the DFR.** The Deposit Facility Rate is what banks earn on overnight deposits parked at the ECB. Since 2014 it has been the rate markets watch most closely — when liquidity is abundant, banks would rather earn the DFR than lend interbank, so the DFR effectively becomes the floor for short-term euro rates. The ECB also sets two companion rates (MRR and MLFR) but those are not yet covered in this dashboard's seed data.

```sql data_window
select
  strftime(min(decision_date), '%b %Y')   as earliest,
  strftime(max(decision_date), '%b %Y')   as latest,
  count(*)                                 as total_decisions,
  count(distinct rate_type)                as rate_types_seeded
from ecb.mart_monetary_policy_timeline
```

> **Data note.** This page covers ECB Governing Council decisions from **{data_window[0].earliest}** to **{data_window[0].latest}** ({data_window[0].total_decisions} decisions, {data_window[0].rate_types_seeded} rate type seeded). The decision history is sourced from a hand-curated seed CSV — newer decisions and the MRR/MLFR rate types will appear once the seed is updated (tracked in `FUTURE.local.md`).

## Latest decision

```sql most_recent
select
  strftime(decision_date, '%d %b %Y')    as decision_label,
  rate_type,
  old_rate,
  new_rate,
  change_bps,
  case when change_bps > 0 then 'Hike'
       when change_bps < 0 then 'Cut'
       else 'Hold'
  end as direction,
  abs(change_bps) as abs_bps,
  round(headline_inflation, 1) as inflation_at_decision
from ecb.mart_monetary_policy_timeline
order by decision_date desc, rate_type
limit 1
```

<Grid cols=3>
  <BigValue data={most_recent} value=direction       title="Most recent action | {most_recent[0].decision_label}"/>
  <BigValue data={most_recent} value=new_rate        title="{most_recent[0].rate_type} after decision (%)" fmt="#,##0.00"/>
  <BigValue data={most_recent} value=abs_bps         title="Move size (bps)"/>
</Grid>

The most recent decision was a **{most_recent[0].direction}** of **{most_recent[0].abs_bps} bps** on the **{most_recent[0].rate_type}** ({most_recent[0].old_rate}% → {most_recent[0].new_rate}%) on **{most_recent[0].decision_label}**, when headline inflation was running at **{most_recent[0].inflation_at_decision}%**.

## Recent decisions

```sql latest_decisions
select
  strftime(decision_date, '%d %b %Y') as decision_date_label,
  decision_date,
  rate_type,
  old_rate,
  new_rate,
  change_bps,
  case when change_bps > 0 then 'hike'
       when change_bps < 0 then 'cut'
       else 'hold'
  end as direction,
  round(headline_inflation, 1) as inflation_at_decision
from ecb.mart_monetary_policy_timeline
order by decision_date desc, rate_type
limit 5
```

<DataTable data={latest_decisions} />

## Decision history

```sql decisions_filtered
select
  decision_date,
  rate_type,
  change_bps,
  case when change_bps > 0 then 'hike'
       when change_bps < 0 then 'cut'
       else 'hold'
  end as direction
from ecb.mart_monetary_policy_timeline
where change_bps != 0
order by decision_date
```

<BarChart
  data={decisions_filtered}
  x=decision_date
  y=change_bps
  series=direction
  title="Rate changes (basis points)"
/>

> **Reading this chart.** Each bar is one ECB decision. **Above zero = a hike, below zero = a cut.** The cluster of large positive bars in 2022–23 was the steepest tightening cycle in ECB history; the run of negative bars from late 2024 onward is the disinflation-driven cutting cycle.

## Path of policy rates over time

```sql rate_levels
select
  decision_date,
  rate_type,
  new_rate
from ecb.mart_monetary_policy_timeline
order by decision_date
```

<LineChart
  data={rate_levels}
  x=decision_date
  y=new_rate
  series=rate_type
  title="ECB policy rates — actual levels (%)"
/>

```sql rate_path_summary
select
  round((select new_rate         from ecb.mart_monetary_policy_timeline order by decision_date desc limit 1), 2) as latest_rate,
  round((select min(new_rate)    from ecb.mart_monetary_policy_timeline), 2) as all_time_low,
  round((select max(new_rate)    from ecb.mart_monetary_policy_timeline), 2) as all_time_high,
  (select strftime(decision_date, '%b %Y') from ecb.mart_monetary_policy_timeline order by new_rate asc  limit 1) as low_month,
  (select strftime(decision_date, '%b %Y') from ecb.mart_monetary_policy_timeline order by new_rate desc limit 1) as high_month
```

**Reading the levels chart.** The DFR is currently at **{rate_path_summary[0].latest_rate}%**. Across the full series, it ranged from a low of **{rate_path_summary[0].all_time_low}% in {rate_path_summary[0].low_month}** to a high of **{rate_path_summary[0].all_time_high}% in {rate_path_summary[0].high_month}**.

Notice the long flatline at or below zero from 2014 to 2022 — that was the negative-rates era, an unprecedented experiment that ended when post-COVID inflation forced the ECB to hike. The 2022–23 climb to 4.00% was the fastest tightening in ECB history.

## Full decision timeline

Every decision with the macro snapshot at that moment.

```sql full_timeline
select
  strftime(decision_date, '%Y-%m-%d') as decision_date,
  rate_type,
  old_rate,
  new_rate,
  change_bps,
  round(headline_inflation, 2) as headline_infl_pct,
  round(core_inflation, 2) as core_infl_pct,
  is_inverted as yield_inverted,
  context_note
from ecb.mart_monetary_policy_timeline
order by decision_date desc
```

<DataTable data={full_timeline} rows=15 search=true />

## Related

- [← Back to overview](/)
- [Inflation](/inflation) — what drove these decisions
- [Currency & external](/currency) — how the euro responded
- [Pipeline Health](/pipeline) — data freshness and sources