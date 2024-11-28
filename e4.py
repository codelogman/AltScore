import requests

API_KEY = '4c2212c16e7a4570aa9652b3ffa82681'
HEADERS = {
    'accept': 'application/json',
    'API-KEY': API_KEY,
    'Content-Type': 'application/json'
}
URL = "https://makers-challenge.altscore.ai/v1/s1/e4/solution"

# Datos obtenidos de la página
usuario = "Not all those who wander"
contrasena = "are lost"

# Enviar la solución con los datos obtenidos
data = {"username": usuario, "password": contrasena}
response = requests.post(URL, headers=HEADERS, json=data)

if response.status_code == 200:
    print(f"Solución enviada correctamente. Usuario: '{usuario}', Contraseña: '{contrasena}', Respuesta: {response.json()}")
    if response.json().get("result") == "correct":
        print("¡Combinación correcta encontrada!")
else:
    print(f"Error al enviar la solución: {response.status_code}", response.json())

