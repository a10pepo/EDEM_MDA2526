{% macro clean_citations(column_name) %}
    TRIM(
        REGEXP_REPLACE(
            {{ column_name }}, 
        '\[.*\]', '', 'g')
    )
{% endmacro %}