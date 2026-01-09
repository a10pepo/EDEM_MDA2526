/*
    TEST SINGULAR: Este test falla si alguna categoría (Eging, Spinning, etc.)
    en el Mart final ha acumulado un beneficio total negativo.
*/

select
    categoria,
    sum(beneficio_total) as total_beneficio_acumulado
from {{ ref('fct__rendimiento_productos') }} -- Usamos el Mart de rendimiento
group by 1
having sum(beneficio_total) < 0