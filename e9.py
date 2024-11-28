from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# Datos de los puntos críticos y de la curva de saturación
critical_pressure = 10  # MPa
critical_volume = 0.0035  # m³/kg
liquid_start_pressure = 0.05  # MPa
liquid_start_volume = 0.00105  # m³/kg
vapor_start_pressure = 0.05  # MPa
vapor_start_volume = 30.0  # m³/kg

class PhaseChangeResponse(BaseModel):
    specific_volume_liquid: float
    specific_volume_vapor: float

def interpolate(value: float, start: float, end: float, start_value: float, end_value: float) -> float:
    """Interpolate between two points."""
    return start_value + (value - start) * (end_value - start_value) / (end - start)

@app.get("/phase-change-diagram", response_model=PhaseChangeResponse)
async def get_phase_change_diagram(pressure: Optional[float] = None):
    if pressure is None:
        raise HTTPException(status_code=400, detail="Pressure parameter is required.")
    if pressure < liquid_start_pressure or pressure > critical_pressure:
        raise HTTPException(status_code=400, detail="Pressure out of range for phase change curve.")
    
    # Interpolación para el volumen específico de líquido
    specific_volume_liquid = interpolate(
        pressure,
        liquid_start_pressure,
        critical_pressure,
        liquid_start_volume,
        critical_volume
    )
    
    # Interpolación para el volumen específico de vapor
    specific_volume_vapor = interpolate(
        pressure,
        vapor_start_pressure,
        critical_pressure,
        vapor_start_volume,
        critical_volume
    )
    
    return PhaseChangeResponse(
        specific_volume_liquid=specific_volume_liquid,
        specific_volume_vapor=specific_volume_vapor
    )

