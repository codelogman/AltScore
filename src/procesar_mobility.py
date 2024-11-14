# procesar_mobility.py

import pandas as pd
import h3
from fastparquet import ParquetFile
from collections import defaultdict

def procesar_mobility_en_bloques(ruta_mobility, tamano_bloque=100000):
    # Inicializar contadores para densidad de movilidad y tiempo de permanencia
    densidad_mobility = defaultdict(int)
    tiempo_permanencia = defaultdict(list)

    # Usar fastparquet para cargar el archivo en bloques
    pf = ParquetFile(ruta_mobility)
    
    for chunk in pf.iter_row_groups(columns=['device_id', 'lat', 'lon', 'timestamp']):
        # Convertir coordenadas a índice H3 (sin especificar 'resolution')
        chunk['hex_id'] = chunk.apply(lambda row: h3.latlng_to_cell(row['lat'], row['lon'], 9), axis=1)
        
        # Calcular densidad de movilidad (dispositivos únicos por hexágono)
        densidad_por_hex = chunk.groupby('hex_id')['device_id'].nunique()
        for hex_id, densidad in densidad_por_hex.items():
            densidad_mobility[hex_id] += densidad

        # Calcular tiempo de permanencia en hexágonos
        chunk = chunk.sort_values(by=['device_id', 'timestamp'])
        chunk['time_diff'] = chunk.groupby('device_id')['timestamp'].diff()
        chunk['same_hex'] = chunk['hex_id'] == chunk.groupby('device_id')['hex_id'].shift()
        tiempos_por_hex = chunk[chunk['same_hex']].groupby('hex_id')['time_diff'].mean()
        
        for hex_id, tiempo in tiempos_por_hex.items():
            tiempo_permanencia[hex_id].append(tiempo)

    # Promediar el tiempo de permanencia
    tiempo_permanencia_promedio = {hex_id: sum(tiempos) / len(tiempos) for hex_id, tiempos in tiempo_permanencia.items()}

    # Convertir resultados a DataFrames
    df_densidad = pd.DataFrame(list(densidad_mobility.items()), columns=['hex_id', 'mobility_density'])
    df_tiempo = pd.DataFrame(list(tiempo_permanencia_promedio.items()), columns=['hex_id', 'avg_time_in_hex'])

    # Unir resultados en un solo DataFrame
    df_features = pd.merge(df_densidad, df_tiempo, on='hex_id', how='outer')
    return df_features

if __name__ == "__main__":
    ruta_mobility = './data/mobility_data.parquet'
    features_mobility = procesar_mobility_en_bloques(ruta_mobility)
    print("Características de movilidad calculadas:\n", features_mobility.head())
    # Guardar las características de movilidad en un archivo CSV para su posterior uso
    features_mobility.to_csv('./data/features_mobility.csv', index=False)

