def validate_post(text: str):
    if not text or not text.strip():
        raise ValueError("El texto no puede estar vacío")

    if len(text) > 280:
        raise ValueError("El texto supera los 280 caracteres")
