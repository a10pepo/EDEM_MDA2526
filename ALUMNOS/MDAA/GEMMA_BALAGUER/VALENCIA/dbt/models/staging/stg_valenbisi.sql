
SELECT
    address,
    number,
    CASE WHEN open = 'true' THEN TRUE
         WHEN open = 'false' THEN FALSE
         ELSE NULL END AS open,
    available,
    free,
    total,
    ticket,
    CASE WHEN updated_at ~ '^\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2}$'
         THEN TO_TIMESTAMP(updated_at, 'DD/MM/YYYY HH24:MI:SS')
         ELSE NULL END AS updated_at,
    lon::numeric AS lon,
    lat::numeric AS lat,
    CASE WHEN update_jcd ~ '^\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2}$'
         THEN TO_TIMESTAMP(update_jcd, 'DD/MM/YYYY HH24:MI:SS')
         ELSE NULL END AS update_jcd
FROM {{ source('valenbisi_source', 'valenbisi') }}
