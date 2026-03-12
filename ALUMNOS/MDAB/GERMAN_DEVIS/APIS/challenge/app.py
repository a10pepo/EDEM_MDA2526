import os
import tweepy
from flask import Flask, request, jsonify
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv

# 1. Cargar secretos del .env
load_dotenv()

app = Flask(__name__)
auth = HTTPBasicAuth()

# --- CONFIGURACIÓN USUARIOS ---
# El usuario es 'grman_admin' y la contraseña 'german123'
users = {
    "german_admin": generate_password_hash("german123")
}

# --- VERIFICACIÓN DE PASSWORD ---
@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users[username], password):
        return username
    return None

# --- CONEXIÓN CON TWITTER (X) ---
def get_twitter_client():
    """Conecta con X usando las llaves del .env"""
    api_key = os.getenv("X_API_KEY")
    api_secret = os.getenv("X_API_SECRET")
    access_token = os.getenv("X_ACCESS_TOKEN")
    access_secret = os.getenv("X_ACCESS_TOKEN_SECRET")

    # Verificamos que las claves existan
    if not all([api_key, api_secret, access_token, access_secret]):
        print("Error: Faltan credenciales en el archivo .env")
        return None

    # Autenticación OAuth 1.0a (Requerida para Free Tier v2)
    client = tweepy.Client(
        consumer_key=api_key,
        consumer_secret=api_secret,
        access_token=access_token,
        access_token_secret=access_secret
    )
    return client

# --- RUTA PARA PUBLICAR TWEET (POST) ---
@app.route('/tweet', methods=['POST'])
@auth.login_required  # <--- ¡Protegido con contraseña!
def create_tweet():
    # 1. Recibir datos del cuerpo JSON
    data = request.get_json()
    
    # 2. Validar que envíen texto
    if not data or 'content' not in data:
        return jsonify({"error": "Falta el campo 'content' en el JSON"}), 400
    
    tweet_text = data['content']

    # 3. Validar longitud (reglas de Twitter)
    if len(tweet_text) < 1 or len(tweet_text) > 280:
        return jsonify({"error": "El tweet debe tener entre 1 y 280 caracteres"}), 400

    # 4. Conectar y Publicar
    client = get_twitter_client()
    if not client:
        return jsonify({"error": "Error de configuración en el servidor"}), 500

    try:
        # ¡Aquí ocurre la magia!
        response = client.create_tweet(text=tweet_text)
        
        # Devolvemos éxito con el ID del tweet
        return jsonify({
            "message": "¡Tweet publicado con éxito!",
            "id": response.data['id'],
            "text": tweet_text
        }), 201

    except tweepy.TooManyRequests:
        return jsonify({"error": "Límite de tweets excedido (429)"}), 429
    except Exception as e:
        return jsonify({"error": f"Error al publicar en X: {str(e)}"}), 500

# --- ARRANQUE ---
if __name__ == '__main__':
    print("---  Servidor Listo en http://127.0.0.1:5000 ---")
    app.run(debug=True, port=5000)