# 🐦 X (Twitter) API Automator - Python Integration

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Tweepy](https://img.shields.io/badge/Library-Tweepy-1DA1F2?logo=twitter&logoColor=white)](https://www.tweepy.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Este proyecto documenta el proceso de construcción de un automatizador para la **API v2 de X (Twitter)**, permitiendo la publicación programática de contenido mediante autenticación segura y una arquitectura profesional.

---

## 🏗️ Etapa 1: Configuración de la Infraestructura API

La base del proyecto fue la obtención de permisos en el **X Developer Portal**. Este proceso fue decisivo para habilitar la capacidad de escritura.

* **Creación del Proyecto:** Se estableció un proyecto de tipo educativo.
* **Configuración de Permisos:** Se modificó manualmente el acceso a **"Read and Write and Direct Message permissions"**. *Sin este paso, las peticiones POST serían rechazadas.*
* **Gestión de Credenciales:** Generación de las 4 llaves maestras para el flujo **OAuth 1.0a**:
    * `API Key` & `API Secret`
    * `Access Token` & `Access Token Secret`

---

## 📂 Etapa 2: Arquitectura de Archivos y Seguridad

Organización basada en estándares de escalabilidad y protección de datos sensibles.

| Archivo | Descripción |
| :--- | :--- |
| `main.py` | Script principal con la lógica de conexión y publicación. |
| `.env` | **Archivo oculto** con credenciales privadas (excluido de Git). |
| `.env.example` | Plantilla pública con las variables necesarias. |
| `.gitignore` | Filtro para evitar subir `venv/` o secretos al repositorio. |
| `requirements.txt` | Lista de dependencias para garantizar la portabilidad. |

---

## 💻 Etapa 3: Preparación del Entorno (Windows)

Gestión de dependencias mediante un entorno virtual para aislamiento total.

1.  **Creación del entorno:**
    ```bash
    python -m venv venv
    ```
2.  **Activación:**
    ```powershell
    .\venv\Scripts\activate
    ```
3.  **Instalación de librerías críticas:**
    ```bash
    pip install tweepy python-dotenv
    ```

---

## 🧠 Etapa 4: Implementación de la Lógica Principal

El archivo `main.py` se diseñó en base a tres pilares:

* **Carga de Entorno Seguro:** Uso de `load_dotenv()` para inyectar llaves en memoria.
* **Inicialización del Cliente:** Uso de `tweepy.Client` para manejar automáticamente las firmas de cabeceras OAuth.
* **Validación y Manejo de Errores:**
    * Lógica condicional para el límite máximo de **280 caracteres**.
    * Bloques `try-except` para capturar errores de red o *Rate Limits*.



---

## 🚀 Etapa 5: Ejecución y Resultados

Para poner en marcha la solución, se ejecuta el comando principal desde la terminal:

```bash
python main.py