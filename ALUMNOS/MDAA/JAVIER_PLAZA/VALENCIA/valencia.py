import requests 
import psycopg

respuesta = requests.get("https://valencia.opendatasoft.com/api/records/1.0/search/?dataset=valenbisi-disponibilitat-valenbisi-dsiponibilidad")

respuesta = respuesta.json()

print(respuesta)

