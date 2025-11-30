Esta aplicación simula un entorno en el que múltiples sensores repartidos por una casa envian información a un hub domótico central, que la procesa, y define acciones a implementar. Estas acciones son después enviadas a controladores (Consumers) dependiendo del tipo de habitación (interior o exterior) que se encarga de implementar cada acción (encender luces, radidores, etc).
En caso de requerir acciones no ejecutables por el controlador inteligente (cerrar ventanas), el usuario recibirá la notificación de la acción requerida a través de un Stream.

Información enviada por el producer (producer_eventos.py) al topic 'eventos_domoticos' en formato json:

    evento_data = {
        "habitacion_id": 2,
        "habitacion_nombre": "dormitorio",
        "tipo_habitacion": "interior",
        "evento": "baja_temperatura",
        "timestamp": 2025-12-01 19:55:06
    }

El script hub_domotico_alertas.py actua como consumer al recibir los datos del topic 'eventos_domoticos', transforma la informacion añadiendo la acción requerida al json, y envia estos datos a dos topics dependiendo si la habitación del evento es interior (eventos_interior) o exterior (eventos_exterior). 
Ejemplo de JSON mandado por el Hub a los Consumidores finales:

    msg = {
        "habitacion_id": 2,
        "habitacion_nombre": "dormitorio",
        "tipo_habitacion": "interior",
        "evento": "baja_temperatura",
        "timestamp": 2025-12-01 19:55:06
        "accion": "encender_radiador"
    }




