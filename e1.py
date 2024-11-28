import requests
import time as t

# API-KEY para autenticación
api_key = "4c2212c16e7a4570aa9652b3ffa82681"

# Configuración de la URL y el encabezado de autenticación
get_url = 'https://makers-challenge.altscore.ai/v1/s1/e1/resources/measurement'
post_url = 'https://makers-challenge.altscore.ai/v1/s1/e1/solution'
headers = {
    "API-KEY": api_key
}

# Funciones de conversión de unidades
def convert_distance(distance, unit):
    if unit == "AU":
        return distance  # AU como estándar
    elif unit == "km":
        return distance / 149597870.7  # 1 AU = 149,597,870.7 km
    else:
        raise ValueError(f"Unidad de distancia desconocida: {unit}")

def convert_time(time, unit):
    if unit == "hours":
        return time  # hours como estándar
    elif unit == "minutes":
        return time / 60  # 1 hour = 60 minutes
    elif unit == "seconds":
        return time / 3600  # 1 hour = 3600 seconds
    else:
        raise ValueError(f"Unidad de tiempo desconocida: {unit}")

# Función para obtener una medición válida
def get_measurement():
    while True:
        response = requests.get(get_url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            print("Datos obtenidos:", data)  # Mostrar datos obtenidos para depuración
            
            distance_str = data.get('distance', "")
            time_str = data.get('time', "")
            
            if "failed to measure" not in distance_str and "failed to measure" not in time_str:
                try:
                    # Separar el valor y la unidad para cada medición
                    distance_value, distance_unit = distance_str.split()[0], distance_str.split()[1]
                    time_value, time_unit = time_str.split()[0], time_str.split()[1]
                    
                    # Convertir valores a float y convertir a unidades estándar
                    distance = convert_distance(float(distance_value), distance_unit)
                    time_observed = convert_time(float(time_value), time_unit)
                    
                    if time_observed > 0:
                        return distance, time_observed
                    else:
                        print("Error: El valor de 'time' es cero o negativo.")
                except ValueError as e:
                    print("Error:", e)
            else:
                print("Medición fallida, reintentando...")
        else:
            print("Error en la medición:", response.status_code)
            print("Detalle:", response.text)
        
        t.sleep(2)

# Función para calcular la velocidad redondeada al entero más cercano
def calculate_velocity(distance, time_observed):
    velocity = round(distance / time_observed)
    return velocity

# Función para enviar la solución
def send_solution(velocity):
    response = requests.post(post_url, json={'speed': velocity}, headers=headers)
    if response.status_code == 200:
        print("Solución enviada con éxito. Respuesta:", response.json())
    else:
        print("Error al enviar la solución:", response.status_code)
        print("Detalle:", response.text)

# Obtener una medición válida
distance, time_observed = get_measurement()

# Calcular la velocidad y enviar la solución
velocity = calculate_velocity(distance, time_observed)
send_solution(velocity)

