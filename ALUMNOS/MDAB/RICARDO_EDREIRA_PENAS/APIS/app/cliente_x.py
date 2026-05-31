"""
==============================================
CLIENTE DE LA API DE X (TWITTER)
==============================================
Este módulo maneja la conexión con la API de X
y permite publicar posts.

Incluye un "modo simulación" para desarrollo
que guarda los posts en un archivo local
en vez de publicarlos realmente.

Autor: Ricardo Edreira
Fecha: Enero 2026
==============================================
"""

import tweepy
from datetime import datetime
from app.config import obtener_configuracion, es_modo_desarrollo
from app.almacenamiento import guardar_en_historial


class ClienteX:
    """
    Clase para interactuar con la API de X (Twitter).
    
    Esta clase simplifica el uso de Tweepy y añade
    funcionalidades como validación y modo de prueba.
    """
    
    def __init__(self):
        """
        Inicializa el cliente de X.
        
        En modo producción, crea una conexión real con X.
        En modo desarrollo, solo simula las publicaciones.
        """
        self.config = obtener_configuracion()
        self.cliente = None
        
        # Solo conectar con X si estamos en modo producción
        if not es_modo_desarrollo():
            self._conectar()
    
    def _conectar(self):
        """
        Establece la conexión con la API de X.
        
        Usa OAuth 1.0a para autenticarse con las credenciales
        del archivo .env
        """
        try:
            # Crear el cliente de Tweepy para la API v2
            self.cliente = tweepy.Client(
                consumer_key=self.config['api_key'],
                consumer_secret=self.config['api_secret'],
                access_token=self.config['access_token'],
                access_token_secret=self.config['access_token_secret']
            )
            print("✅ Conectado a la API de X correctamente")
        except Exception as error:
            print(f"❌ Error al conectar con X: {error}")
            raise
    
    def validar_post(self, texto):
        """
        Valida que el texto del post sea correcto.
        
        Args:
            texto (str): El texto a validar
            
        Returns:
            tuple: (es_valido, mensaje_error)
        """
        # Quitar espacios al inicio y final
        texto = texto.strip() if texto else ""
        
        # Verificar que no esté vacío
        if not texto:
            return False, "El post no puede estar vacío"
        
        # Verificar longitud (máximo 280 caracteres)
        if len(texto) > 280:
            return False, f"El post tiene {len(texto)} caracteres. Máximo: 280"
        
        return True, None
    
    def publicar(self, texto):
        """
        Publica un post en X.
        
        En modo desarrollo, guarda el post localmente.
        En modo producción, lo publica realmente en X.
        
        Args:
            texto (str): El texto a publicar (1-280 caracteres)
            
        Returns:
            dict: Resultado con éxito, mensaje y datos del post
        """
        # Primero validar el texto
        es_valido, error = self.validar_post(texto)
        if not es_valido:
            return {
                'exito': False,
                'mensaje': error,
                'datos': None
            }
        
        # Limpiar el texto
        texto = texto.strip()
        
        # ¿Estamos en modo desarrollo?
        if es_modo_desarrollo():
            return self._publicar_simulado(texto)
        else:
            return self._publicar_real(texto)
    
    def _publicar_simulado(self, texto):
        """
        Simula una publicación (para desarrollo).
        
        Guarda el post en el historial local pero
        no lo publica realmente en X.
        """
        print(f"📝 [SIMULACIÓN] Publicando: {texto}")
        
        # Crear datos del post simulado
        datos_post = {
            'id': f"sim_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            'texto': texto,
            'fecha': datetime.now().isoformat(),
            'modo': 'simulacion'
        }
        
        # Guardar en el historial
        guardar_en_historial(datos_post)
        
        return {
            'exito': True,
            'mensaje': '¡Post simulado correctamente! (modo desarrollo)',
            'datos': datos_post
        }
    
    def _publicar_real(self, texto):
        """
        Publica realmente en X.
        
        Usa la API de X para publicar el post.
        """
        try:
            print(f"🐦 Publicando en X: {texto}")
            
            # Publicar usando Tweepy
            respuesta = self.cliente.create_tweet(text=texto)
            
            # Crear datos del post
            datos_post = {
                'id': str(respuesta.data['id']),
                'texto': texto,
                'fecha': datetime.now().isoformat(),
                'modo': 'produccion'
            }
            
            # Guardar en el historial
            guardar_en_historial(datos_post)
            
            print(f"✅ ¡Publicado! ID: {datos_post['id']}")
            
            return {
                'exito': True,
                'mensaje': '¡Post publicado en X correctamente!',
                'datos': datos_post
            }
            
        except tweepy.TooManyRequests:
            # Error de límite de peticiones
            return {
                'exito': False,
                'mensaje': 'Has alcanzado el límite de posts. Espera un rato.',
                'datos': None
            }
            
        except tweepy.Forbidden:
            # Error de permisos
            return {
                'exito': False,
                'mensaje': 'No tienes permisos. Revisa la configuración de tu app en X.',
                'datos': None
            }
            
        except tweepy.Unauthorized:
            # Error de autenticación
            return {
                'exito': False,
                'mensaje': 'Credenciales inválidas. Revisa tu archivo .env',
                'datos': None
            }
            
        except Exception as error:
            # Cualquier otro error
            return {
                'exito': False,
                'mensaje': f'Error inesperado: {str(error)}',
                'datos': None
            }
