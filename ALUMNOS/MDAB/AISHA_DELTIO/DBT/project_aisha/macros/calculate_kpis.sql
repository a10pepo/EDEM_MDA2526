{# Macro para determinar si es Podio (Top 3) #}
{% macro is_podium(position_column) %}
    case 
        when {{ position_column }} <= 3 then 1 
        else 0 
    end
{% endmacro %}

{# Macro para determinar si entró en Puntos (Top 10 en la era moderna) #}
{% macro is_in_points(position_column) %}
    case 
        when {{ position_column }} <= 10 then 1 
        else 0 
    end
{% endmacro %}

{# Macro para determinar si Ganó #}
{% macro is_victory(position_column) %}
    case 
        when {{ position_column }} = 1 then 1 
        else 0 
    end
{% endmacro %}