import requests
import os
import time
import tweepy

# Tiempo de espera para que la API esté completamente operativa y haya datos disponibles
time.sleep(90)

url_base_api = "http://api:5000"

# Credenciales para autenticarse con la API
usuario = os.getenv("USUARIO_API_POST")
contrasena = os.getenv("CONTRASENA_API_POST")

# Credenciales de la API de X/Twitter
x_api_key = os.getenv("X_API_KEY")
x_api_secret = os.getenv("X_API_SECRET")
x_access_token = os.getenv("X_ACCESS_TOKEN")
x_access_token_secret = os.getenv("X_ACCESS_TOKEN_SECRET")

# Función para registrar al usuario
def registrar_usuario():
    try:
        respuesta = requests.post(
            f"{url_base_api}/registrar_usuarios",
            json={"usuario": usuario, "contrasena": contrasena}
        )
        
        if respuesta.status_code == 201:
            print("Usuario registrado correctamente")
            return True
        elif respuesta.status_code == 400:
            # El usuario ya existe, no es un error
            print("El usuario ya existe")
            return True
        else:
            print(f"Error registrando usuario: {respuesta.status_code}")
            return False
    except Exception as e:
        print(f"Error en registrar_usuario: {e}")
        return False

# Función para obtener el token de acceso
def obtener_token():
    try:
        respuesta_token = requests.post(
            f"{url_base_api}/iniciar_sesion", 
            auth=(usuario, contrasena)
        )
        
        if respuesta_token.status_code == 200:
            print("Token generado correctamente")
            token = respuesta_token.json().get("token_acceso")
            return token
        else:
            print(f"Error obteniendo el token: {respuesta_token.status_code}")
            return None
    except Exception as e:
        print(f"Error en obtener_token: {e}")
        return None

# Función para obtener información de un alimento
def obtener_alimento(token):
    try:
        respuesta = requests.get(
            f"{url_base_api}/obtener_info_alimentos",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        if respuesta.status_code == 200:
            datos = respuesta.json()
            print(f"Alimento obtenido: {datos.get('nombre')}")
            return datos
        elif respuesta.status_code == 404:
            print("No hay alimentos disponibles para publicar")
            return None
        else:
            print(f"Error obteniendo alimento: {respuesta.status_code}")
            return None
    except Exception as e:
        print(f"Error en obtener_alimento: {e}")
        return None

# Función para confirmar la publicación del alimento
def confirmar_publicacion(token, id_alimento):
    try:
        respuesta = requests.put(
            f"{url_base_api}/confirmar_publicacion/{id_alimento}",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        if respuesta.status_code == 200:
            print(f"Alimento {id_alimento} marcado como publicado")
            return True
        else:
            print(f"Error confirmando publicación: {respuesta.status_code}")
            return False
    except Exception as e:
        print(f"Error en confirmar_publicacion: {e}")
        return False

# Función para crear el texto del tweet
def crear_tweet(alimento):
    nombre = alimento.get("nombre")
    tipo = alimento.get("tipo")
    calorias = alimento.get("calorias")
    grasas = alimento.get("grasas")
    carbohidratos = alimento.get("carbohidratos")
    azucar = alimento.get("azucar")
    proteina = alimento.get("proteina")
    
    # Crear el texto del tweet con información nutricional
    tweet = f"{nombre} ({tipo})\n\n"
    tweet += f"Información nutricional (por 100g):\n"
    tweet += f"• Calorías: {calorias} kcal\n"
    tweet += f"• Grasas: {grasas}g\n"
    tweet += f"• Carbohidratos: {carbohidratos}g\n"
    tweet += f"• Azúcar: {azucar}g\n"
    tweet += f"• Proteína: {proteina}g\n\n"
    tweet += f"#Nutrición #Salud #{nombre.replace(' ', '')}"
    
    return tweet

# Función para publicar en X/Twitter
def publicar_en_x(texto):
    try:
        # Autenticación con la API v2 de X/Twitter
        client = tweepy.Client(
            consumer_key=x_api_key,
            consumer_secret=x_api_secret,
            access_token=x_access_token,
            access_token_secret=x_access_token_secret
        )
        
        # Publicar el tweet
        response = client.create_tweet(text=texto)
        print(f"Tweet publicado exitosamente! ID: {response.data['id']}")
        return True
    except Exception as e:
        print(f"Error publicando en X: {e}")
        return False

# Función principal
def main():
    print("Iniciando proceso de publicación diaria en X...")
    
    # Bucle infinito para publicación diaria
    while True:
        try:
            print(f"\n{'='*50}")
            print(f"Nuevo ciclo de publicación - {time.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"{'='*50}\n")
            
            # Registrar usuario si no existe
            print("Verificando/registrando usuario...")
            registrar_usuario()
            
            # Obtener token de autenticación
            token = obtener_token()
            if not token:
                print("No se pudo obtener el token. Reintentando en 24 horas.")
            else:
                # Obtener información de un alimento
                alimento = obtener_alimento(token)
                if not alimento:
                    print("No se pudo obtener información del alimento. Reintentando en 24 horas.")
                else:
                    # Crear el texto del tweet
                    texto_tweet = crear_tweet(alimento)
                    print(f"\nTweet a publicar:\n{texto_tweet}\n")
                    
                    # Publicar en X/Twitter
                    if publicar_en_x(texto_tweet):
                        # Confirmar la publicación en la base de datos
                        id_alimento = alimento.get("id")
                        if id_alimento:
                            confirmar_publicacion(token, id_alimento)
                        print("Proceso completado exitosamente!")
                    else:
                        print("Error en la publicación. No se marcará como publicado.")
            
            # Esperar 24 horas (86400 segundos) antes de la próxima publicación
            print(f"Esperando 24 horas para la próxima publicación...")
            print(f"Próxima publicación aproximadamente: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() + 86400))}")
            time.sleep(86400)
            
        except Exception as e:
            print(f"Error inesperado en el ciclo principal: {e}")
            print("Reintentando en 24 horas...")
            time.sleep(86400)

if __name__ == "__main__":
    main()
