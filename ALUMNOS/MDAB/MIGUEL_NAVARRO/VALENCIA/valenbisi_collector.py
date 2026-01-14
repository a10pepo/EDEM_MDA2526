import requests, time, psycopg, os

# URL CONECTION TO DB
DATABASE_URL = os.getenv("DATABASE_URL")    # takes url from .env
# CONECTION TO DB
while True:
    try:
        connection = psycopg.connect(DATABASE_URL)
        print("DB successfully connected")
        break
    except psycopg.OperationalError:
        print("DB is connecting... Wait 2 seconds")
        time.sleep(2) # Try again in 2 seconds
# Cursor
cur = connection.cursor()


url = "https://valencia.opendatasoft.com/api/explore/v2.1/catalog/datasets/valenbisi-disponibilitat-valenbisi-dsiponibilidad/records?limit=20"

response = requests.get(url)
data = response.json()

print(data["results"][0])

