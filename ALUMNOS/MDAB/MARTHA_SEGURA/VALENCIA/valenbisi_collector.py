import time
from datetime import datetime
import requests

API_URL = (
    "https://valencia.opendatasoft.com/api/explore/v2.1/catalog/datasets/"
    "valenbisi-disponibilitat-valenbisi-dsiponibilidad/records?limit=200"
)

POLL_SECONDS = 300  # 5 minutos


while True:
    timestamp = datetime.now()

    response = requests.get(API_URL)
    data = response.json()

    # 👇 AQUÍ está la corrección clave
    stations = data.get("results", [])

    for station in stations:
        station_id = station["number"]
        station_name = station["address"]
        latitude = station["geo_point_2d"]["lat"]
        longitude = station["geo_point_2d"]["lon"]
        available_bikes = station["available"]
        available_slots = station["free"]
        station_status = station["open"]

        print(
            station_id,
            station_name,
            latitude,
            longitude,
            available_bikes,
            available_slots,
            station_status,
            timestamp
        )

    time.sleep(POLL_SECONDS)

