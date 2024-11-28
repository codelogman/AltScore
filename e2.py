import requests
import time
import math

API_KEY = '4c2212c16e7a4570aa9652b3ffa82681'
BASE_URL = "https://makers-challenge.altscore.ai/v1/s1/e2/resources/stars"

# Función para obtener datos y encabezados de una página específica
def obtener_datos_estrellas(page):
    headers = {'API-KEY': API_KEY}
    params = {'page': page, 'sort-by': 'id', 'sort-direction': 'desc'}
    response = requests.get(BASE_URL, headers=headers, params=params)
    x_total_count = int(response.headers.get('x-total-count', 0))
    
    try:
        data = response.json()
        return data, x_total_count
    except ValueError:
        print("Error al procesar la respuesta JSON en la página", page)
        return None, x_total_count

# Función para calcular la resonancia promedio
def calcular_resonancia_promedio():
    resonancias = []
    page = 1
    total_estrellas = None

    while True:
        datos_estrellas, x_total_count = obtener_datos_estrellas(page)

        if total_estrellas is None:
            total_estrellas = x_total_count
            total_pages = math.ceil(total_estrellas / 3)

        # Si los datos no están disponibles, detenemos el proceso
        if datos_estrellas is None:
            print("No se pudieron obtener datos en la página", page)
            break

        # Extraer y acumular las resonancias
        for estrella in datos_estrellas:
            if isinstance(estrella.get('resonance'), int):
                resonancias.append(estrella['resonance'])

        print(f"Datos de estrellas obtenidos en página {page}: {datos_estrellas}")

        # Revisar si hemos alcanzado la última página
        if page >= total_pages:
            break

        page += 1
        time.sleep(1)

    # Calcular la resonancia promedio
    if resonancias:
        resonancia_promedio = round(sum(resonancias) / len(resonancias))
    else:
        resonancia_promedio = 0

    return resonancia_promedio

# Enviar la solución
def enviar_solucion(resonancia_promedio):
    solution_url = "https://makers-challenge.altscore.ai/v1/s1/e2/solution"
    headers = {'API-KEY': API_KEY}
    data = {"average_resonance": resonancia_promedio}
    response = requests.post(solution_url, headers=headers, json=data)
    print("Solución enviada con éxito. Respuesta:", response.json())

# Ejecución
resonancia_promedio = calcular_resonancia_promedio()
if resonancia_promedio:
    enviar_solucion(resonancia_promedio)
else:
    print("No se pudo calcular una resonancia promedio válida.")

