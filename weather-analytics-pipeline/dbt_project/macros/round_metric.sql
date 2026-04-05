{% macro round_metric(value, decimals=1) %}
    round({{ value }}, {{ decimals}})
{% endmacro %}
