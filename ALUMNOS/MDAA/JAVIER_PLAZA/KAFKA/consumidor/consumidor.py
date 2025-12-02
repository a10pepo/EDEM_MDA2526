from confluent_kafka import Consumer
import json

# Configuración del consumidor y creación del mismo. 
config = {
    "bootstrap.servers": "kafka:29092",
    "group.id": "grupo_alertas",
    "auto.offset.reset": "earliest"
}
consumidor = Consumer(config)
consumidor.subscribe(["alertas"])

# Función para ejecutar la orden de compra o de venta en función del mensaje.
def ejecutar_orden(accion, alerta, precio, fecha):
    print(f"Se ha relizado la acción {alerta}, sobre {accion} el {fecha} con un coste de {precio}")

# Bucle para consumir los mensajes y realizar las compras o las ventas de los activos.
try:    
    while True: 
        mensaje = consumidor.poll(1.0)
        if mensaje is None:
            continue
        if mensaje.error():
            print(f"Error al recibir mensaje: {mensaje.error()}")
            continue
        try:
            payload = json.loads(mensaje.value().decode("utf-8"))
        except Exception as e:
            print("Erro decodificando el JSON:", e)
            print("Mensaje en bruto:", mensaje.value())
            continue
        accion = payload.get("accion")
        alerta = payload.get("alerta")
        precio = payload.get("precio")
        fecha = payload.get("fecha")
        print("Mensaje recibido:", payload)
        ejecutar_orden(accion, alerta, precio, fecha)
except KeyboardInterrupt:
    print("Programa detenido por el usuario")
finally: 
    consumidor.close()