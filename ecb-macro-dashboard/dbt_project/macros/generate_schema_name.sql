{#
    generate_schema_name — override dbt's default schema naming.

    By default, dbt prefixes custom schemas with the target schema name:
        target.schema = "main", custom_schema_name = "staging"
        → "main_staging"

    We want just the custom name:
        custom_schema_name = "staging" → "staging"

    This is the standard override from the dbt docs and matches the
    weather pipeline's setup. Without it, every schema gets the "main_"
    prefix and the database feels cluttered.
#}

{% macro generate_schema_name(custom_schema_name, node) -%}
    {%- if custom_schema_name is none -%}
        {{ target.schema }}
    {%- else -%}
        {{ custom_schema_name | trim }}
    {%- endif -%}
{%- endmacro %}