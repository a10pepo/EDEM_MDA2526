import os
from flask import Flask, request, jsonify
import tweepy
from dotenv import load_dotenv
from scraper import obtener_resumen_rfetm

load_dotenv()

app = Flask(__name__)

# Configuración de credenciales desde variables de entorno
client = tweepy.Client(
    consumer_key=os.getenv("TWITTER_API_KEY"),
    consumer_secret=os.getenv("TWITTER_API_SECRET"),
    access_token=os.getenv("TWITTER_ACCESS_TOKEN"),
    access_token_secret=os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
)

@app.route('/post_tweet', methods=['POST'])
def post_tweet():
    data = request.get_json()
    text = data.get('text')
    
    if not text:
        return jsonify({"error": "No se proporcionó texto"}), 400
    
    try:
        response = client.create_tweet(text=text)
        return jsonify({
            "message": "Tweet publicado con éxito",
            "tweet_id": response.data['id']
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@app.route('/tweet_resultados', methods=['POST'])
def tweet_resultados():
    try:
        # 1. Obtenemos el texto directamente de la web
        texto_resumen = obtener_resumen_rfetm()
        
        # 2. (Opcional) Pasamos ese texto por OpenAI para darle "vidilla"
        # completion = client_ai.chat.completions.create(...)
        
        # 3. Publicamos el tweet
        response = client.create_tweet(text=texto_resumen)
        
        return jsonify({
            "mensaje": "Resumen publicado",
            "tweet_text": texto_resumen,
            "id": response.data['id']
        }), 201
    except Exception as e:
        # 1. Imprimes el error real para ti
        print(f"❌ ERROR obteniendo resultados: {e}")
        
        # 2. Al usuario mensaje genérico
        return jsonify({"error": "Error interno del servidor"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)