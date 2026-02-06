import random
import requests
from time import sleep

FLASK_API_URL = "http://flask:5000/ingestion"

#Generador tickets automáticos 
while True:

    tiendas= ["Recambios Moratalla", "Tienda de Electrónica", "Supermercado El Ahorro", "Librería El Saber", "Ropa y Moda"]
    direcciones= ["Calle Falsa 123", "Avenida Siempre Viva 456", "Plaza Mayor 789", "Calle del Sol 321", "Avenida de la Luna 654"]
    fechas=["2024-06-01", "2024-06-02", "2024-06-03", "2024-06-04", "2024-06-05"]

    aleatorio=random.randint(0, 4)

    ticket= {"id": random.randint(1, 1000),
        "timestamp": "2024-06-01 11:00:00",
        "adress": direcciones(aleatorio),
        "nombre tienda": tienda(aleatorio), 
        "importe": round(random.uniform(10.0, 1000.0), 2),
        "refund deadline": fechas(random.randint(0, 4)),
        "change deadline": fechas(random.randint(0, 4))
        }

    #Llamamos a la ruta del servidor para enviar el ticket
    response = requests.post(FLASK_API_URL, json={"ticket": ticket})
        
    #Esperamos 200 segundos hasta el nuevo ticket 
    sleep(200)