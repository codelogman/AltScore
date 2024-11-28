#generar_climate.py

import pandas as pd
import numpy as np

def generar_climate_data(ruta_features, ruta_climate_output):
    # Cargar características de movilidad
    features_mobility = pd.read_csv(ruta_features)

    # Generar datos climáticos simulados asociados a cada hex_id
    np.random.seed(42)
    climate_data = pd.DataFrame({
        'hex_id': features_mobility['hex_id'],
        'avg_temperature': np.random.uniform(15, 35, size=len(features_mobility)),
        'rainfall_mm': np.random.uniform(0, 300, size=len(features_mobility)),
        'sunshine_hours': np.random.uniform(1500, 3000, size=len(features_mobility))
    })

    # Guardar el archivo generado
    climate_data.to_csv(ruta_climate_output, index=False)
    print(f"Archivo {ruta_climate_output} generado con datos climáticos simulados.")

if __name__ == "__main__":
    ruta_features = './data/features_mobility.csv'
    ruta_climate_output = './data/climate_data.csv'
    generar_climate_data(ruta_features, ruta_climate_output)

