import requests
import time
# Configuración de la API
API_URL = "https://makers-challenge.altscore.ai/v1/s1/e5/actions/"
API_KEY = '4c2212c16e7a4570aa9652b3ffa82681'
HEADERS = {
    'accept': 'application/json',
    'API-KEY': API_KEY,
    'Content-Type': 'application/json'
}

# Última posición registrada (de la bitácora)
def parse_radar_data(data):
    grid = []
    rows = data.split('|')
    for row in rows:
        grid.append([row[i:i+2] for i in range(0, len(row), 2)])
    return grid

def analizar_posiciones():
    radar_data = "a01b01c01d01e01f01g01h01|a02b02c02d02e$2f02g02h02|a03b03c03d03e03f03g03h$3|a04b04c04d04e04f04g04h04|a05b05c05d05e$5f05g^5h05|a06b06c06d06e$6f06g06h06|a07b07c07d07e07f07g07h07|a08b08c08d08e08f#8g08h08|"
    grid = parse_radar_data(radar_data)
    enemy_pos = None
    target_pos = None
    obstacles = []

    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if cell == "^5":
                enemy_pos = (i, j)
            elif cell == "#8":
                target_pos = (i, j)
            elif "$" in cell:
                obstacles.append((i, j))
    return enemy_pos, target_pos, obstacles

# Iniciar la misión
def iniciar_mision():
    response = requests.post(API_URL + "start", headers=HEADERS)
    if response.status_code == 200:
        print("Misión iniciada:", response.json())
    else:
        print("Error al iniciar la misión:", response.status_code, response.json())
        return False
    return True

# Realizar turno de radar o ataque
def realizar_turno(action, x=None, y=None):
    data = {"action": action}
    if action == "attack":
        data["attack_position"] = {"x": x, "y": y}
    
    response = requests.post(API_URL + "perform-turn", headers=HEADERS, json=data)
    if response.status_code == 200:
        resultado = response.json()
        print(f"Acción '{action}' realizada:", resultado)
        return resultado
    else:
        print(f"Error en la acción '{action}':", response.status_code, response.json())
        return None

# Predicción de movimiento con consideración de obstáculos
def predecir_movimiento(pos_actual, pos_objetivo, obstacles):
    x, y = pos_actual
    target_x, target_y = pos_objetivo
    
    # Movimiento directo hacia el objetivo evitando obstáculos
    if x < target_x and (x+1, y) not in obstacles:
        x += 1
    elif x > target_x and (x-1, y) not in obstacles:
        x -= 1
    if y < target_y and (x, y+1) not in obstacles:
        y += 1
    elif y > target_y and (x, y-1) not in obstacles:
        y -= 1

    return x, y

# Ejecución de la misión
if iniciar_mision():
#if True:
    enemy_pos, target_pos, obstacles = analizar_posiciones()
    print(f"Posición inicial del enemigo: {enemy_pos}")
    print(f"Posición objetivo (Hope): {target_pos}")
    print(f"Obstáculos: {obstacles}")

    # Realizar tres lecturas de radar para confirmar la predicción
    for turno in range(3):
        resultado_radar = realizar_turno("radar")
        if not resultado_radar:
            print("Error en el radar, intentando nuevamente...")
            continue

        # Ajustar posición del enemigo
        enemy_pos = predecir_movimiento(enemy_pos, target_pos, obstacles)
        print(f"Predicción de la posición del enemigo en turno {turno + 1}: {enemy_pos}")
        time.sleep(1)

    # Preparar y realizar el ataque en el cuarto turno
    x_coordenada = chr(ord('a') + enemy_pos[0])
    y_coordenada = enemy_pos[1] + 1
    print(f"Intentando ataque en posición: {x_coordenada}{y_coordenada}")
    
    resultado_ataque = realizar_turno("attack", x=x_coordenada, y=y_coordenada)
    
    if resultado_ataque and resultado_ataque.get("action_result") == "hit":
        print("¡Impacto exitoso en la nave enemiga!")
    else:
        print("El ataque falló o el enemigo no estaba en la posición esperada.")
else:
    print("Misión no iniciada, verifique el código y la conexión.")

