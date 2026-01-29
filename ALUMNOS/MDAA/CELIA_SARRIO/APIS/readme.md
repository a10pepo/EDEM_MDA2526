# X Post Publisher 🚀

Aplicación en Python que permite **publicar un tweet real en X (Twitter)** utilizando la **X API v2**, con un flujo sencillo y controlado.  
El contenido del tweet se **genera automáticamente en base a un tópico**, evitando la necesidad de introducir texto manualmente y mejorando la usabilidad.

Este proyecto ha sido desarrollado como **trabajo académico** para aprender a integrar APIs REST, aplicar buenas prácticas de seguridad y diseñar una aplicación clara y mantenible.

---

## ✨ Características principales

- 📌 Publicación **real** de tweets en X
- 🧠 Generación automática de contenido por tópicos
- 👀 Vista previa del tweet antes de publicar
- 👍 Confirmación explícita del usuario
- 🧪 Modo *development* y *production*
- 💾 Persistencia local de tweets publicados (JSON)
- 🔒 Gestión segura de credenciales mediante variables de entorno
- ✅ Validación de contenido (vacío y longitud máxima)
- ⚠️ Manejo básico de errores de la API

---

## 🧩 Flujo de funcionamiento

1. El usuario ejecuta la aplicación manualmente.
2. Selecciona un **tópico** predefinido.
3. La aplicación **genera automáticamente el tweet**.
4. Se muestra una **preview** del contenido.
5. El usuario confirma si desea publicarlo.
6. El tweet se publica en X (solo en modo `production`).

> En cada ejecución se publica **como máximo un tweet**, garantizando control total sobre la publicación.

---

## 🏷️ Tópicos disponibles

- `technology`
- `programming`
- `education`
- `sports`
- `random`

Cada tópico genera mensajes coherentes y variados, incluyendo información temporal para evitar duplicados.

---

## 🛠️ Tecnologías utilizadas

- **Python 3**
- **Tweepy** (X API v2)
- **python-dotenv**
- API REST oficial de X (Twitter)

---

## 📁 Estructura del proyecto
```bash
x-post-publisher/
│
├── main.py # Flujo principal de la aplicación
├── topic_generator.py # Generación automática de tweets por tópico
├── x_client.py # Cliente de la X API
├── storage.py # Persistencia local en JSON
├── validators.py # Validación de contenido
│
├── data/
│ └── published.json # Tweets publicados
│
├── .env.example
├── requirements.txt
└── README.md
```

## ⚙️ Instalación

1. Clona el repositorio:
```bash
git clone https://github.com/celiiasarrio/x-post-publisher
cd x-post-publisher
```

2. Instala las dependencias:
```bash
pip install -r requirements.txt
```

## 🔐 Configuración

Crea un archivo .env con este formato y tus credenciales:
```bash
APP_MODE=production
X_API_KEY=tu_api_key
X_API_SECRET=tu_api_secret
X_ACCESS_TOKEN=tu_access_token
X_ACCESS_TOKEN_SECRET=tu_access_token_secret
```
⚠️ Nunca subas el archivo .env al repositorio.

## ▶️ Uso

Ejecuta la aplicación:
```bash
python main.py
```
Sigue las instrucciones en pantalla para seleccionar un tópico y confirmar la publicación.

## 🧪 Modos de ejecución

- development
El tweet no se publica en X.
Se guarda únicamente en published.json.

- production
El tweet se publica realmente en X utilizando la API oficial.

## 🔒 Seguridad

- Las credenciales se gestionan exclusivamente mediante variables de entorno

- No hay claves ni tokens hardcodeados en el código

- El proyecto es seguro para repositorios públicos

## 📉 Limitaciones de la X API Free Tier

- Máximo 17 tweets por día

- Acceso limitado a operaciones de lectura

- Sin métricas ni analíticas avanzadas

Estas limitaciones se han tenido en cuenta en el diseño del proyecto.

## 📚 Conceptos del curso aplicados

- Integración con APIs REST

- Autenticación mediante tokens

- Validación de datos de entrada

- Manejo de errores HTTP

- Persistencia local

- Separación de responsabilidades

- Buenas prácticas de seguridad

## 🚀 Posibles mejoras futuras

- Integración con APIs públicas (quotes, news, facts)

- Generación dinámica de hashtags

- Interfaz web para selección de tópicos

- Programación de publicaciones

- Tests unitarios e integración continua

