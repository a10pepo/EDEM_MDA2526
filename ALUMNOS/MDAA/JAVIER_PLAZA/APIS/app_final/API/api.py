from flask import Flask, jsonify, request
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import requests
import os
import psycopg
import time

# Creación de la aplicación donde se encontrará la API.
app = Flask(__name__)
auth = HTTPBasicAuth()

# Configuración de una clave de seguridad para el uso de la API. Sin la clave del .env no se podría emplear la API.
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
jwt = JWTManager(app)

# Función para realizar una conexión con la base de datos cuando se quiera. 
def conexion_db():
    # Se pone un bucle de 10 intentos con un tiempo de 2 segundos por cada intento por si falla la conexión. 
    for i in range(10):
        try: 
            bbdd_url = os.getenv("DATABASE_URL")
            connection = psycopg.connect(bbdd_url)
            print("BD conectada con éxito")
            return connection
        except Exception as e :
            print("Error conectando a la BD:", e)
            time.sleep(2)

# Función que verifica que el usuario que emplee la API, se sabe su propia contraseña.
@auth.verify_password
def verificar_contrasena(usuario, contrasena):
    connection = conexion_db()
    query = """SELECT contrasena FROM credenciales WHERE usuario = %s"""
    cur = connection.cursor()
    cur.execute(query, (usuario,))
    resultado = cur.fetchone()
    cur.close()
    connection.close()
    if resultado and check_password_hash(resultado["contrasena"], contrasena):
        return usuario
    return None

# En la ruta /registrar_usuarios se crea una función POST, por la cual se puede crear un usuario con su contraseña.
@app.route("/registrar_usuarios", methods = ["POST"])
def resgistrar_usuarios():
    datos = request.get_json()  # Los datos se deben de enviar en formato JSON
    usuario = datos.get("usuario")
    contrasena = datos.get("contrasena")
    if not usuario or not contrasena: 
        return jsonify({"mensaje": "Se necesita usuario y contraseña."}), 400
    connection = conexion_db()
    cur = connection.cursor()
    try: 
        # Se insertan el usuario y la contraseña en la base de datos.
        query = """INSERT INTO usuarios (usuario, contrasena) VALUES (%s, %s)"""
        cur.execute(query, (usuario, generate_password_hash(contrasena)))
        connection.commit()
        cur.close()
        connection.close()
        # Si no ocurre ningún error, se crea el usuario y devuelve el valor 201.
        return jsonify({"mensaje": "Usuario creado correctamente"}), 201
    # Si el usuario ya se ha introducido salta un error, para evitar duplicados.
    except psycopg.errors.UniqueViolation:
        cur.close()
        connection.close()
        return jsonify({"mensaje": "El usuario ya existe"}), 400

# Devuelve un token para un usuario.
@app.route("/iniciar_sesion", methods = ["POST"])
@auth.login_required  # Verifica que el usuario y la contraseña introducidos son correctos.
def iniciar_sesion():
    usuario_actual = auth.current_user()
    token_acceso = create_access_token(identity = usuario_actual)
    return jsonify({"token_acceso": token_acceso}), 200







