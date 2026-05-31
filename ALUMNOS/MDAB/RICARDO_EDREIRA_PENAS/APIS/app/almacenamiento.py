"""
==============================================
MÓDULO DE ALMACENAMIENTO LOCAL
==============================================
Este módulo maneja el guardado de datos locales:
- Historial de posts publicados
- Borradores guardados

Los datos se guardan en archivos JSON en la
carpeta 'data/' del proyecto.

Autor: Ricardo Edreira
Fecha: Enero 2026
==============================================
"""

import json
import os
from datetime import datetime

# Carpeta donde se guardan los datos
CARPETA_DATOS = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')

# Archivos de datos
ARCHIVO_HISTORIAL = os.path.join(CARPETA_DATOS, 'historial.json')
ARCHIVO_BORRADORES = os.path.join(CARPETA_DATOS, 'borradores.json')


def _asegurar_carpeta():
    """
    Crea la carpeta de datos si no existe.
    """
    if not os.path.exists(CARPETA_DATOS):
        os.makedirs(CARPETA_DATOS)


def _leer_json(archivo):
    """
    Lee un archivo JSON y devuelve su contenido.
    
    Args:
        archivo (str): Ruta al archivo
        
    Returns:
        list: Lista de elementos del archivo (vacía si no existe)
    """
    _asegurar_carpeta()
    
    if os.path.exists(archivo):
        try:
            with open(archivo, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []
    return []


def _escribir_json(archivo, datos):
    """
    Escribe datos en un archivo JSON.
    
    Args:
        archivo (str): Ruta al archivo
        datos (list): Lista de datos a guardar
    """
    _asegurar_carpeta()
    
    with open(archivo, 'w', encoding='utf-8') as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)


# ==============================================
# FUNCIONES PARA EL HISTORIAL DE POSTS
# ==============================================

def guardar_en_historial(post):
    """
    Guarda un post en el historial.
    
    Args:
        post (dict): Datos del post publicado
    """
    historial = _leer_json(ARCHIVO_HISTORIAL)
    historial.insert(0, post)  # Añadir al principio
    _escribir_json(ARCHIVO_HISTORIAL, historial)


def obtener_historial():
    """
    Obtiene todo el historial de posts.
    
    Returns:
        list: Lista de posts publicados (más reciente primero)
    """
    return _leer_json(ARCHIVO_HISTORIAL)


def contar_posts_hoy():
    """
    Cuenta cuántos posts se han publicado hoy.
    
    Returns:
        int: Número de posts publicados hoy
    """
    historial = obtener_historial()
    hoy = datetime.now().date().isoformat()
    
    contador = 0
    for post in historial:
        # Obtener solo la fecha del post
        fecha_post = post.get('fecha', '')[:10]
        if fecha_post == hoy:
            contador += 1
    
    return contador


# ==============================================
# FUNCIONES PARA BORRADORES
# ==============================================

def guardar_borrador(texto):
    """
    Guarda un nuevo borrador.
    
    Args:
        texto (str): Texto del borrador
        
    Returns:
        dict: El borrador guardado con su ID
    """
    borradores = _leer_json(ARCHIVO_BORRADORES)
    
    # Crear nuevo borrador con ID único
    nuevo_borrador = {
        'id': f"borr_{datetime.now().strftime('%Y%m%d%H%M%S')}",
        'texto': texto,
        'fecha_creacion': datetime.now().isoformat()
    }
    
    borradores.insert(0, nuevo_borrador)
    _escribir_json(ARCHIVO_BORRADORES, borradores)
    
    return nuevo_borrador


def obtener_borradores():
    """
    Obtiene todos los borradores guardados.
    
    Returns:
        list: Lista de borradores
    """
    return _leer_json(ARCHIVO_BORRADORES)


def obtener_borrador(id_borrador):
    """
    Obtiene un borrador específico por su ID.
    
    Args:
        id_borrador (str): ID del borrador
        
    Returns:
        dict: El borrador encontrado o None
    """
    borradores = obtener_borradores()
    
    for borrador in borradores:
        if borrador['id'] == id_borrador:
            return borrador
    
    return None


def eliminar_borrador(id_borrador):
    """
    Elimina un borrador.
    
    Args:
        id_borrador (str): ID del borrador a eliminar
        
    Returns:
        bool: True si se eliminó, False si no existía
    """
    borradores = _leer_json(ARCHIVO_BORRADORES)
    
    # Buscar y eliminar
    for i, borrador in enumerate(borradores):
        if borrador['id'] == id_borrador:
            borradores.pop(i)
            _escribir_json(ARCHIVO_BORRADORES, borradores)
            return True
    
    return False
