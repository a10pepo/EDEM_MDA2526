WITH source AS (
    -- 1. Leemos de la tabla raw.tickets que define tu código Python
    SELECT * FROM {{ source('raw', 'tickets') }}
),

renamed_and_categorized AS (
    SELECT
        -- Identificadores y Tiempo
        ticket_id,
        timestamp,
        
        -- Datos de la Tienda (Limpieza de nombres)
        shop_name,
        adress AS address,          -- Corregimos el typo 'adress' del Python
        latitud AS latitude,        -- Estandarizamos a inglés
        longitud AS longitude,      -- Estandarizamos a inglés
        
        -- Datos Económicos
        "import" AS amount,         -- IMPORTANTE: "import" entre comillas y renombramos
        
        -- Datos del Producto
        product_name,

        -- LÓGICA DE NEGOCIO (Categorización)
        CASE 
            WHEN product_name IN ('Producto A', 'Producto B') THEN 'Tecnología'
            WHEN product_name = 'Producto C' THEN 'Alimentación'
            WHEN product_name = 'Producto D' THEN 'Ocio'
            WHEN product_name = 'Producto E' THEN 'Ropa'
            ELSE 'Sin Categoría'
        END AS category,

        -- Fechas límite
        refund_deadline,
        change_deadline

    FROM source
)

SELECT * FROM renamed_and_categorized