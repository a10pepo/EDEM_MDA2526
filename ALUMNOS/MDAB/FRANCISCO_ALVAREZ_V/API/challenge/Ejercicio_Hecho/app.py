

import os
import json
import requests
from datetime import datetime
from requests_oauthlib import OAuth1
from dotenv import load_dotenv


load_dotenv()


# CONFIGURATION



X_API_KEY = os.getenv('X_API_KEY')
X_API_SECRET = os.getenv('X_API_SECRET')
X_ACCESS_TOKEN = os.getenv('X_ACCESS_TOKEN')
X_ACCESS_TOKEN_SECRET = os.getenv('X_ACCESS_TOKEN_SECRET')
APP_MODE = os.getenv('APP_MODE', 'development')
X_API_POST_URL = 'https://api.x.com/2/tweets'
POSTS_FILE = 'posts_history.json'

def validate_credentials():
    """
    Validate that all required X API credentials are configured.

    Returns:
        tuple: (is_valid: bool, error_message: str or None)
    """
    credentials = {
        'X_API_KEY': X_API_KEY,
        'X_API_SECRET': X_API_SECRET,
        'X_ACCESS_TOKEN': X_ACCESS_TOKEN,
        'X_ACCESS_TOKEN_SECRET': X_ACCESS_TOKEN_SECRET
    }

    missing = [name for name, value in credentials.items()
               if not value or value.startswith('tu_')]

    if missing:
        return False, f"Credenciales faltantes o no configuradas lo siento =( ): {', '.join(missing)}"

    return True, None


def validate_post_content(text):
    
    """
    Validate post content according to X API requirements.

    Args:
        text: The post content to validate

    Returns:
        tuple: (is_valid: bool, error_message: str or None)
    """
    
    if text is None:
        return False, "El contenido del post no puede ser None"

    if not isinstance(text, str):
        return False, "El contenido del post debe ser un string"


    stripped_text = text.strip()

    if len(stripped_text) == 0:
        return False, "El post no puede estar vacio o contener solo espacios en blanco"

    if len(text) > 280:
        return False, f"El post excede el limite de 280 caracteres (actual: {len(text)})"

    return True, None

def load_posts_history():
    """Load posts history from local JSON file."""
    if os.path.exists(POSTS_FILE):
        try:
            with open(POSTS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []
    return []


def save_post_to_history(post_data):
    """
    Save a post to local history.

    Args:
        post_data: Dictionary with post information
    """
    history = load_posts_history()
    history.append(post_data)

    with open(POSTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, indent=2, ensure_ascii=False)


def get_posts_history():
    """Get all posts from local history."""
    return load_posts_history()


def create_oauth1_auth():
    """
    Create OAuth1 authentication object for X API.

    Returns:
        OAuth1 object for requests authentication
    """
    return OAuth1(
        X_API_KEY,
        client_secret=X_API_SECRET,
        resource_owner_key=X_ACCESS_TOKEN,
        resource_owner_secret=X_ACCESS_TOKEN_SECRET
    )


def publish_post_mock(text):
    """
    Mock function to simulate posting (development mode).
    Saves to local file instead of calling X API.

    Args:
        text: The post content

    Returns:
        dict: Simulated response with post data
    """
    import random

    # Generate a fake post ID
    fake_id = str(random.randint(1000000000000000000, 9999999999999999999))

    post_data = {
        'id': fake_id,
        'text': text,
        'created_at': datetime.now().isoformat(),
        'mode': 'mock',
        'status': 'saved_locally'
    }

    save_post_to_history(post_data)

    return {
        'success': True,
        'data': post_data,
        'message': '[MODO MOCK] Post guardado localmente (no enviado a X API)'
    }


def publish_post_real(text):
    """
    Publish a post to X API (production mode).

    Args:
        text: The post content

    Returns:
        dict: Response with success status and data or error
    """
    auth = create_oauth1_auth()

    payload = {'text': text}
    headers = {'Content-Type': 'application/json'}

    try:
        response = requests.post(
            X_API_POST_URL,
            json=payload,
            auth=auth,
            headers=headers,
            timeout=30
        )

        # Parse response
        response_data = response.json()

        # Handle different HTTP status codes
        if response.status_code == 201:
            # Success - post created
            post_data = {
                'id': response_data['data']['id'],
                'text': response_data['data']['text'],
                'created_at': datetime.now().isoformat(),
                'mode': 'production',
                'status': 'published'
            }
            save_post_to_history(post_data)

            return {
                'success': True,
                'data': post_data,
                'message': 'Post publicado exitosamente en X'
            }

        elif response.status_code == 401:
            return {
                'success': False,
                'error': 'UNAUTHORIZED',
                'message': 'Credenciales invalidas. Verifica tu API Key, API Secret, Access Token y Access Token Secret.',
                'help': 'Regenera tus tokens en el Portal de Desarrolladores de X'
            }

        elif response.status_code == 403:
            error_detail = response_data.get('detail', 'Acceso denegado')
            return {
                'success': False,
                'error': 'FORBIDDEN',
                'message': f'Acceso denegado: {error_detail}',
                'help': 'Verifica que tu Access Token tenga permisos "Read and Write"'
            }

        elif response.status_code == 429:
            return {
                'success': False,
                'error': 'RATE_LIMIT',
                'message': 'Has excedido el limite de publicaciones. Espera antes de intentar de nuevo.',
                'help': 'El nivel gratuito permite 17 posts por 24 horas'
            }

        else:
            error_msg = response_data.get('detail', response_data.get('title', 'Error desconocido'))
            return {
                'success': False,
                'error': f'HTTP_{response.status_code}',
                'message': f'Error de la API: {error_msg}',
                'raw_response': response_data
            }

    except requests.exceptions.Timeout:
        return {
            'success': False,
            'error': 'TIMEOUT',
            'message': 'La solicitud a X API tardo demasiado. Intenta de nuevo.'
        }

    except requests.exceptions.ConnectionError:
        return {
            'success': False,
            'error': 'CONNECTION_ERROR',
            'message': 'No se pudo conectar a X API. Verifica tu conexion a internet.'
        }

    except requests.exceptions.RequestException as e:
        return {
            'success': False,
            'error': 'REQUEST_ERROR',
            'message': f'Error de red: {str(e)}'
        }

    except json.JSONDecodeError:
        return {
            'success': False,
            'error': 'INVALID_RESPONSE',
            'message': 'La respuesta de X API no es JSON valido'
        }


def publish_post(text, dry_run=False):
    """
    Main function to publish a post.
    Routes to mock or real API based on APP_MODE.

    Args:
        text: The post content
        dry_run: If True, only validate without publishing

    Returns:
        dict: Response with success status and data or error
    """
    # Validate post content
    is_valid, error_msg = validate_post_content(text)
    if not is_valid:
        return {
            'success': False,
            'error': 'VALIDATION_ERROR',
            'message': error_msg
        }

    # Dry run mode - just validate
    if dry_run:
        return {
            'success': True,
            'message': f'[DRY RUN] Post valido ({len(text)} caracteres). No se publicara.',
            'data': {'text': text, 'length': len(text)}
        }

    # Development mode - use mock
    if APP_MODE == 'development':
        return publish_post_mock(text)

    # Production mode - validate credentials first
    is_valid, error_msg = validate_credentials()
    if not is_valid:
        return {
            'success': False,
            'error': 'CREDENTIALS_ERROR',
            'message': error_msg,
            'help': 'Configura tus credenciales en el archivo .env'
        }

    # Call real X API
    return publish_post_real(text)


def print_header():
    """Print application header."""
    print("\n" + "=" * 60)
    print("  X API Challenge - Post Publisher")
    print("=" * 60)
    print(f"  Modo: {APP_MODE.upper()}")
    if APP_MODE == 'development':
        print("  (Los posts se guardaran localmente, no se enviaran a X)")
    print("=" * 60 + "\n")


def print_menu():
    """Print main menu options."""
    print("\nOpciones:")
    print("  1. Publicar un nuevo post")
    print("  2. Ver historial de posts")
    print("  3. Verificar credenciales")
    print("  4. Cambiar modo (development/production)")
    print("  5. Salir")
    print()


def handle_new_post():
    """Handle creating and publishing a new post."""
    print("\n--- Nuevo Post ---")
    print("(Escribe tu post, maximo 280 caracteres)")
    print("(Escribe 'cancelar' para volver al menu)\n")

    text = input("Tu post: ").strip()

    if text.lower() == 'cancelar':
        print("Cancelado.")
        return

    # Show character count
    print(f"\nCaracteres: {len(text)}/280")

    # Validate first
    is_valid, error_msg = validate_post_content(text)
    if not is_valid:
        print(f"\nError: {error_msg}")
        return

    # Confirm before publishing
    if APP_MODE == 'production':
        confirm = input("\nEsta seguro de que quiere publicar esto? (s/n): ").strip().lower()
        if confirm != 's':
            print("Publicacion cancelada.")
            return

    # Publish
    print("\nPublicando...")
    result = publish_post(text)

    if result['success']:
        print(f"\nExito! {result['message']}")
        if 'data' in result:
            print(f"ID: {result['data'].get('id', 'N/A')}")
            print(f"Texto: {result['data'].get('text', text)}")
    else:
        print(f"\nError: {result['message']}")
        if 'help' in result:
            print(f"Ayuda: {result['help']}")


def handle_view_history():
    """Handle viewing post history."""
    print("\n--- Historial de Posts ---")

    history = get_posts_history()

    if not history:
        print("No hay posts en el historial.")
        return

    print(f"Total: {len(history)} posts\n")

    for i, post in enumerate(history[-10:], 1):  # Show last 10
        mode = post.get('mode', 'unknown')
        status = post.get('status', 'unknown')
        created = post.get('created_at', 'N/A')
        text = post.get('text', '')

        # Truncate long posts for display
        display_text = text[:50] + "..." if len(text) > 50 else text

        print(f"{i}. [{mode}] {display_text}")
        print(f"   ID: {post.get('id', 'N/A')} | Fecha: {created}")
        print()


def handle_verify_credentials():
    """Handle verifying X API credentials."""
    print("\n--- Verificacion de Credenciales ---")

    is_valid, error_msg = validate_credentials()

    if is_valid:
        print("Todas las credenciales estan configuradas.")
        print("\nCredenciales detectadas:")
        print(f"  X_API_KEY: {'*' * 8}...{X_API_KEY[-4:] if X_API_KEY else 'NO CONFIGURADA'}")
        print(f"  X_API_SECRET: {'*' * 8}...{X_API_SECRET[-4:] if X_API_SECRET else 'NO CONFIGURADA'}")
        print(f"  X_ACCESS_TOKEN: {'*' * 8}...{X_ACCESS_TOKEN[-4:] if X_ACCESS_TOKEN else 'NO CONFIGURADA'}")
        print(f"  X_ACCESS_TOKEN_SECRET: {'*' * 8}...{X_ACCESS_TOKEN_SECRET[-4:] if X_ACCESS_TOKEN_SECRET else 'NO CONFIGURADA'}")
    else:
        print(f"Error: {error_msg}")
        print("\nAsegurate de:")
        print("  1. Copiar .env.example a .env")
        print("  2. Llenar tus credenciales reales del Portal de Desarrolladores de X")


def handle_change_mode():
    """Handle changing application mode."""
    global APP_MODE

    print("\n--- Cambiar Modo ---")
    print(f"Modo actual: {APP_MODE}")
    print("\nOpciones:")
    print("  1. development (mock - guarda localmente)")
    print("  2. production (real - publica en X)")

    choice = input("\nElige (1/2): ").strip()

    if choice == '1':
        APP_MODE = 'development'
        print("Modo cambiado a: development")
    elif choice == '2':
        # Verify credentials before switching to production
        is_valid, error_msg = validate_credentials()
        if not is_valid:
            print(f"\nNo se puede cambiar a production: {error_msg}")
            return
        APP_MODE = 'production'
        print("Modo cambiado a: production")
        print("ADVERTENCIA: Los posts se publicaran en tu cuenta de X!")
    else:
        print("Opcion invalida.")


def main():
    """Main CLI loop."""
    print_header()

    while True:
        print_menu()

        choice = input("Elige una opcion (1-5): ").strip()

        if choice == '1':
            handle_new_post()
        elif choice == '2':
            handle_view_history()
        elif choice == '3':
            handle_verify_credentials()
        elif choice == '4':
            handle_change_mode()
        elif choice == '5':
            print("\nHasta luego!")
            break
        else:
            print("Opcion invalida. Elige 1-5.")


if __name__ == '__main__':
    main()
