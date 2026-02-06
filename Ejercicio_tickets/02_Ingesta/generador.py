import random
import requests
from time import sleep

FLASK_API_URL = "http://flask:5000/ingestion"

#Generador tickets automáticos 
while True:

    tiendas= ["Recambios Moratalla", "Tienda de Electrónica", "Supermercado El Ahorro", "Librería El Saber", "Ropa y Moda"]

    ticket= {"id": random.randint(1, 1000),
        "timestamp": "2024-06-01 11:00:00",
        "adress": "Calle Falsa 123",
        "nombre tienda": "Recambios Moratalla", 
        "importe": round(random.uniform(10.0, 100.0), 2),
        "refund deadline": "2024-06-01",
        "change deadline": "2024-06-01"
        }

    #Llamamos a la ruta del servidor para enviar el ticket
    response = requests.post(FLASK_API_URL, json={"ticket": ticket})
        
    #Esperamos 200 segundos hasta el nuevo ticket 
    sleep(200)