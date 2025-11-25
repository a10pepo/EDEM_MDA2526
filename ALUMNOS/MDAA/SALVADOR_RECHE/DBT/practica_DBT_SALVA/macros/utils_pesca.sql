{% macro get_raw_source(source_file) %}
    -- Construye la ruta relativa a la carpeta de la base de datos (../data/)
    -- y añade el prefijo 'raw__' y la extensión '.csv'
    './data/' || 'raw__' || {{ source_file }} || '.csv'
{% endmacro %}

-- Nota: Usaremos esta macro para leer los archivos en los modelos staging

{% macro calcular_beneficio_neto(cantidad, precio_venta, coste_compra) %}
    (
        -- Cálculo del INGRESO TOTAL REAL de la línea:
        ({{ cantidad }} * {{ precio_venta }})
        -
        -- Cálculo del COSTE TOTAL de la línea:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
        ({{ cantidad }} * {{ coste_compra }})
    )
{% endmacro %}