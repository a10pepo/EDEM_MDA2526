{% macro lbs_to_kg(column_name, decimal_places=1) %}
    round(cast({{ column_name }} as double) * 0.453592, {{ decimal_places }})
{% endmacro %}

{% macro inches_to_cm(column_name, decimal_places=0) %}
    round(cast({{ column_name }} as double) * 2.54, {{ decimal_places }})
{% endmacro %}