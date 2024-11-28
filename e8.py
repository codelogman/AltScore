import requests
import time
from datetime import datetime, timedelta

# Configuración de la URL base y API KEY
BASE_URL = "https://makers-challenge.altscore.ai/v1/s1/e8/actions/door"
API_KEY = "4c2212c16e7a4570aa9652b3ffa82681"
HEADERS = {
    'accept': 'application/json',
    'API-KEY': API_KEY
}

# Lista extensa de palabras a probar
sequence = ["expelliarmus", "reparo", "Altwarts", "expecto patronum", "accio", "lumos", 
            "nox", "wingardium leviosa", "protego", "aguamenti", "incendio", "alohomora", 
            "morsmordre", "riddikulus", "sectumsempra", "colloshoo", "expulso", 
            "piertotum locomotor"]

log_file_path = "door_attempts.log"

def log_message(word, log_time, message):
    """Guardar el intento en el archivo de log."""
    with open(log_file_path, "a") as log_file:
        log_file.write(f"Palabra: {word}, Tiempo: {log_time}, Mensaje: {message}\n")

def attempt_door(word):
    """Intento de abrir la puerta usando POST en el segundo exacto."""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    response = requests.post(BASE_URL, headers=HEADERS, json={"spell_word": word})
    
    if response.status_code == 200:
        message = response.json().get("response", "")
        print(f"¡Éxito! POST con la palabra: {word} en {current_time}")
        log_message(word, current_time, message)
        return True  # Indica éxito en la palabra actual
    else:
        hidden_message = response.json().get('hidden_message', 'Sin mensaje de error')
        print(f"Error {response.status_code} con POST {word}. Mensaje: {hidden_message}")
        log_message(word, current_time, hidden_message)
        return False  # Indica fallo

def attempt_revelio():
    """Prueba el hechizo Revelio para ver si revela algo."""
    response = requests.post(BASE_URL, headers=HEADERS, json={"spell_word": "Revelio"})
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if response.status_code == 200:
        message = response.json().get("response", "")
        print(f"Revelio reveló en {current_time}: {message}")
        log_message("Revelio", current_time, message)
    else:
        hidden_message = response.json().get('hidden_message', 'Sin mensaje de error')
        print(f"Error {response.status_code} con Revelio. Mensaje: {hidden_message}")
        log_message("Revelio", current_time, hidden_message)

def wait_until_next_minute():
    """Espera hasta el primer segundo del siguiente minuto."""
    now = datetime.now()
    next_minute = (now + timedelta(minutes=1)).replace(second=0, microsecond=0)
    time_to_wait = (next_minute - now).total_seconds()
    time.sleep(time_to_wait)

def continuous_sequence_with_revelio():
    """Intenta continuamente la secuencia con Revelio tras cada palabra."""
    while True:
        for word in sequence:
            # Espera al primer segundo del próximo minuto
            wait_until_next_minute()

            # Intenta la palabra en el segundo exacto
            success = attempt_door(word)
            
            # Intenta Revelio después de cada palabra exitosa
            if success:
                attempt_revelio()
            else:
                print(f"Error en la palabra {word}. Continuando con la siguiente palabra...")
        
        # Probar Revelio al final de la secuencia completa
        print("Intentando Revelio después de la secuencia completa...")
        attempt_revelio()

# Ejecuta el intento continuo de secuencia con Revelio
continuous_sequence_with_revelio()

