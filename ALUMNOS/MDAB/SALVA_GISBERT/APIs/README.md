🚀 X Auto-Poster API
Este proyecto es un script de automatización en Python que permite publicar posts (tweets) en X (Twitter) utilizando su API v2. Está diseñado para ser una herramienta sencilla pero robusta, siguiendo las mejores prácticas de seguridad al manejar credenciales sensibles.

🌟 Funcionalidades Implementadas
Publicación Automatizada: Envío de mensajes de texto a X mediante peticiones HTTP.

Autenticación Segura: Implementación de OAuth 1.0a para la firma de peticiones.

Gestión de Entorno: Separación de credenciales sensibles mediante el uso de archivos .env.

Arquitectura Limpia: Código modular y fácil de integrar en otros flujos de trabajo (pipelines de datos, bots, etc.).

🛠️ Tecnologías Utilizadas
Lenguaje: Python 3.x

Librerías principales:

requests: Para la comunicación con la API.

requests-oauthlib: Para gestionar la firma de seguridad OAuth 1.0a.

python-dotenv: Para la carga de variables de entorno.

📋 Requisitos Previos
Python 3.10 o superior instalado.

Una cuenta en X Developer Portal con un Proyecto y una App creados.

Permisos de la App configurados como "Read and Write".

⚙️ Instalación Paso a Paso
Clonar el repositorio:

Bash

git clone https://github.com/tu-usuario/nombre-del-repo.git
cd nombre-del-repo
Crear un entorno virtual (opcional pero recomendado):

Bash

python -m venv venv
# En Windows (Git Bash):
source venv/Scripts/activate
Instalar las librerías necesarias: Ejecuta el siguiente comando para instalar todas las dependencias de una vez:

Bash

pip install requests requests-oauthlib python-dotenv
🔐 Configuración (Archivo .env)
Para que el script funcione, debes crear un archivo llamado .env en la raíz del proyecto. Nunca subas este archivo a GitHub.

Crea el archivo: touch .env

Añade tus credenciales del X Developer Portal:

Plaintext

CONSUMER_KEY="tu_api_key_aqui"
CONSUMER_SECRET="tu_api_key_secret_aqui"
ACCESS_TOKEN="tu_access_token_aqui"
ACCESS_TOKEN_SECRET="tu_access_token_secret_aqui"
Nota: Si cambias los permisos de la app a "Read and Write", recuerda darle a "Regenerate" en el portal para obtener nuevos tokens válidos.

🚀 Uso del Script
Para ejecutar el programa y publicar tu post, simplemente corre:

Bash

python postOnX.py
El script buscará las credenciales en el archivo .env y enviará el mensaje configurado en el bloque if __name__ == "__main__":.

📸 Capturas de Pantalla
Ejemplo del script ejecutándose con éxito en la terminal y el post apareciendo en X.

💡 Conceptos de Clase Aplicados
Este proyecto aplica conceptos clave del módulo de APIs:

Métodos HTTP: Uso específico de POST para la creación de recursos.

Autenticación y Autorización: Diferencia práctica entre Bearer Tokens y OAuth 1.0a User Context.

Seguridad: Gestión de secretos para evitar fugas de información en repositorios públicos.

⚠️ Limitaciones y Problemas Conocidos
API Free Tier: La cuenta gratuita de X tiene un límite estricto de posts mensuales (actualmente 1,500 posts/mes a nivel de app).

Contenido: Solo soporta texto plano. No incluye subida de imágenes/media en esta versión.

Error 403: Si recibes este error, es probable que tus tokens no tengan permisos de escritura.