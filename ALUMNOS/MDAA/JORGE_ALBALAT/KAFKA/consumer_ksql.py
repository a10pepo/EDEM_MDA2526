import requests
import time

KSQL_URL = "http://localhost:8088/ksql"

def ejecutar_ksql(nombre, sql):
    headers = {"Content-Type": "application/vnd.ksql.v1+json; charset=utf-8"}
    data = {"ksql": sql, "streamsProperties": {"ksql.streams.auto.offset.reset": "latest"}}
    try:
        r = requests.post(KSQL_URL, json=data, headers=headers)
        if r.status_code == 200: print(f"{nombre}: OK")
        else: print(f"{nombre}: {r.json().get('message')}")
    except Exception as e: print(f"Error: {e}")

sql_entrada = """
CREATE STREAM IF NOT EXISTS stream_pedidos (
    id VARCHAR, 
    cliente VARCHAR, 
    restaurante VARCHAR, 
    tiempo VARCHAR
) WITH (
    KAFKA_TOPIC='pedidos_tiempo', 
    VALUE_FORMAT='JSON'
);
"""

sql_filtro = """
CREATE STREAM IF NOT EXISTS pedidos_lentos AS
    SELECT id, cliente, restaurante, tiempo
    FROM stream_pedidos 
    WHERE CAST(tiempo AS INT) > 45;
"""

if __name__ == "__main__":
    ejecutar_ksql("Creando Stream Base (Tus campos)", sql_entrada)
    time.sleep(2)
    ejecutar_ksql("Creando Filtro Lentos (> 45 min)", sql_filtro)