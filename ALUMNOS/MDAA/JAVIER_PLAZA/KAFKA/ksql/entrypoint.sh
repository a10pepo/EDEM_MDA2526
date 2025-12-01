#!/bin/bash

echo "Esperando a que ksqlDB esté disponible..."

until curl -s http://ksql:8088/info >/dev/null; do
  echo "ksqlDB no responde todavía..."
  sleep 2
done

echo "ksqlDB listo, aplicando scripts SQL..."

curl -X POST "http://ksql:8088/ksql" \
  -H "content-type: application/vnd.ksql.v1+json; charset=utf-8" \
  -d @/scripts/crear_stream.json

curl -X POST "http://ksql:8088/ksql" \
  -H "content-type: application/vnd.ksql.v1+json; charset=utf-8" \
  -d @/scripts/crear_tabla.json

echo "Scripts aplicados correctamente."
