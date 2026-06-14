{% macro ensure_dataset_exists(dataset_name) %}
  {% set sql %}
    CREATE SCHEMA IF NOT EXISTS `{{ target.project }}.{{ dataset_name }}` OPTIONS(location='{{ target.location }}');
  {% endset %}
  {% do run_query(sql) %}
{% endmacro %}