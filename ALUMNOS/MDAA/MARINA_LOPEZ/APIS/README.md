# 📱 X API Post Publisher

## Descripción del Proyecto
Esta aplicación es una herramienta de línea de comandos (CLI) desarrollada en Python que permite interactuar con la API de X (Twitter). Fue diseñada para demostrar la capacidad de autenticación segura, publicación de contenido validado y gestión de errores.

## Características Implementadas (Features)

1.  **Menú Interactivo:** Sistema de navegación simple para elegir entre Publicar (POST) o Borrar (DELETE).
2.  **Validación de Inputs:**
    * Verifica que el tweet no esté vacío.
    * Asegura que la longitud sea menor a 280 caracteres.
3.  **Modo Seguro (Mock Mode):** Interruptor de configuración (`MOCK_MODE=True`) para simular operaciones sin consumir la cuota de la API.
4.  **Confirmación de Usuario:** "Prompt" de seguridad (yes/no) antes de ejecutar acciones irreversibles.
5.  **Feedback HTTP:** Muestra al usuario los códigos de estado HTTP simulados o reales (201 Created, 200 OK, 400 Bad Request).
6.  **Manejo de Errores (Error Handling):** Captura específica de errores de API como 401 (Credenciales), 403 (Permisos) y 404 (No encontrado).

## 🛠️ Tecnologías Utilizadas

* **Lenguaje:** Python 
* **Librería Principal:** `Tweepy` (Wrapper oficial para X API v2)
* **Seguridad:** `python-dotenv` (Para manejo de variables de entorno)

## 🎓 Conceptos del Curso Aplicados

El desarrollo de este proyecto se basó en los siguientes conceptos aprendidos:

* **Autenticación OAuth:** Uso de claves (Consumer Keys) y tokens de acceso para autenticar la aplicación de forma segura.
* **Seguridad de Secretos:** Implementación de archivos `.env` y `.gitignore` para no exponer credenciales en el repositorio.
* **Códigos de Estado HTTP:** Implementación lógica de respuestas basada en estándares web (201 para creación, 400 para errores de cliente, 500 para errores de servidor).
* **Manejo de Excepciones (Try/Except):** Estructura robusta para capturar fallos de red o de API sin romper la ejecución del programa.
* **CRUD Básico:** Implementación de operaciones Create (Publicar) y Delete (Borrar).

## ⚙️ Prerrequisitos

* Python 3 instalado.
* Una cuenta de desarrollador en X (Twitter Developer Portal) con acceso "Free Tier".
* Claves de API generadas con permisos de **Lecture y Escritura (Read and Write)**.

## 🚀 Instalación y Configuración

Sigue estos pasos para ejecutar el proyecto en tu máquina local:

### 1. creo el entorno
python3 -m venv venv
source venv/bin/activate

### 2. instalo dependencias
pip install tweepy python-dotenv

### 3. configurar .env con tus credenciales 
### 4. Iniciar aplicacion
python3 tw.py

### 5. Selecciono la opcion deseada

## 🚀 Publicar un Tweet
![alt text](<Captura de pantalla 2025-12-17 a la(s) 1.11.40 p. m..png>)
[alt text](<Captura de pantalla 2025-12-17 a la(s) 1.11.47 p. m..png>)

## 🚀 Borrar un Tweet
![alt text](<Captura de pantalla 2025-12-17 a la(s) 12.59.19 p. m..png>)

## 🚀 Limitaciones

Límite de Rate Limit: Solo se permiten 17 posts cada 24 horas. Para esto se implementó el Mock Mode.
Falsos Positivos al Borrar: La API de X tiene una particularidad: a veces devuelve un código `Tweet eliminado correctamente.`al insertar un ID inventado

## Mejoras

Este desafío me ha permitido descubrir el potencial del mundo de las APIs. Aunque el proyecto es funcional, siento que apenas he rasgado la superficie y que me queda mucho por indagar. Soy consciente de las infinitas posibilidades que ofrece la integración con otras APIs, y si dispusiera de más tiempo, me encantaría seguir explorando para llevar esta herramienta a un siguiente nivel.