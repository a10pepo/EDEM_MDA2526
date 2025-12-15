from flask import Flask, jsonify, request
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import requests

url_frutas = "https://fruityvice.com/api/fruit/all"

# Llamada a la API con todas las frutas para poder sacar las frutas que existen.
respuesta_url_frutas = request(url_frutas)

respuesta_url_frutas = respuesta_url_frutas.json()

# Creación de la lista de las frutas y bucle para introducir las frutas en la lista.
frutas = []
for fruta in respuesta_url_frutas["name"]:
    frutas.append(fruta)

# Creación de la aplicación donde se encuentra la API
app = Flask(__name__)
auth = HTTPBasicAuth()

app.config['JWT_SECRET_KEY'] = 'your_secret_jwt_key'
jwt = JWTManager(app)