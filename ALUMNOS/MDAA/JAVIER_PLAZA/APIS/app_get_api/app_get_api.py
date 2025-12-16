from flask import Flask, jsonify, request
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import requests
import os
import random 

url_frutas = "https://fruityvice.com/api/fruit/all"

# Llamada a la API con todas las frutas para poder sacar las frutas que existen.
respuesta_url_frutas = request(url_frutas)

respuesta_url_frutas = respuesta_url_frutas.json()

# Creación de la lista de fruityvice y bucle para introducir las frutas en la lista.
frutas = []
for fruta in respuesta_url_frutas["name"]:
    frutas.append(fruta)

# Selección de una fruta para que aparezca la información nutricional de una única fruta.
fruta = random.choice(frutas)

# Creación de la aplicación donde se encuentra la API.
app = Flask(__name__)
auth = HTTPBasicAuth()

# Configuración de una clave de seguridad para el uso de la API. Sin la clave del .env no se podría emplear la API.
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
jwt = JWTManager(app)

# Diccionario para poder guardar los datos de los usuarios creados la API.
usuarios = {}

# Función que verifica que el usuario que emplee la API, se sabe su propia contraseña.
@auth.verify_password
def verificar_contraseña(usuario, contraseña):
    if usuario in usuarios and check_password_hash(usuarios.get(usuario)["contraseña"], contraseña):
        return usuario
    return None

# En la ruta /usuarios se crea una función POST, por la cual se puede crear un usuario con su contraseña. 
@app.route("/usuarios", methods = ["POST"])
def registrar_usuarios():
    datos = request.get_json()  # Los datos que se envien en el POST tienen que estar en formato JSON.
    usuario = datos.get("usuario")
    contraseña = datos.get("contraseña")

    # En el caso de que no introduzca el usuario contraseña o usuario. O si el usuario ya está creado, saltará el error 400. 
    if not usuario or not contraseña: 
        return jsonify({"mensaje": "Se necesita usuario y contraseña."}), 400
    if usuario in usuarios: 
        return jsonify({"mensaje": "El usuario ya existe."}), 400
    
    # La contraseña que introduzca el usuario se guardará encriptada.
    usuarios[usuario] = {
        "contraseña": generate_password_hash(contraseña)
    }

    # Si se crea correctame el usuario, devuelve el 201.
    return jsonify({"mensaje": "Usuario creado correctamente"}), 201



