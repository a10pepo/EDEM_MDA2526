1. Definimos el caso de uso:

Imaginemos que una empresa de repartos (Glovo) tiene un topico de sus pedidos en donde recoge todos los pedidos que entregan sus repartidores. Si un pedido no ha podido ser entregado se marca como tal. En las oficinas ven que ese pedido no ha podido ser entregado y llaman al cliente. Si lo solucionan arreglado. Si no, se reprocesa ese pedido en otro hilo.

2. Ejemplos del dataset:

{
    "sensor_id": "S3",
    "value": 42.15,
    "temperature": 75.21,
    "humidity": 30.12,
    "status": "OK",
    "timestamp": 1707672661.4582,
    "uuid": "6f9e42e1-8d3b-4c7a-9f2d-1a2b3c4d5e6f"
}

{
    "sensor_id": "S3",
    "value": 42.15,
    "temperature": 82.02,
    "humidity": 30.12,
    "status": "FAIL",
    "timestamp": 1707672661.4582,
    "uuid": "6f9e42e1-8d3b-4c7a-9f2d-1a2b3c4d5e6f"
}
