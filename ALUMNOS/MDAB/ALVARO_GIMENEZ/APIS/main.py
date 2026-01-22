import requests

URL = "https://mastodon.social"   
TOKEN_ACCESO = "KXm2pL6A-gia3j2p9jrio-d1uUO6j8cBrINEbUcNh0s"

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
