import requests
from statistics import mean

# URL de la PokéAPI
POKEAPI_BASE_URL = "https://pokeapi.co/api/v2/"
TYPE_URL = POKEAPI_BASE_URL + "type/"
POST_URL = "https://makers-challenge.altscore.ai/v1/s1/e6/solution"
API_KEY = "4c2212c16e7a4570aa9652b3ffa82681"  # Reemplaza con tu clave de API

HEADERS = {
    'accept': 'application/json',
    'API-KEY': API_KEY,
    'Content-Type': 'application/json'
}

def obtener_pokemons_por_tipo():
    # Obtener tipos de Pokémon
    response = requests.get(TYPE_URL)
    tipos_data = response.json()['results']
    
    # Diccionario para almacenar alturas
    alturas_por_tipo = {}
    
    for tipo in sorted(tipos_data, key=lambda x: x['name']):
        nombre_tipo = tipo['name']
        if nombre_tipo in {"shadow", "unknown"}:
            continue  # Excluimos tipos "shadow" y "unknown"
        
        tipo_response = requests.get(tipo['url']).json()
        alturas = []
        
        # Obtener altura de cada Pokémon del tipo
        for pokemon in tipo_response['pokemon']:
            pokemon_data = requests.get(pokemon['pokemon']['url']).json()
            altura = pokemon_data['height']
            alturas.append(altura)
        
        # Calcular la altura promedio
        altura_promedio = round(mean(alturas), 3) if alturas else 0
        alturas_por_tipo[nombre_tipo] = altura_promedio

    return alturas_por_tipo

def enviar_respuesta(alturas_por_tipo):
    # Crear el cuerpo de la solicitud con alturas ordenadas alfabéticamente
    data = {
        "heights": {tipo: alturas_por_tipo.get(tipo, 0) for tipo in sorted(alturas_por_tipo)}
    }

    # Enviar respuesta
    response = requests.post(POST_URL, headers=HEADERS, json=data)
    if response.status_code == 200:
        print("Respuesta enviada correctamente:", response.json())
    else:
        print(f"Error en el envío de la respuesta: {response.status_code}", response.json())

# Ejecutar flujo de datos
alturas_por_tipo = obtener_pokemons_por_tipo()
enviar_respuesta(alturas_por_tipo)

