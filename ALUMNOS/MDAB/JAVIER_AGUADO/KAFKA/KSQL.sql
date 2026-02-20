CREATE STREAM temperatura_Valencia_stream
    (ciudad VARCHAR)
    (temp_Valencia DOUBLE)
    WITH (KAFKA_TOPIC='temperatura_Valencia',
        VALUE_FORMAT='DELIMITED');
        


CREATE STREAM temperatura_Valencia_media_stream WITH (
    KAFKA_TOPIC='temperatura_Valencia_media',
    VALUE_FORMAT='DELIMITED'
) AS
SELECT temp_Valencia
FROM temperatura_Valencia_stream
EMIT CHANGES;

