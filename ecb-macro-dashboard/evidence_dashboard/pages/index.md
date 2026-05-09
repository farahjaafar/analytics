---
title: ECB Macro Dashboard
---

A single-page snapshot of euro area macroeconomic conditions — prices, policy rates, the yield curve, and the euro itself. Each section links into a deeper page if you want detail.

> **About this dashboard.** Built as a portfolio data-engineering project: extract from **ECB SDW** + **Eurostat** APIs, transformed in **dbt** (DuckDB), surfaced in **Evidence**, and refreshed automatically via **GitHub Actions** on a weekly cadence. Series start in **2014** and run through the latest released month. Source code: [github.com/farahjaafar/analytics](https://github.com/farahjaafar/analytics).

## Latest snapshot

> **Why each tile shows a different month.** The underlying sources publish on different schedules. **Headline inflation** is released by Eurostat 2–3 weeks after month-end, so it lags. The **Deposit Facility Rate** updates only when the ECB Governing Council changes it (so the date marks the most recent change, not "today"). The **Real policy rate** combines the two, so it's only as fresh as the older of the pair (inflation). **10Y–2Y spread** and **EUR/USD** come from daily ECB market data and are typically the most current.

```sql latest_macro
select
  (select round(headline_inflation, 1)     from ecb.mart_macro_overview where headline_inflation  is not null order by period_month desc limit 1) as headline_inflation,
  (select strftime(period_month, '%b %Y')  from ecb.mart_macro_overview where headline_inflation  is not null order by period_month desc limit 1) as headline_inflation_month,
  (select round(deposit_rate, 2)           from ecb.mart_macro_overview where deposit_rate        is not null order by period_month desc limit 1) as deposit_rate,
  (select strftime(period_month, '%b %Y')  from ecb.mart_macro_overview where deposit_rate        is not null order by period_month desc limit 1) as deposit_rate_month,
  (select round(real_rate, 2)              from ecb.mart_macro_overview where real_rate           is not null order by period_month desc limit 1) as real_rate,
  (select strftime(period_month, '%b %Y')  from ecb.mart_macro_overview where real_rate           is not null order by period_month desc limit 1) as real_rate_month,
  (select round(yield_curve_spread, 2)     from ecb.mart_macro_overview where yield_curve_spread  is not null order by period_month desc limit 1) as yield_curve_spread,
  (select strftime(period_month, '%b %Y')  from ecb.mart_macro_overview where yield_curve_spread  is not null order by period_month desc limit 1) as yield_curve_spread_month,
  (select round(eur_usd, 4)                from ecb.mart_macro_overview where eur_usd             is not null order by period_month desc limit 1) as eur_usd,
  (select strftime(period_month, '%b %Y')  from ecb.mart_macro_overview where eur_usd             is not null order by period_month desc limit 1) as eur_usd_month
```

<Grid cols=5>
  <BigValue data={latest_macro} value=headline_inflation  title="Headline inflation (%) | {latest_macro[0].headline_inflation_month}"  fmt="#,##0.0"/>
  <BigValue data={latest_macro} value=deposit_rate        title="Deposit Facility Rate (%) | {latest_macro[0].deposit_rate_month}" fmt="#,##0.00"/>
  <BigValue data={latest_macro} value=real_rate           title="Real policy rate (pp) | {latest_macro[0].real_rate_month}"   fmt="#,##0.00"/>
  <BigValue data={latest_macro} value=yield_curve_spread  title="10Y–2Y spread (pp) | {latest_macro[0].yield_curve_spread_month}"      fmt="#,##0.00"/>
  <BigValue data={latest_macro} value=eur_usd             title="EUR/USD | {latest_macro[0].eur_usd_month}"                 fmt="#,##0.0000"/>
</Grid>

- **Real policy rate** = deposit rate − headline inflation. Above zero ⇒ ECB stance is *restrictive*; below zero ⇒ *accommodative*.
- **10Y–2Y spread** is the slope of the yield curve. Negative ⇒ *inverted* (historically a recession signal).

## The ECB story — inflation vs policy rate

```sql inflation_vs_rate
select period_month, 'Headline inflation (%)' as series, headline_inflation as value from ecb.mart_macro_overview union all
select period_month, 'Deposit rate (%)'       as series, deposit_rate              from ecb.mart_macro_overview
order by period_month, series
```

<LineChart
  data={inflation_vs_rate}
  x=period_month
  y=value
  series=series
  title="Euro area: inflation vs ECB deposit rate"
  yFmt="#,##0.0"
/>

> **Reading this chart.** This is the central monetary-policy narrative in one image. From 2014 to mid-2022 the ECB held the DFR at **−0.50%** (the negative-rates era) while inflation hovered near or below target. Then the post-COVID and energy-price shock pushed headline inflation toward **10%**, triggering the **fastest hiking cycle in ECB history** — DFR climbed from −0.50% to **4.00%** between July 2022 and September 2023. Inflation has since converged back toward 2%, opening the door to the cutting cycle that began mid-2024.

## Yield curve — 2Y, 10Y, and the spread

```sql yield_curve
select period_month, '2Y yield'      as series, yield_2Y           as value from ecb.mart_macro_overview union all
select period_month, '10Y yield'     as series, yield_10Y                  from ecb.mart_macro_overview union all
select period_month, '10Y–2Y spread' as series, yield_curve_spread         from ecb.mart_macro_overview
order by period_month, series
```

<LineChart
  data={yield_curve}
  x=period_month
  y=value
  series=series
  title="Euro area yield curve — short, long, and slope"
  yFmt="#,##0.00"
/>

```sql inversion_summary
select
  count(*) filter (where is_inverted) as inverted_months,
  count(*) as total_months,
  round(100.0 * count(*) filter (where is_inverted) / count(*), 1) as inverted_pct
from ecb.mart_macro_overview
```

> **Reading this chart.** The **2Y** tracks short-term policy-rate expectations; the **10Y** reflects long-term growth + inflation expectations. The **spread** (10Y minus 2Y) is the curve's slope — positive in normal times, negative when markets expect future rate cuts. The euro area curve was inverted in **{inversion_summary[0].inverted_months} of {inversion_summary[0].total_months} months ({inversion_summary[0].inverted_pct}%)** in this window — most of it during the 2022–24 hiking cycle.

## EUR/USD over time

```sql eur_usd_overview
select period_month, eur_usd
from ecb.mart_macro_overview
order by period_month
```

<LineChart
  data={eur_usd_overview}
  x=period_month
  y=eur_usd
  title="EUR/USD — monthly average"
  yFmt="#,##0.0000"
/>

```sql eurusd_extremes
select
  round((select eur_usd from ecb.mart_macro_overview order by period_month desc limit 1), 4) as latest,
  round((select min(eur_usd) from ecb.mart_macro_overview), 4) as low,
  (select strftime(period_month, '%b %Y') from ecb.mart_macro_overview order by eur_usd asc  limit 1) as low_month,
  round((select max(eur_usd) from ecb.mart_macro_overview), 4) as high,
  (select strftime(period_month, '%b %Y') from ecb.mart_macro_overview order by eur_usd desc limit 1) as high_month
```

> **Reading this chart.** Latest: **{eurusd_extremes[0].latest}**. All-time low: **{eurusd_extremes[0].low}** in **{eurusd_extremes[0].low_month}** (the September 2022 parity moment, when 1 EUR briefly bought less than 1 USD for the first time in 20 years). All-time high: **{eurusd_extremes[0].high}** in **{eurusd_extremes[0].high_month}**. For more FX detail across other currencies, see [Currency & external](/currency).

## See also

- [Inflation](/inflation) — country comparison, components, gap vs the ECB 2% target
- [Monetary policy](/monetary-policy) — every rate decision with the macro snapshot at that moment
- [Currency & external](/currency) — EUR vs USD, GBP, JPY, CHF, PLN with rolling averages
- [Pipeline Health](/pipeline) — data freshness and row counts
