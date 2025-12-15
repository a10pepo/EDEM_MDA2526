from flask import Flask, jsonify, request
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import requests

url_frutas = "https://fruityvice.com/api/fruit/all"

# 
respuesta_url_frutas = request(url_frutas)

respuesta_url_frutas = respuesta_url_frutas.json()

frutas = []

for fruta in respuesta_url_frutas["name"]:
    frutas.append(fruta)

app = Flask(__name__)
auth = HTTPBasicAuth()

app.config['JWT_SECRET_KEY']