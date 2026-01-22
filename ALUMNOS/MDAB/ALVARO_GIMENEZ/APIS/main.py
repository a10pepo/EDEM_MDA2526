import requests
import os

TOKEN_ACCESO = os.getenv("MASTODON_TOKEN")
URL = "https://mastodon.social"   

url = f"{URL}/api/v1/statuses"

headers = {
    "Authorization": f"Bearer {TOKEN_ACCESO}",
    "Content-Type": "application/json"
}

mensaje = {
    "status": "Hola muy buenos dias a todos. Este es mi primer post automático :)",
    "visibility": "public"
}

response = requests.post(url, json=mensaje, headers=headers)

if response.status_code == 200:
    print("Post publicado correctamente")
    print(response.json())
else:
    print("Error:", response.status_code)
    print(response.text)
