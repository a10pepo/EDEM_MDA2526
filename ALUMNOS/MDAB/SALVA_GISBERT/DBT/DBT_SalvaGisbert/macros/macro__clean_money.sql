{% macro clean_money(column_name) %}
    TRY_CAST(
        replace(
            replace(
                {{ column_name }}, 
            '$', ''), 
        ',', '') 
    AS DOUBLE)
{% endmacro %}