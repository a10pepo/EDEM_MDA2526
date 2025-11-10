import requests
#try:
url_rae = "https://rae-api.com/api/random"
response_rae = requests.get(url_rae)
convert_rae = response_rae.json()['data']['word'].lower()
print(convert_rae)
#     palabra_rae = convert_rae.get("palabra", []) # No puedo comprobar el output puesto que la API está caída

# except:
#     print("Error al conectar con la API de la RAE")
#     exit