select
    product_id,
    category,
    sub_category,
    coalesce(description_en, description_es, description_fr, description_de, description_pt, description_zh) as description,
    color,
    sizes,
    production_cost,
    suggested_price,
    is_low_cost
from {{ ref('int_product_financials') }}
