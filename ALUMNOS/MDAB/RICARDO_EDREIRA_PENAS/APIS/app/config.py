"""
==============================================
MÓDULO DE CONFIGURACIÓN
==============================================
Este módulo carga las credenciales de la API de X
desde el archivo .env y las hace disponibles
para el resto de la aplicación.

Autor: Ricardo Edreira
Fecha: Enero 2026
==============================================
"""

import os
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()


def obtener_configuracion():
    """
    Obtiene la configuración de la aplicación.
    
    Lee las credenciales de X API y el modo de la aplicación
    desde las variables de entorno.
    
    Returns:
        dict: Diccionario con toda la configuración
    
    Raises:
        ValueError: Si faltan credenciales en modo producción
    """
    
    # Leer las variables de entorno
    configuracion = {
        # Credenciales de X API
        'api_key': os.getenv('X_API_KEY'),
        'api_secret': os.getenv('X_API_SECRET'),
        'access_token': os.getenv('X_ACCESS_TOKEN'),
        'access_token_secret': os.getenv('X_ACCESS_TOKEN_SECRET'),
        
        # Modo de la aplicación (development o production)
        'modo': os.getenv('APP_MODE', 'development')
    }
    
    # En modo producción, verificar que existan las credenciales
    if configuracion['modo'] == 'production':
        credenciales = [
            configuracion['api_key'],
            configuracion['api_secret'],
            configuracion['access_token'],
            configuracion['access_token_secret']
        ]
        
        if not all(credenciales):
            raise ValueError(
                "¡Faltan credenciales de X API! "
                "Revisa tu archivo .env"
            )
    
    return configuracion


def es_modo_desarrollo():
    """
    Verifica si estamos en modo desarrollo.
    
    Returns:
        bool: True si estamos en modo desarrollo
    """
    config = obtener_configuracion()
    return config['modo'] == 'development'
