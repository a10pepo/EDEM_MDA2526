import os, psycopg, requests, unicodedata, time

#URL CONEXIÓN A BD 
url = os.getenv("DATABASE_URL")
#CONEXIÓN A BD
connection = psycopg.connect(url)
# Cursor
cur = connection.cursor()
print("BD conectada con éxito")

def insertar(idEstacion , nombreEstacion , latitud , longitud , nBicicletasDisponibles , nEspaciosLibres, estado, totalCapacidad):
    try:
        query = """INSERT INTO valenbisi_raw(station_id , station_name , latitude , longitude , available_bikes , available_slots , station_status , total_capacity, timestamp)
        VALUES(%s , %s , %s , %s, %s , %s , %s , %s , NOW())
        """
        values = (idEstacion , nombreEstacion , latitud , longitud , nBicicletasDisponibles , nEspaciosLibres, estado, totalCapacidad)
        cur.execute(query , values)
    except Exception as e:
        print(e)

    connection.commit()



response = requests.get("https://valencia.opendatasoft.com/api/explore/v2.1/catalog/datasets/valenbisi-disponibilitat-valenbisi-dsiponibilidad/records?limit=3")
data = response.json()

x = [0, 1, 2]

for aux in x:
    idEstacion = data["results"][aux]["number"]
    nombreEstacion = data["results"][aux]["address"]
    latitud = data["results"][aux]["geo_shape"]["geometry"]["coordinates"][0]
    longitud = data["results"][0]["geo_shape"]["geometry"]["coordinates"][1]
    nBicicletasDisponibles = data["results"][aux]["available"]
    nEspaciosLibres = data["results"][aux]["free"]
    estado = data["results"][aux]["open"]
    totalCapacidad = data["results"][aux]["total"]

    insertar(idEstacion , nombreEstacion , latitud , longitud , nBicicletasDisponibles , nEspaciosLibres, estado, totalCapacidad)



# print(idEstacion)
# print(nombreEstacion) 
# print(coordenadas)
# print(nBicicletasDisponibles)
# print(nEspaciosLibres)
# print(estado)


