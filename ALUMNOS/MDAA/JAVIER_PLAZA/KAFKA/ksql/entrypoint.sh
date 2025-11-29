#!/bin/bash

echo "Esperando a que ksqlDB esté disponible..."

until curl -s http://ksqldb-server:8088/info >/dev/null; do
  echo "ksqlDB no responde todavía..."
  sleep 2
done

echo "✔ ksqlDB listo, aplicando scripts SQL..."

curl -X "POST" "http://ksqldb-server:8088/ksql" \
     -H "content-type: application/vnd.ksql.v1+json; charset=utf-8" \
     -d "{\"ksql\": \"RUN SCRIPT '/scripts/create_streams.sql';\"}"

curl -X "POST" "http://ksqldb-server:8088/ksql" \
     -H "content-type: application/vnd.ksql.v1+json; charset=utf-8" \
     -d "{\"ksql\": \"RUN SCRIPT '/scripts/transformations.sql';\"}"

echo "Scripts aplicados correctamente."
