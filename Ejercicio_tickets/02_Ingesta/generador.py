import random
import requests
from time import sleep

FLASK_API_URL = "http://backend:8000/ingestion"

#Generador tickets automáticos 
while True:

    tienda= ["Recambios Moratalla", "Tienda de Electrónica", "Supermercado El Ahorro", "Librería El Saber", "Ropa y Moda"]
    direcciones= ["Calle Falsa 123", "Avenida Siempre Viva 456", "Plaza Mayor 789", "Calle del Sol 321", "Avenida de la Luna 654"]
    fechas=["2024-06-01", "2024-06-02", "2024-06-03", "2024-06-04", "2024-06-05"]
    producto["Producto A", "Producto B", "Producto C", "Producto D", "Producto E"]

    aleatorio=random.randint(0, 4)

    ticket= {"ticket_id": random.randint(1, 1000),
        "timestamp": "2024-06-01 11:00:00",
        "adress": direcciones[aleatorio],
        "shop_name": tienda[aleatorio], 
        "product_name": producto_seleccionado,
        "import": round(random.uniform(10.0, 1000.0), 2),
        "refund_deadline": fechas[random.randint(0, 4)],
        "change_deadline": fechas[random.randint(0, 4)]
        }

    #Llamamos a la ruta del servidor para enviar el ticket
    try:
      response = requests.post(FLASK_API_URL, json={"ticket": ticket})
    except:
      print("Error al enviar el ticket. El servidor no está disponible.")

    #Esperamos 200 segundos hasta el nuevo ticket 
    sleep(20)