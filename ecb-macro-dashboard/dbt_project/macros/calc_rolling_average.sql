{% macro calc_rolling_average(column, partition_by, order_by, window_size) %}
    avg({{ column }}) over (
        partition by {{ partition_by }}
        order by {{ order_by }}
        rows between {{ window_size - 1 }} preceding and current row
    )
{% endmacro %}