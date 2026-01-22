import os
import time
import json
from mastodon import Mastodon, MastodonAPIError
from stravalib.client import Client

# --- MIS VARIABLES ---
STRAVA_ID = os.getenv('ID_CLIENTE')
STRAVA_SECRET = os.getenv('SECRETO_CLIENTE')
STRAVA_REFRESH = os.getenv('S_TOKEN_ACTUALIZACION')
MASTODON_TOKEN = os.getenv('M_TOKEN_ACCESO')
MASTODON_URL = os.getenv('MASTODON_API') 
MODO = os.getenv('ENTORNO')

ARCHIVO = '/data/history.json' # guardamos el ID de cada actividad para no repetir la publicación.
ARCHIVO_LOGS = '/data/posts_simulados.txt' # guardamos las pruebas de desarrollo

# --- VALIDACIONES DEL MENSAJE ---
def validar_mensaje(mensaje):
    # 1. Comprobar si está vacío o son solo espacios
    if not mensaje or mensaje.strip() == "":
        print("Error: El mensaje estaba vacío.")
        return False
    
    # 2. Comprobar longitud (Mastodon suele deja 500) 
    limite = 500
    if len(mensaje) > limite:
        print(f"Error: El mensaje es muy largo ({len(mensaje)} caracteres).")
        return False
        
    return True

def conectar_strava():
    try:
        client = Client()
        respuesta = client.refresh_access_token(
            client_id=STRAVA_ID,
            client_secret=STRAVA_SECRET,
            refresh_token=STRAVA_REFRESH
        )
        client.access_token = respuesta['access_token']
        return client
    except:
        print("Fallo al conectar con Strava")
        return None

def buscar_emoji(tipo):
    actividad = str(tipo) # convierto a texto por si acaso
    if "Run" in actividad: return "🏃‍♀️"
    elif "Ride" in actividad or "Bike" in actividad: return "🚴‍♀️"
    elif "Swim" in actividad: return "🏊‍♀️"
    elif "Walk" in actividad: return "🚶‍♀️"
    elif "Hike" in actividad: return "🥾"
    elif "Weight" in actividad or "Workout" in actividad or "Crossfit" in actividad: return "🏋️‍♀️"
    elif "Yoga" in actividad: return "🧘‍♀️"
    else: return "🏅"
    
    
def iniciar_bot():
    print(f"--- Mirando si hay actividades nuevas (Modo: {MODO}) ---")

    cuantas = 4  # dudo que suba mas de 4 actividades en tres horas
    
    # Si no hay historial, bajo y publico todo.
    if not os.path.exists(ARCHIVO):
        print("Primera vez: Voy a bajar las ultimas 40")
        cuantas = 40

    # 1. Conexiones
    cliente_strava = conectar_strava()
    if not cliente_strava: return
    
    # Solo conectamos Mastodon si estamos en PRODUCCION 
    mastodon = None
    if MODO == 'PRODUCCION':
        mastodon = Mastodon(access_token=MASTODON_TOKEN, api_base_url=MASTODON_URL)

    # 2. Bajo la lista
    try:
        lista = list(cliente_strava.get_activities(limit=cuantas))
    except:
        return

    # 3. Cargo historial
    subidas = []
    if os.path.exists(ARCHIVO):
        f = open(ARCHIVO, 'r')
        subidas = json.load(f)
        f.close()

    nuevas_subidas = list(subidas)
    
    lista.reverse() # aqui hay que darlo la vuelta que sino me lo leía del revés

    for resumen in lista:
        if resumen.id in subidas:
            continue
            
        print("Procesando: " + resumen.name)

        # Descripción completa
        try:
            actividad = cliente_strava.get_activity(resumen.id)
        except:
            actividad = resumen

        # Preparo el mensaje
        emoji = buscar_emoji(actividad.type)
        nombre_tipo = str(actividad.type)
        desc = actividad.description if actividad.description else ""
        
        mensaje = f"{emoji} {nombre_tipo}\n📝 {actividad.name}\n\n{desc}"
        
        # --- VALIDACIÓN ANTES DE ENVIAR ---
        if not validar_mensaje(mensaje):
            print("Salto esta actividad porque no pasó la validación.")
            continue
        
        # --- LÓGICA DESARROLLO ---
        if MODO == 'DESARROLLO':
            print("[TEST] No se publica. Guardando en archivo local...")
            
            # Guardamos en un fichero de texto para ver cómo queda
            f_log = open(ARCHIVO_LOGS, 'a')
            fecha = time.strftime("%Y-%m-%d %H:%M:%S")
            f_log.write(f"--- {fecha} ---\n{mensaje}\n-------------------\n")
            f_log.close()
            
            # Simulamos que se ha subido para guardarlo en historial
            nuevas_subidas.append(actividad.id)
            time.sleep(1)

        else:
            # MODO PRODUCCION
            try:
                mastodon.status_post(mensaje)
                print("ÉXITO: Publicado en Mastodon")
                nuevas_subidas.append(actividad.id)
                time.sleep(10)

            # --- MANEJAR ERRORES DE MASTODON ---
            except MastodonAPIError as e:
                error_str = str(e)
                if "429" in error_str:
                    print("Mastodon dice que paremos (Rate Limit 429).")
                    time.sleep(300) # Espera 5 minutos extra
                elif "500" in error_str or "503" in error_str:
                    print("Servidor Mastodon caído (500/503). Intento luego.")
                else:
                    print(f"Error desconocido al publicar: {e}")
                    
            except Exception as e:
                print(f"❌ Error genérico: {e}")

    # Guardar historial
    f = open(ARCHIVO, 'w')
    json.dump(nuevas_subidas[-100:], f)
    f.close()

if __name__ == "__main__":
    print(f"Bot AISHA arrancado en entorno: {MODO}")
    while True:
        iniciar_bot()
        time.sleep(10800) # 3 Horas