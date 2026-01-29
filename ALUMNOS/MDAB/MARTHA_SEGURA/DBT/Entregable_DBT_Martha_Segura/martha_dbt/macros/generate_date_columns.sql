{% macro generate_date_columns(date_field) %}
    {{ date_field }}                            as date,
    extract(year  from {{ date_field }})        as year,
    extract(month from {{ date_field }})        as month,
    extract(day   from {{ date_field }})        as day
{% endmacro %}
