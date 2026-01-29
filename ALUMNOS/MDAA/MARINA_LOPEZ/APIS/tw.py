import tweepy
import os
from dotenv import load_dotenv  # Importamos esto para leer el .env


# 1. Cargar las variables del archivo .env
load_dotenv()


MOCK_MODE = False # Modo de simulación para pruebas sin enviar tweets reales 
#si dice True es la prueba y lo devuelve por terminal si dice False crea el tweet real


#2. leo las claves
api_key = os.getenv("X_API_KEY")
api_secret = os.getenv("X_API_SECRET")
access_token = os.getenv("X_ACCESS_TOKEN")
token_secret = os.getenv("X_ACCESS_TOKEN_SECRET")

#3. Autentificarse
client = tweepy.Client(
    consumer_key=api_key,
    consumer_secret=api_secret,
    access_token=access_token,
    access_token_secret=token_secret
)

#4. Escribir el tweet 
# a) incluyo condicional con MOCK_MODE para usar el modo prueba o no
# b) incluyo validación de longitud de caracteres del tweet para evitar errores
# c) incluyo confirmacion del usuario antes de enviar el tweet
# d) para comprobar que se twittea, pedimos que nos de el id del tweet
# e) bucle try-except para capturar errores y conocerlos

def postear():
    texto = "¡Hola mundo! twitteando usando la API de X 🚀"
    longitud = len(texto)
    
    try: 
        if 0 < longitud <= 280:

            confirmacion = input(f"Vas a publicar: '{texto}' ¿Estás seguro? (yes/no): ").lower()
            
            if confirmacion == "yes" or confirmacion == "y":

                if MOCK_MODE == True:
                    print(f"[HTTP 201 Created][MODO PRUEBA] Tweet simulado: '{texto}'")
                else:
                    response = client.create_tweet(text=texto)
                    print(f"[HTTP 201 Created] Tweet enviado a X con éxito! ID del tweet: {response.data['id']}")
            else:
                print("Operación cancelada por el usuario.")
        
        else: 
            print(f"❌ Error 400 (Bad Request]: El tweet no cumple con los requisitos de longitud. Tiene {longitud} caracteres (Máx 280).")

    except tweepy.errors.Forbidden as e:
            print(f"❌ Error 403 (Permisos): {e}")
            print("Revisa si tu App tiene permisos 'Read and Write' en el portal de desarrolladores.")
    except tweepy.errors.Unauthorized as e:
            print(f"❌ Error 401 (Credenciales): {e}")
            print("Revisa si tus claves en el archivo .env son correctas.")
    except Exception as e:
        print(f"Hubo un error: {e}")

def borrar():
    id_tweet = input("Pega aquí el ID del tweet a borrar: ")
    
    confirmacion = input(f"Vas a eliminar el tweet {id_tweet}. ¿Segura? (yes/no): ").lower()
    
    if confirmacion == "yes" or confirmacion == "y":
        try:
            if MOCK_MODE:
                print(f"[HTTP 200][MODO PRUEBA] Tweet {id_tweet} eliminado.")
            else:
                response = client.delete_tweet(id_tweet)
                if response.data['deleted'] == True:
                    print(f"[HTTP 200] Tweet eliminado correctamente.")
                else:
                  print("No se borró (el ID no existe)")
                
        except tweepy.errors.NotFound:
            print("❌ Error 404: No encuentro ese tweet (¿El ID es correcto?).")
        except Exception as e:
            print(f"❌ Error inesperado: {e}")
    else:
        print("Operación cancelada por el usuario.")

#4. menu para elegir si quiero crear tweet o borrar tweet
opcion = input("\n¿Qué quieres hacer? \n1. Crear tweet \n2. Borrar tweet \n👉 Elige:")
if opcion == "1":
   postear()
elif opcion == "2":
   borrar()