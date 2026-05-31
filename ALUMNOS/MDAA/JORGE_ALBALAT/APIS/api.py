import requests
import tweepy
import os

X_API_KEY = os.getenv("X_API_KEY")
X_API_SECRET = os.getenv("X_API_SECRET")
X_ACCESS_TOKEN = os.getenv("X_ACCESS_TOKEN")
X_ACCESS_TOKEN_SECRET = os.getenv("X_ACCESS_TOKEN_SECRET")

NBA_API_URL = "http://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard"

def ejecutar_bot():
    print("🏀 Obteniendo datos de la NBA...")
    
    try:
        response = requests.get(NBA_API_URL)
        if response.status_code != 200:
            print(f"Error conectando a ESPN: {response.status_code}")
            return

        data = response.json()
        eventos = data.get("events", [])

        if not eventos:
            print("No hay partidos disponibles.")
            return
        
        partido = eventos[0]
        equipo1 = partido['competitions'][0]['competitors'][0]
        equipo2 = partido['competitions'][0]['competitors'][1]

        nombre1 = equipo1['team']['displayName']
        puntos1 = equipo1.get('score', '0')
        nombre2 = equipo2['team']['displayName']
        puntos2 = equipo2.get('score', '0')
        estado = partido['status']['type']['detail']

        texto_tweet = (
            f"🏀 NBA:\n"
            f"{nombre1} ({puntos1}) vs ({puntos2}) {nombre2}\n"
            f"Estado: {estado}\n"
        )
        
        print(f"Texto preparado:\n{texto_tweet}")

        
        try:
            client = tweepy.Client(
                consumer_key=X_API_KEY,
                consumer_secret=X_API_SECRET,
                access_token=X_ACCESS_TOKEN,
                access_token_secret=X_ACCESS_TOKEN_SECRET
            )
            resp = client.create_tweet(text=texto_tweet)
            print(f"TWEET ENVIADO CON ÉXITO. ID: {resp.data['id']}")
        except Exception as e:
            print(f"ERROR AL PUBLICAR EN TWITTER: {e}")

    except Exception as e:
        print(f"Error general: {str(e)}")

if __name__ == '__main__':
    ejecutar_bot()