WITH source AS (
    SELECT * FROM {{ source('raw', 'tickets') }}
),

renamed_and_categorized AS (
    SELECT
        -- 1. Mapeo de columnas (Origen -> Destino)
        id_ticket AS ticket_id,
        purchase_date AS timestamp,
        shop AS shop_name,
        price AS amount,
        
        -- Traemos la columna tal cual la definen en backend
        product_name,

        -- 2. Lógica de Categorización (Usando el nuevo nombre)
        CASE 
            WHEN product_name IN ('Producto A', 'Producto B') THEN 'Tecnología'
            WHEN product_name = 'Producto C' THEN 'Alimentación'
            WHEN product_name = 'Producto D' THEN 'Ocio'
            WHEN product_name = 'Producto E' THEN 'Ropa'
            ELSE 'Sin Categoría'
        END AS category

    FROM source
)

SELECT * FROM renamed_and_categorized