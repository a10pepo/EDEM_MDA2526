"""
Autenticacion con Garmin Connect.
La libreria garminconnect intenta primero el endpoint movil (mas rapido)
y cae a requests si recibe 429; los avisos de rate-limit son normales.
"""
import logging
from garminconnect import Garmin
from src import config

logger = logging.getLogger(__name__)


def get_client() -> Garmin:
    client = Garmin(email=config.GARMIN_EMAIL, password=config.GARMIN_PASSWORD)
    client.login()
    logger.info("Sesion Garmin Connect iniciada correctamente")
    return client
