

with __dbt__cte__base_raw_events_delivery as (


SELECT
publish_time,
data,
message_id
FROM `e2e-gcp-almacenamiento`.`delivery_bronze`.`raw_events_delivery`
) SELECT
publish_time,
message_id,
CAST(JSON_VALUE(data, '$.delivery_status') AS STRING) AS delivery_status,
CAST(JSON_VALUE(data, '$.event_at') AS TIMESTAMP) AS event_at,
CAST(JSON_VALUE(data, '$.order_id') AS INT64) AS order_id
FROM __dbt__cte__base_raw_events_delivery