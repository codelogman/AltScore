import requests

# Enviar la respuesta final
solution_url = "https://makers-challenge.altscore.ai/v1/s1/e8/solution"
API_KEY = "4c2212c16e7a4570aa9652b3ffa82681"
HEADERS = {
    'accept': 'application/json',
    'API-KEY': API_KEY
}
# Mensaje recibido tras usar `Revelio`
solution_data = {
    "hidden_message": ""
}

response = requests.post(solution_url, headers=HEADERS, json=solution_data)

if response.status_code == 200:
    print("¡Solución enviada correctamente! Respuesta:", response.json())
else:
    print(f"Error {response.status_code}: {response.json().get('message', 'Sin mensaje de error')}")

