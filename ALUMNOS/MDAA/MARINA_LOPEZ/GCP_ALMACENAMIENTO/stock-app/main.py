import logging
from google.cloud import pubsub_v1
from stock_app.callback import callback

# --- CONFIGURACIÓN ---
PROJECT_ID = "astral-bit-481514-n1"
SUBSCRIPTION_NAME = "stock-sub"

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # 1. Crear el cliente oficial de Google
    subscriber = pubsub_v1.SubscriberClient()
    
    # 2. Construir la ruta exacta manualmente
    subscription_path = subscriber.subscription_path(PROJECT_ID, SUBSCRIPTION_NAME)
    
    logging.info(f"Stock App conectada y escuchando en: {subscription_path}")

    # 3. Activar la suscripción
    # Esto conecta tu 'callback.py' directamente al flujo de mensajes
    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)

    # 4. Mantener la app encendida esperando mensajes
    try:
        streaming_pull_future.result()
    except KeyboardInterrupt:
        streaming_pull_future.cancel()
        logging.info("Apagando la app...")
    except Exception as e:
        logging.error(f"Error en la conexión: {e}")