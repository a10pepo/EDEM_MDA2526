import requests 
import psycopg

respuesta = requests.get("https://valencia.opendatasoft.com/api/explore/v2.1/catalog/datasets/valenbisi-disponibilitat-valenbisi-dsiponibilidad/records?limit=20")

respuesta = respuesta.json()

resultados = []
for resultado in respuesta["results"]:
    print(resultado)




