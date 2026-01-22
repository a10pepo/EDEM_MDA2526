# Cómo hice este proyecto

Esta guía explica los pasos que seguí para construir la aplicación.

---

## 1. Setup inicial

Primero creé la estructura de carpetas:

```bash
mkdir -p app static/css static/js templates data
```

Luego el entorno virtual:

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 2. Dependencias

Fichero `requirements.txt`:
```
flask>=3.0.0
tweepy>=4.14.0
python-dotenv>=1.0.0
```

---

## 3. Configuración

Creé `app/config.py` para cargar las credenciales:

```python
from dotenv import load_dotenv
import os

load_dotenv()

def obtener_configuracion():
    return {
        'api_key': os.getenv('X_API_KEY'),
        # ... resto de credenciales
    }
```

---

## 4. Cliente de X

En `app/cliente_x.py` usé Tweepy:

```python
import tweepy

class ClienteX:
    def __init__(self):
        self.cliente = tweepy.Client(...)
    
    def publicar(self, texto):
        # Validar longitud
        if len(texto) > 280:
            return error
        
        # Publicar
        respuesta = self.cliente.create_tweet(text=texto)
```

Para el modo desarrollo, simplemente guardo en un JSON en vez de publicar.

---

## 5. Almacenamiento

`app/almacenamiento.py` maneja el guardado local:

```python
def guardar_en_historial(post):
    historial = leer_json('historial.json')
    historial.insert(0, post)
    escribir_json('historial.json', historial)
```

Similar para los borradores.

---

## 6. Rutas Flask

En `app/rutas.py`:

```python
@rutas.route('/publicar', methods=['POST'])
def publicar():
    texto = request.form.get('texto')
    cliente = ClienteX()
    resultado = cliente.publicar(texto)
    
    if resultado['exito']:
        flash('Publicado!', 'exito')
    return redirect('/')
```

---

## 7. Templates HTML

Usé Jinja2 para las plantillas. `base.html` tiene la estructura común y las demás heredan de ella.

---

## 8. CSS

Hice un tema oscuro con variables CSS:

```css
:root {
    --color-fondo: #15202b;
    --color-primario: #1d9bf0;
}
```

---

## 9. JavaScript

El contador de caracteres:

```javascript
function actualizarContador() {
    const textarea = document.getElementById('texto-post');
    const contador = document.getElementById('caracteres-actuales');
    contador.textContent = textarea.value.length;
}
```

---

## 10. Docker

Dockerfile básico:

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "run.py"]
```
---

## Recursos útiles

- Documentación de Tweepy
- Flask documentation
- X API docs
