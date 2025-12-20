from dotenv import load_dotenv
import os
import tweepy

# -----------------------------
# Cargar variables de entorno
# -----------------------------
load_dotenv()

API_KEY = os.getenv("X_API_KEY")
API_SECRET = os.getenv("X_API_SECRET")
ACCESS_TOKEN = os.getenv("X_ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("X_ACCESS_TOKEN_SECRET")
APP_MODE = os.getenv("APP_MODE", "production")

# -----------------------------
# Validar credenciales
# -----------------------------
if not all([API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET]):
    raise Exception("Faltan variables de entorno. Revisa tu archivo .env")

# -----------------------------
# Autenticación con X API v2
# -----------------------------
try:
    client = tweepy.Client(
        consumer_key=API_KEY,
        consumer_secret=API_SECRET,
        access_token=ACCESS_TOKEN,
        access_token_secret=ACCESS_TOKEN_SECRET
    )
    print("Autenticación correcta")
except Exception as e:
    print("Error de autenticación:", e)
    exit(1)

# -----------------------------
# Función para publicar post
# -----------------------------
def publicar_post(texto: str):
    texto = texto.strip()
    if len(texto) == 0:
        raise ValueError("El post no puede estar vacío")
    if len(texto) > 280:
        raise ValueError("El post no puede superar 280 caracteres")

    if APP_MODE.lower() == "development":
        print(f"[DEV MODE] Simulando post: {texto}")
    else:
        try:
            response = client.create_tweet(text=texto)
            print(f"Post publicado correctamente: {texto}")
            print("ID del post:", response.data['id'])
        except tweepy.TweepyException as e:
            print("Error al publicar el post:", e)

# -----------------------------
# Ejemplo de uso
# -----------------------------
if __name__ == "__main__":
    mensaje = input("Escribe el mensaje que quieres publicar en X: ")
    publicar_post(mensaje)
