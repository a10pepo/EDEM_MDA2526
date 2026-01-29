from flask import Flask, jsonify, request
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import os
import psycopg
from psycopg.rows import dict_row
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
            connection = psycopg.connect(bbdd_url, row_factory = dict_row) # row_factory, para que los datos extraidos se hagan en forma de diccionarios. 
            print("BD conectada con éxito")
            return connection
        except Exception as e :
            print(f"Error conectando a la BD (intento {i+1}/10): {e}")
            time.sleep(2)
    print("Error: No se pudo conectar a la BD después de 10 intentos")
    return None

# Función que verifica que el usuario que emplee la API, se sabe su propia contraseña.
@auth.verify_password
def verificar_contrasena(usuario, contrasena):
    connection = conexion_db()
    if connection is None:
        print("Error: No se pudo conectar a la base de datos en verificar_contrasena")
        return None
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
    if connection is None: 
        return jsonify({"mensaje": "No se pudo conectar a la base de datos."}), 500
    cur = connection.cursor()
    try: 
        # Se insertan el usuario y la contraseña en la base de datos.
        query = """INSERT INTO credenciales (usuario, contrasena) VALUES (%s, %s)"""
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
    except Exception as e:
        print(f"Error en registro de usuario: {e}")
        cur.close()
        connection.close()
        return jsonify({"mensaje": f"Error interno: {str(e)}"}), 500

# Devuelve un token para un usuario.
@app.route("/iniciar_sesion", methods = ["POST"])
@auth.login_required  # Verifica que el usuario y la contraseña introducidos son correctos.
def iniciar_sesion():
    usuario_actual = auth.current_user()
    token_acceso = create_access_token(identity = usuario_actual)
    return jsonify({"token_acceso": token_acceso}), 200

# Función POST, para poder hacer la ingestión de datos a la base de datos
@app.route("/insertar_alimentos", methods=["POST"])
@jwt_required()
def insertar_alimentos():
    datos = request.get_json()

    # El nombre del alimento es esencial, sin el no se puede saber a quien corresponde la información nutricional. Por eso se para si no se encuentra en los datos. 
    if not datos.get("nombre"):
        return jsonify({"mensaje": "Falta el nombre del alimento, siendo este esencial"}), 400
    connection = conexion_db()

    # Por si falla la conexión con la base de datos, se controla con el error 500.
    if not connection:
        return jsonify({"mensaje": "Error conectando a la BD"}), 500

    cur = connection.cursor()

    try:
        # Introducir los datos en la base de datos, con unos criterios predefinidos.
        query = """
            INSERT INTO alimentos (
                nombre, tipo, calorias, grasas, carbohidratos, azucar, proteina, publicado
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s
            )
            ON CONFLICT (nombre) DO NOTHING; 
        """
        cur.execute(query, (
            datos.get("nombre"),
            datos.get("tipo"), 
            datos.get("calorias"),      
            datos.get("grasas"),
            datos.get("carbohidratos"),
            datos.get("azucar"),
            datos.get("proteina"),
            False # Al introducirlos en la base de datos, 
        ))

        connection.commit()

        if cur.rowcount > 0:
            return jsonify({"mensaje": "Alimento insertado"}), 201
        else:
            return jsonify({"mensaje": "El alimento ya existía"}), 200
    
    # Se controla por si falla la API. 
    except Exception as e:
        connection.rollback() 
        print(f"Error en inserción: {e}") 
        return jsonify({"mensaje": f"Error interno: {str(e)}"}), 500
    finally:
        cur.close()
        connection.close()

# Funcion GET para poder obtener la información que queramos de la base de datos, para poder publicarla.
@app.route("/obtener_info_alimentos", methods = ["GET"])
@jwt_required()
def obtener_info_alimentos():
    connection = conexion_db()
    try:
        cur = connection.cursor()

        # Extracción de datos no publicados, de manera aleatoria. 
        query = """SELECT id, nombre, tipo, calorias, grasas, carbohidratos, azucar, proteina
                FROM alimentos
                WHERE publicado = FALSE
                ORDER BY RANDOM()
                LIMIT 1"""
        cur.execute(query)
        resultado = cur.fetchone()
        
        # Si se han extraido los datos correctamente, devuelve un JSON, y el valor 200.
        if resultado: 
            return jsonify(resultado), 200
        else:
            return jsonify({"mensaje": "No quedan alimentos por publicar"}), 404
    
    # Se controla por si falla la API
    except Exception as e:
        return jsonify({"mensaje": f"Error obteniendo la información de los alimentos: {str(e)}"}), 500
    finally:
        cur.close()
        connection.close()

# Función para cambiar la columna publicacion en la base de datos si se ha realizado una publicación.
@app.route("/confirmar_publicacion/<int:id_alimento>", methods=["PUT"])
@jwt_required()
def confirmar_publicacion(id_alimento):
    connection = conexion_db()
    try:
        cur = connection.cursor()
        query = "UPDATE alimentos SET publicado = TRUE WHERE id = %s"
        cur.execute(query, (id_alimento,))
        connection.commit()
        if cur.rowcount > 0:
            return jsonify({"mensaje": f"Alimento {id_alimento} marcado como publicado"}), 200
        else:
            return jsonify({"mensaje": "No se encontró el alimento con ese ID"}), 404
    except Exception as e:
        connection.rollback()
        return jsonify({"mensaje": f"Error actualizando estado: {str(e)}"}), 500
    finally:
        cur.close()
        connection.close()

# Manejo del error 405: Cuando el método (GET, POST) es incorrecto
@app.errorhandler(405)
def metodo_no_permitido(error):
    return jsonify({'error': 'Método no permitido. Revisa si debes usar GET o POST.'}), 405

if __name__ == '__main__':
    app.run(debug = True, host = "0.0.0.0")
