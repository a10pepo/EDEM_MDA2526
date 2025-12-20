import requests

url_frutas = "https://fruityvice.com/api/fruit/all"

respuesta_url_frutas = requests.get(url_frutas)

respuesta_url_frutas = respuesta_url_frutas.json()