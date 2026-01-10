import psycopg
from funciones import f_llamada_api

API_URL = "https://valencia.opendatasoft.com/api/explore/v2.1/catalog/datasets/valenbisi-disponibilitat-valenbisi-dsiponibilidad/records?limit=20"

response = f_llamada_api(API_URL,"valenbisi_api")

print(response)