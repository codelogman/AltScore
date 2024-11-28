import requests

API_KEY = '4c2212c16e7a4570aa9652b3ffa82681'
HEADERS = {
    'accept': 'application/json',
    'API-KEY': API_KEY,
    'Content-Type': 'application/json'
}
BASE_URL = "https://makers-challenge.altscore.ai/v1/s1/e3/resources/"
SWAPI_BASE_URL = "https://swapi.dev/api/"

# Función para obtener personajes y planetas
def obtener_datos_star_wars():
    personajes = []
    planetas = {}

    # Obtener datos de personajes
    response = requests.get(SWAPI_BASE_URL + "people/")
    data = response.json()
    
    for personaje in data['results']:
        nombre = personaje['name']
        planeta_url = personaje['homeworld']
        personajes.append({"nombre": nombre, "planeta_url": planeta_url})

    # Obtener datos de planetas
    response = requests.get(SWAPI_BASE_URL + "planets/")
    data = response.json()
    
    for planeta in data['results']:
        nombre = planeta['name']
        url = planeta['url']
        planetas[url] = nombre
    
    return personajes, planetas

# Función para consultar al oráculo sobre el lado de la fuerza de un personaje
def obtener_afiliacion_oraculo(nombre_personaje):
    response = requests.get(BASE_URL + "oracle-rolodex", headers=HEADERS, params={'name': nombre_personaje})
    
    if response.status_code == 200:
        data = response.json()
        oracle_notes = data.get("oracle_notes", "").lower()
        
        # Decodificar la afiliación del personaje según oracle_notes
        if "luminoso" in oracle_notes:
            return "luminoso"
        elif "oscuro" in oracle_notes:
            return "oscuro"
        else:
            return None  # Afiliación no especificada en los notas del oráculo
    else:
        print(f"Error al consultar el oráculo para {nombre_personaje}: {response.status_code}")
        return None

# Cálculo del IBF para los planetas
def calcular_ibf(planetas, personajes):
    planetas_ibf = {}

    # Organizar personajes por planeta
    for personaje in personajes:
        planeta_url = personaje['planeta_url']
        nombre = personaje['nombre']
        
        afiliacion = obtener_afiliacion_oraculo(nombre)
        
        # Contar afiliaciones para cada planeta
        if planeta_url not in planetas_ibf:
            planetas_ibf[planeta_url] = {'luminoso': 0, 'oscuro': 0, 'total': 0}
        
        if afiliacion == 'luminoso':
            planetas_ibf[planeta_url]['luminoso'] += 1
        elif afiliacion == 'oscuro':
            planetas_ibf[planeta_url]['oscuro'] += 1
        
        planetas_ibf[planeta_url]['total'] += 1
    
    # Calcular IBF y encontrar el planeta con equilibrio (IBF cercano a 0)
    planeta_equilibrado = None
    ibf_mas_cercano = 1  # IBF más cercano a cero

    for planeta_url, conteo in planetas_ibf.items():
        if conteo['total'] > 0:
            ibf = (conteo['luminoso'] - conteo['oscuro']) / conteo['total']
            if abs(ibf) < abs(ibf_mas_cercano):
                ibf_mas_cercano = ibf
                planeta_equilibrado = planeta_url

    return planetas.get(planeta_equilibrado)

# Envío de la solución
def enviar_solucion(planeta_equilibrado):
    solution_url = "https://makers-challenge.altscore.ai/v1/s1/e3/solution"
    data = {"planet": planeta_equilibrado}
    response = requests.post(solution_url, headers=HEADERS, json=data)
    if response.status_code == 200:
        print("Solución enviada correctamente. Respuesta:", response.json())
    else:
        print(f"Error al enviar la solución: {response.status_code}", response.json())
        print("Encabezados de la respuesta:", response.headers)

# Ejecución del flujo principal
personajes, planetas = obtener_datos_star_wars()
planeta_equilibrado = calcular_ibf(planetas, personajes)
if planeta_equilibrado:
    enviar_solucion(planeta_equilibrado)
else:
    print("No se encontró un planeta con equilibrio en la Fuerza.")

