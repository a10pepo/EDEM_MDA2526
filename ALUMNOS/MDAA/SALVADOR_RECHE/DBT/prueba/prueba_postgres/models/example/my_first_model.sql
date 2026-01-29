/*
    Este es un modelo de ejemplo para verificar la conexión con PostgreSQL.
    Puedes ejecutarlo con: dbt run --models my_first_model
*/

-- Modelo simple que selecciona una consulta básica
select
    1 as id,
    'Hola desde PostgreSQL' as mensaje,
    current_timestamp as fecha_creacion

