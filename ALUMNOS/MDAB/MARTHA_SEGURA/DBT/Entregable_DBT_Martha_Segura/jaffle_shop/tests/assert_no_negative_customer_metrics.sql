-- Test para validar que no hay métricas negativas en los clientes
-- Todas las métricas financieras y de conteo deben ser >= 0

select
    customer_id
from {{ ref('marts__customers') }}
where
    lifetime_value < 0
    