import os
import sys #para leer argumentos de la terminal, imprimir errores y salir del programa
import json #para manejar datos en formato JSON
import requests #para hacer solicitudes HTTP
from dotenv import load_dotenv #para cargar variables de entorno desde un archivo .env

MAX_LEN_DEFAULT = 500

def die(msg: str, code: int = 1): # Función para manejar errores
    print(f"❌ {msg}", file=sys.stderr) # Imprimir mensaje de error en stderr
    sys.exit(code) # Salir del programa con un código de error

def normalize_instance(url: str) -> str: # Normaliza la URL de la instancia de Mastodon
    url = (url or "").strip() # Elimina espacios en blanco
    if not url:
        die("MASTODON_INSTANCE_URL está vacío.")
    return url[:-1] if url.endswith("/") else url

def validate_status(text: str, max_len: int = MAX_LEN_DEFAULT) -> str: # Valida el texto del status
    if text is None:
        die("El status es None.")
    cleaned = text.strip()
    if not cleaned:
        die("El status no puede estar vacío o solo espacios.")
    if len(cleaned) > max_len:
        die(f"El status supera el máximo ({max_len}). Longitud actual: {len(cleaned)}.")
    return cleaned

def post_status(instance: str, token: str, status_text: str): # Publica el status en Mastodon
    url = f"{instance}/api/v1/statuses"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
    }
    payload = {"status": status_text}

    try: # Hacer la solicitud POST
        resp = requests.post(url, headers=headers, data=payload, timeout=20)
    except requests.RequestException as e:
        die(f"Error de red llamando a Mastodon: {e}")

    if resp.status_code == 429: # Manejo de límite 
        retry_after = resp.headers.get("Retry-After")
        msg = "Rate limit (HTTP 429)."
        if retry_after:
            msg += f" Reintenta en ~{retry_after} segundos."
        die(msg, 2)

    if resp.status_code in (401, 403):
        die(f"Token inválido o sin permisos (HTTP {resp.status_code}). Revisa scopes (write:statuses).", 3)

    if resp.status_code >= 400:
        try:
            err = resp.json()
        except Exception:
            err = {"raw": resp.text}
        die(f"Error HTTP {resp.status_code}: {json.dumps(err, ensure_ascii=False)}", 4)

    try:
        return resp.json()
    except Exception:
        die("Respuesta no-JSON inesperada (aunque fue 2xx).", 5)

def main(): # Función principal
    load_dotenv()
    token = os.getenv("MASTODON_ACCESS_TOKEN", "").strip()
    instance = normalize_instance(os.getenv("MASTODON_INSTANCE_URL", ""))

    if not token:
        die("Falta MASTODON_ACCESS_TOKEN en tu entorno (.env).")

    if len(sys.argv) < 2:
        die('Uso: python mastodon_post.py "Tu status"')

    status_text = validate_status(sys.argv[1])

    print("📝 Status a publicar:", status_text)
    confirm = input("¿Publicar? (s/N): ").strip().lower()
    if confirm != "s":
        print("Cancelado.")
        return

    data = post_status(instance, token, status_text) # Publicar el status
    print("✅ Publicado correctamente.")
    if data.get("url"):
        print("🔗 URL:", data["url"])
    elif data.get("uri"):
        print("🔗 URI:", data["uri"])

if __name__ == "__main__":
    main()
