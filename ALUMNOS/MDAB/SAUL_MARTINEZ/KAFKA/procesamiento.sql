CREATE STREAM stream_clean_transactions (
    id VARCHAR,
    user VARCHAR,
    card VARCHAR,
    amount DOUBLE,
    status VARCHAR
) WITH (
    KAFKA_TOPIC='clean_transactions',
    VALUE_FORMAT='JSON'
);

CREATE STREAM stream_vip_sales WITH (
    KAFKA_TOPIC='vip_large_transactions',
    VALUE_FORMAT='JSON'
) AS
SELECT id, user, amount, card
FROM stream_clean_transactions
WHERE amount > 500;
