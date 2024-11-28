from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse

import random

app = FastAPI()

# Diccionario con los sistemas y sus respectivos códigos
systems_codes = {
    "navigation": "NAV-01",
    "communications": "COM-02",
    "life_support": "LIFE-03",
    "engines": "ENG-04",
    "deflector_shield": "SHLD-05"
}

# Variable global para almacenar el sistema dañado
damaged_system = None

# Simulamos un sistema dañado al azar para la llamada GET /status
@app.get("/status")
async def get_status():
    global damaged_system
    if damaged_system is None:
        damaged_system = random.choice(list(systems_codes.keys()))
    return {"damaged_system": damaged_system}

# Genera la página HTML con el código correspondiente al sistema dañado
@app.get("/repair-bay", response_class=HTMLResponse)
async def get_repair_bay():
    global damaged_system
    if damaged_system is None:
        raise HTTPException(status_code=400, detail="Status not set yet. Call /status first.")
    code = systems_codes[damaged_system]

    # Creamos la respuesta HTML con el código del sistema dañado
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Repair</title>
    </head>
    <body>
        <div class="anchor-point">{code}</div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

# Responde con el código de estado HTTP 418
@app.post("/teapot")
async def post_teapot():
    raise HTTPException(status_code=418, detail="I'm a teapot")

