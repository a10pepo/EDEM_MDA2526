WITH source AS (
    -- Seleccionamos la tabla de origen (raw)
    SELECT * FROM {{ source('public', 'raw_tickets') }}
),

renamed_and_categorized AS (
    SELECT
        -- 1. Identificadores y Fechas
        ticket_id,
        timestamp,
        
        -- 2. Limpieza de columnas (renombramos para corregir typos del Python)
        adress AS address,  -- Corregimos 'adress'
        shop_name,
        
        -- Renombramos 'import' a 'amount' o 'total' para evitar errores de SQL
        "import" AS amount, 
        
        -- Asumimos que la nueva columna que meten 'los de ingesta' se llama 'product'
        product,

        -- 3. Fechas límite
        refund_deadline,
        change_deadline,

        -- 4. Lógica de Categorización (La "movida" nueva)
        CASE 
            -- A y B -> Tecnología (Recambios y Electrónica)
            WHEN product IN ('Producto A', 'Producto B') THEN 'Tecnología'
            
            -- C -> Alimentación (Supermercado)
            WHEN product = 'Producto C' THEN 'Alimentación'
            
            -- D -> Ocio (Librería)
            WHEN product = 'Producto D' THEN 'Ocio'
            
            -- E -> Ropa (Ropa y Moda)
            WHEN product = 'Producto E' THEN 'Ropa'
            
            ELSE 'Sin Categoría'
        END AS category

    FROM source
)

SELECT * FROM renamed_and_categorized