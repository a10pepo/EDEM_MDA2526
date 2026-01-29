{% macro get_race_outcome(status_column) %}
    case
        -- Terminó la carrera (o fue doblado pero clasificó)
        when {{ status_column }} like 'Finished' then 'Finished'
        when {{ status_column }} like '+%' then 'Finished' 
        
        -- Fallos del coche (Mecánicos/Fiabilidad) 
        when {{ status_column }} like '%Engine%' then 'Mechanical Failure'
        when {{ status_column }} like '%Gearbox%' then 'Mechanical Failure'
        when {{ status_column }} like '%Transmission%' then 'Mechanical Failure'
        when {{ status_column }} like '%Clutch%' then 'Mechanical Failure'
        when {{ status_column }} like '%Hydraulics%' then 'Mechanical Failure'
        when {{ status_column }} like '%Electrical%' then 'Mechanical Failure'
        when {{ status_column }} like '%Brake%' then 'Mechanical Failure'
        when {{ status_column }} like '%Overheating%' then 'Mechanical Failure'
        
        -- Errores del piloto o incidentes de carrera
        when {{ status_column }} like '%Collision%' then 'Accident'
        when {{ status_column }} like '%Accident%' then 'Accident'
        when {{ status_column }} like '%Spun%' then 'Driver Error'
        
        -- Otros (Descalificado, No salió, etc.)
        when {{ status_column }} like '%Disqualified%' then 'DSQ'
        else 'Other DNF'
    end
{% endmacro %}