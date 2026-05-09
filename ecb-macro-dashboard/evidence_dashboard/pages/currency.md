---
title: Currency & External
---

How the euro has moved against major currencies, with short- and long-term trend context.

> **How to read this page.** The euro is the *base* currency, so e.g. **EUR/USD = 1.10** means **1 euro buys 1.10 dollars**. A rising line ⇒ euro strengthening. A falling line ⇒ euro weakening. Each section zooms in on a different lens: the latest snapshot, the EUR/USD trend, all currencies side-by-side, then the raw monthly data.


## Latest monthly averages

```sql latest_fx
select
  currency_pair,
  period_month,
  monthly_avg_rate,
  mom_pct_change,
  yoy_pct_change,
  strftime(period_month, '%b %Y') as month_label
from ecb.mart_currency_strength
where period_month = (select max(period_month) from ecb.mart_currency_strength)
  and currency_pair in ('EUR/USD', 'EUR/GBP', 'EUR/JPY', 'EUR/CHF', 'EUR/PLN')
order by currency_pair
```

<Grid cols=5>
  <BigValue
    data={latest_fx.filter(d => d.currency_pair === 'EUR/USD')}
    value=monthly_avg_rate
    title="EUR/USD"
    comparison=yoy_pct_change
    comparisonFmt="pct1"
    comparisonTitle="YoY"
    fmt="#,##0.0000"
  />
  <BigValue
    data={latest_fx.filter(d => d.currency_pair === 'EUR/GBP')}
    value=monthly_avg_rate
    title="EUR/GBP"
    comparison=yoy_pct_change
    comparisonFmt="pct1"
    comparisonTitle="YoY"
    fmt="#,##0.0000"
  />
  <BigValue
    data={latest_fx.filter(d => d.currency_pair === 'EUR/JPY')}
    value=monthly_avg_rate
    title="EUR/JPY"
    comparison=yoy_pct_change
    comparisonFmt="pct1"
    comparisonTitle="YoY"
    fmt="#,##0.00"
  />
  <BigValue
    data={latest_fx.filter(d => d.currency_pair === 'EUR/CHF')}
    value=monthly_avg_rate
    title="EUR/CHF"
    comparison=yoy_pct_change
    comparisonFmt="pct1"
    comparisonTitle="YoY"
    fmt="#,##0.0000"
  />
  <BigValue
    data={latest_fx.filter(d => d.currency_pair === 'EUR/PLN')}
    value=monthly_avg_rate
    title="EUR/PLN"
    comparison=yoy_pct_change
    comparisonFmt="pct1"
    comparisonTitle="YoY"
    fmt="#,##0.0000"
  />
</Grid>

**Latest data: {latest_fx[0].month_label}**

```sql kpi_summary
with latest as (
  select * from ecb.mart_currency_strength
  where period_month = (select max(period_month) from ecb.mart_currency_strength)
)
select
  strftime(max(period_month), '%b %Y') as month,
  max(case when currency_pair = 'EUR/USD' then case when yoy_pct_change >= 0 then 'up' else 'down' end end) as usd_dir,
  max(case when currency_pair = 'EUR/USD' then round(abs(yoy_pct_change) * 100, 1) end) as usd_yoy_pct,
  max(case when currency_pair = 'EUR/GBP' then case when yoy_pct_change >= 0 then 'up' else 'down' end end) as gbp_dir,
  max(case when currency_pair = 'EUR/GBP' then round(abs(yoy_pct_change) * 100, 1) end) as gbp_yoy_pct,
  max(case when currency_pair = 'EUR/JPY' then case when yoy_pct_change >= 0 then 'up' else 'down' end end) as jpy_dir,
  max(case when currency_pair = 'EUR/JPY' then round(abs(yoy_pct_change) * 100, 1) end) as jpy_yoy_pct,
  max(case when currency_pair = 'EUR/CHF' then case when yoy_pct_change >= 0 then 'up' else 'down' end end) as chf_dir,
  max(case when currency_pair = 'EUR/CHF' then round(abs(yoy_pct_change) * 100, 1) end) as chf_yoy_pct,
  max(case when currency_pair = 'EUR/PLN' then case when yoy_pct_change >= 0 then 'up' else 'down' end end) as pln_dir,
  max(case when currency_pair = 'EUR/PLN' then round(abs(yoy_pct_change) * 100, 1) end) as pln_yoy_pct
from latest
```

**Reading the cards** (latest data: **{kpi_summary[0].month}**)

- **Big number** — the average exchange rate for the most recent complete month.
- **Chip below** — year-over-year change. Green ⇒ the euro strengthened vs that currency over the past 12 months. Red ⇒ it weakened.
- **Where the euro stands right now:**
  - vs **USD** — {kpi_summary[0].usd_dir} **{kpi_summary[0].usd_yoy_pct}%** YoY
  - vs **GBP** — {kpi_summary[0].gbp_dir} **{kpi_summary[0].gbp_yoy_pct}%** YoY
  - vs **JPY** — {kpi_summary[0].jpy_dir} **{kpi_summary[0].jpy_yoy_pct}%** YoY
  - vs **CHF** — {kpi_summary[0].chf_dir} **{kpi_summary[0].chf_yoy_pct}%** YoY
  - vs **PLN** — {kpi_summary[0].pln_dir} **{kpi_summary[0].pln_yoy_pct}%** YoY


## EUR/USD — rate vs. moving averages

```sql eur_usd_trend
select
  period_month,
  'spot'  as series, monthly_avg_rate as value from ecb.mart_currency_strength where currency_pair = 'EUR/USD' union all
select period_month, '3-month MA',  ma_3m  from ecb.mart_currency_strength where currency_pair = 'EUR/USD' union all
select period_month, '6-month MA',  ma_6m  from ecb.mart_currency_strength where currency_pair = 'EUR/USD' union all
select period_month, '12-month MA', ma_12m from ecb.mart_currency_strength where currency_pair = 'EUR/USD'
```

<LineChart
  data={eur_usd_trend}
  x=period_month
  y=value
  series=series
  title="EUR/USD: spot vs. rolling averages"
  yFmt="#,##0.0000"
/>

```sql eurusd_summary
with eur_usd as (
  select * from ecb.mart_currency_strength where currency_pair = 'EUR/USD'
)
select
  round((select monthly_avg_rate from eur_usd order by period_month desc limit 1), 4) as latest_spot,
  round((select ma_12m            from eur_usd order by period_month desc limit 1), 4) as latest_ma12,
  round((select monthly_avg_rate from eur_usd order by monthly_avg_rate asc  limit 1), 4) as all_time_low,
  (select strftime(period_month, '%b %Y') from eur_usd order by monthly_avg_rate asc  limit 1) as low_month,
  round((select monthly_avg_rate from eur_usd order by monthly_avg_rate desc limit 1), 4) as all_time_high,
  (select strftime(period_month, '%b %Y') from eur_usd order by monthly_avg_rate desc limit 1) as high_month
```

**Reading this chart.** The blue **spot** line is the actual monthly average. The other three lines are **rolling averages** over 3, 6, and 12 months — smoothers that filter out short-term noise. When spot crosses *above* the 12-month MA, the euro is strengthening relative to its recent past; when it crosses *below*, the opposite. Look for the dip near **parity (1.00) around September 2022** — that was the first time in 20 years the euro was worth less than a dollar.

Latest reading: spot is **{eurusd_summary[0].latest_spot}** vs 12-month MA at **{eurusd_summary[0].latest_ma12}**. All-time low: **{eurusd_summary[0].all_time_low}** in {eurusd_summary[0].low_month}. All-time high: **{eurusd_summary[0].all_time_high}** in {eurusd_summary[0].high_month}.


## Multi-currency strength — indexed to 100

```sql indexed_fx
with base as (
  select currency_pair, monthly_avg_rate
  from ecb.mart_currency_strength
  where period_month = (select min(period_month) from ecb.mart_currency_strength)
)
select
  c.period_month,
  c.currency_pair,
  100.0 * c.monthly_avg_rate / b.monthly_avg_rate as indexed_value
from ecb.mart_currency_strength c
join base b using (currency_pair)
where c.currency_pair in ('EUR/USD', 'EUR/GBP', 'EUR/JPY', 'EUR/CHF', 'EUR/PLN')
```

<LineChart
  data={indexed_fx}
  x=period_month
  y=indexed_value
  series=currency_pair
  title="Euro strength vs. major currencies (base = 100 at earliest month)"
  yFmt="#,##0"
/>

```sql indexed_summary
with first_last as (
  select
    currency_pair,
    first_value(monthly_avg_rate) over (partition by currency_pair order by period_month) as first_rate,
    last_value(monthly_avg_rate)  over (partition by currency_pair order by period_month
                                        rows between unbounded preceding and unbounded following) as last_rate
  from ecb.mart_currency_strength
  where currency_pair in ('EUR/USD', 'EUR/GBP', 'EUR/JPY', 'EUR/CHF', 'EUR/PLN')
  qualify row_number() over (partition by currency_pair order by period_month desc) = 1
)
select
  currency_pair,
  round(100 * (last_rate / first_rate - 1), 1) as pct_change_since_start
from first_last
order by pct_change_since_start desc
```

```sql indexed_extremes
with first_last as (
  select
    currency_pair,
    first_value(monthly_avg_rate) over (partition by currency_pair order by period_month) as first_rate,
    last_value(monthly_avg_rate)  over (partition by currency_pair order by period_month
                                        rows between unbounded preceding and unbounded following) as last_rate
  from ecb.mart_currency_strength
  where currency_pair in ('EUR/USD', 'EUR/GBP', 'EUR/JPY', 'EUR/CHF', 'EUR/PLN')
  qualify row_number() over (partition by currency_pair order by period_month desc) = 1
),
ranked as (
  select
    currency_pair,
    round(100 * (last_rate / first_rate - 1), 1) as pct_change_since_start
  from first_last
)
select
  (select currency_pair from ranked order by pct_change_since_start desc limit 1) as top_pair,
  (select pct_change_since_start from ranked order by pct_change_since_start desc limit 1) as top_pct,
  (select currency_pair from ranked order by pct_change_since_start asc limit 1) as bottom_pair,
  (select pct_change_since_start from ranked order by pct_change_since_start asc limit 1) as bottom_pct
```

**Reading this chart.** Every line starts at **100** in the earliest month of our data. A line at **120** means the euro is now **20% stronger** against that currency than at the start of the series; a line at **80** means **20% weaker**. This lets you compare currencies that have very different absolute prices (EUR/JPY ≈ 160 vs EUR/USD ≈ 1.10) on the same scale.

<DataTable data={indexed_summary} rows=5 />

The currency the euro has gained the most against over the full window is **{indexed_extremes[0].top_pair}** ({indexed_extremes[0].top_pct}%). The one it has gained the least (or lost) against is **{indexed_extremes[0].bottom_pair}** ({indexed_extremes[0].bottom_pct}%).


## Full monthly history

```sql fx_table
select
  period_month,
  currency_pair,
  monthly_avg_rate,
  mom_pct_change,
  yoy_pct_change
from ecb.mart_currency_strength
order by period_month desc, currency_pair
```

<DataTable data={fx_table} rows=20 search=true />

**Reading this table.** Sorted newest first. `mom_pct_change` = change from the previous month. `yoy_pct_change` = change from the same month one year ago. Use the column headers to sort — clicking `yoy_pct_change` desc gives you the months when the euro was strengthening fastest.

## Related

- [← Back to overview](/)
- [Inflation](/inflation) — the prices side of the same story
- [Monetary policy](/monetary-policy) — what the ECB did about it
- [Pipeline Health](/pipeline) — data freshness and sources
