"""
==============================================
INICIALIZACIÓN DE LA APLICACIÓN FLASK
==============================================
Este módulo crea y configura la aplicación Flask.

Flask es un framework web que nos permite
crear aplicaciones web de forma sencilla.

Autor: Ricardo Edreira
Fecha: Enero 2026
==============================================
"""

from flask import Flask
import os


def crear_app():
    """
    Crea y configura la aplicación Flask.
    
    Esta función es una "fábrica de aplicaciones" (app factory).
    Es un patrón común en Flask que permite crear
    múltiples instancias de la app si es necesario.
    
    Returns:
        Flask: La aplicación configurada
    """
    
    # Crear la aplicación Flask
    app = Flask(
        __name__,
        template_folder='../templates',  # Carpeta de plantillas HTML
        static_folder='../static'         # Carpeta de archivos estáticos (CSS, JS)
    )
    
    # Configurar una clave secreta para las sesiones
    # (necesaria para los mensajes flash)
    app.secret_key = os.environ.get('SECRET_KEY', 'clave-secreta-desarrollo')
    
    # Importar y registrar las rutas
    from app.rutas import rutas
    app.register_blueprint(rutas)
    
    # Mensaje de bienvenida
    print("=" * 50)
    print("🐦 X API Post Publisher")
    print("=" * 50)
    
    return app
