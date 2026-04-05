---
title: Weather Analytics Dashboard
---

# Weather Analytics Dashboard

Global weather data across 8 cities — 365 days of daily observations.

```sql kpis
select
    count(distinct city)                   as cities,
    count(*)                               as total_days,
    round(avg(temp_mean_celsius), 1)       as avg_temp,
    round(avg(humidity_pct), 1)            as avg_humidity,
    count(distinct climate_zone)           as climate_zones,
    round(avg(daylight_hours), 1)          as avg_daylight,
    round(max(temp_max_celsius), 1)        as hottest_temp,
    round(min(temp_min_celsius), 1)        as coldest_temp
from weather.fct_daily_weather
```

<BigValue data={kpis} value=cities        title="Cities Tracked" />
<BigValue data={kpis} value=total_days    title="Days of Data" />
<BigValue data={kpis} value=avg_temp      title="Global Avg Temp (°C)" />
<BigValue data={kpis} value=avg_humidity  title="Global Avg Humidity (%)" />
<BigValue data={kpis} value=climate_zones title="Climate Zones" />
<BigValue data={kpis} value=avg_daylight  title="Avg Daylight (hrs)" />
<BigValue data={kpis} value=hottest_temp  title="Hottest Recorded (°C)" />
<BigValue data={kpis} value=coldest_temp  title="Coldest Recorded (°C)" />


---

## Temperature Trends Over Time

```sql temp_trends
select date, city, temp_mean_celsius
from weather.fct_daily_weather
order by date
```

<LineChart
    data={temp_trends}
    x=date
    y=temp_mean_celsius
    series=city
    title="Mean Daily Temperature by City"
    yAxisTitle="°C"
/>

---

## City Overview

```sql city_summary
select
    city,
    continent,
    climate_zone,
    avg_temp_celsius,
    coldest_temp_celsius,
    hottest_temp_celsius,
    avg_humidity_pct / 100   as avg_humidity_pct,
    pct_rainy_days / 100     as pct_rainy_days,
    avg_wind_max_kmh
from weather.dim_cities
order by avg_temp_celsius desc
```

<DataTable data={city_summary} />

---

## Average Temperature by City

<BarChart data={city_summary} x=city y=avg_temp_celsius title="Average Temperature by City" yAxisTitle="°C" />

---

## Humidity & Rainy Days

<BarChart data={city_summary} x=city y=avg_humidity_pct title="Average Humidity by City" yAxisTitle="%" />

<BarChart data={city_summary} x=city y=pct_rainy_days title="% Rainy Days by City" yAxisTitle="%" />

---

## Seasonal Patterns

> **Note:** Seasonal patterns reflect temperate climates with 4 distinct seasons. Cities in tropical or arid climates experience little seasonal variation. Use the filter below to choose which cities to include.

```sql cities_list
select distinct city from weather.fct_daily_weather order by city
```

<Dropdown
    data={cities_list}
    name=city_filter
    value=city
    multiple=true
    title="Include Cities"
    defaultValue={["Berlin", "London", "New York", "Sydney", "Tokyo", "Cape Town"]}
/>

```sql seasonal
select
    season,
    round(avg(temp_mean_celsius), 1)  as avg_temp,
    round(avg(precipitation_mm), 2)   as avg_precip_mm
from weather.fct_daily_weather
where season is not null
  and season not in ('None', 'N/A', 'Unknown', '')
  and city in ${inputs.city_filter.value}
group by season
order by avg_temp desc
```

<BarChart data={seasonal} x=season y=avg_temp      title="Average Temperature by Season" yAxisTitle="°C" />
<BarChart data={seasonal} x=season y=avg_precip_mm title="Average Precipitation by Season" yAxisTitle="mm" />
