import json
import requests as requests
import psycopg2 #Revisar apuntes python, conector a postgres
import time as time
from datetime import datetime

#Definimos y abrimos la conexión a la base de datos (Postgres SQL)
psycopg2.connect(
        host="db",             
        port=5432,
        database="valenbisi",
        user="postgres",
        password="postgres"
    )
conn = get_db_connection()
cursor = conn.cursor()

#Creamos una función que acondiciones los datos devueltos por la API
def estructurador(dataset_api_valenbisi):
    return {"timestamp": datetime.now(),
    "station_name": dataset_api_valenbisi["address"], 
    "station_id": dataset_api_valenbisi["number"],
    "data":{
        "available_bikes": dataset_api_valenbisi["available"],
        "available_slots": dataset_api_valenbisi["free"],
        "station_status": dataset_api_valenbisi["open"],
        "total_capacity": dataset_api_valenbisi["total"],
        }}

#Lista de resultados para almacenar respuestas de la api
resultados=[]

#Este código continuamente y cada 5 min recoge datos de la api de valenbisi y las guarda en una base de datos
while True:
    
    #Buscamos los datos de la API de Valenbisi, cuidado con la paginación, límite de 20 registros
    offset=20
    limit=20
    url=f"https://valencia.opendatasoft.com/api/explore/v2.1/catalog/datasets/valenbisi-disponibilitat-valenbisi-dsiponibilidad/records?limit={limit}&offset={offset}"

    while True:
        
        response = requests.get(url)
        data = response.json()

        #En caso de no encontrar más registros hemos terminado de consumir la api
        if not data["results"]:
            break

        for registros in data["results"]:
            resultados.append(estructurador(registros))
        offset += 20
        url=f"https://valencia.opendatasoft.com/api/explore/v2.1/catalog/datasets/valenbisi-disponibilitat-valenbisi-dsiponibilidad/records?limit={limit}&offset={offset}"

    #Guardamos los datos de la API en la bbdd





    #Paramos el código 5 minutos 
    time.sleep(300)
