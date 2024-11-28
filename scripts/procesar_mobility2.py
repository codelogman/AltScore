# procesar_mobility2.py

from sklearn.impute import KNNImputer
import pandas as pd
import h3
from fastparquet import ParquetFile
from collections import defaultdict
from tqdm import tqdm

def procesar_mobility_completo(ruta_mobility, resolucion_inicial=9, resolucion_reducida=None):
    # Inicializar contadores para densidad de movilidad, tiempo de permanencia, y métricas adicionales
    densidad_mobility = defaultdict(int)
    tiempo_permanencia = defaultdict(list)
    tiempo_permanencia_varianza = defaultdict(list)
    frecuencia_visitas = defaultdict(lambda: defaultdict(int))

    # Usar fastparquet para procesar el archivo en bloques
    pf = ParquetFile(ruta_mobility)
    total_bloques = len(pf.row_groups)  # Obtener número total de bloques para la barra de progreso

    # Procesar cada bloque con una barra de progreso
    for chunk in tqdm(pf.iter_row_groups(columns=['device_id', 'lat', 'lon', 'timestamp']), total=total_bloques, desc="Procesando bloques"):
        # Convertir coordenadas a índice H3
        chunk['hex_id'] = chunk.apply(lambda row: h3.latlng_to_cell(row['lat'], row['lon'], resolucion_inicial), axis=1)

        # Reducir resolución de hexágonos si se especifica
        if resolucion_reducida:
            chunk['hex_id'] = chunk['hex_id'].apply(lambda x: h3.cell_to_parent(x, resolucion_reducida))

        # Calcular densidad de movilidad (dispositivos únicos por hexágono)
        densidad_por_hex = chunk.groupby('hex_id')['device_id'].nunique()
        for hex_id, densidad in densidad_por_hex.items():
            densidad_mobility[hex_id] += densidad

        # Calcular tiempo de permanencia en hexágonos
        chunk = chunk.sort_values(by=['device_id', 'timestamp'])
        chunk['time_diff'] = chunk.groupby('device_id')['timestamp'].diff()
        chunk['same_hex'] = chunk['hex_id'] == chunk.groupby('device_id')['hex_id'].shift()
        tiempos_por_hex = chunk[chunk['same_hex']].groupby('hex_id')['time_diff'].mean()
        tiempos_varianza_por_hex = chunk[chunk['same_hex']].groupby('hex_id')['time_diff'].var()

        for hex_id, tiempo in tiempos_por_hex.items():
            tiempo_permanencia[hex_id].append(tiempo)

        for hex_id, varianza in tiempos_varianza_por_hex.items():
            tiempo_permanencia_varianza[hex_id].append(varianza)

        # Calcular frecuencia de visitas por dispositivo
        visitas_por_hex = chunk.groupby(['hex_id', 'device_id']).size()
        for (hex_id, device_id), visitas in visitas_por_hex.items():
            frecuencia_visitas[hex_id][device_id] += visitas

    # Promediar el tiempo de permanencia y varianza
    tiempo_permanencia_promedio = {hex_id: sum(tiempos) / len(tiempos) for hex_id, tiempos in tiempo_permanencia.items()}
    tiempo_permanencia_varianza_promedio = {hex_id: sum(varianzas) / len(varianzas) for hex_id, varianzas in tiempo_permanencia_varianza.items()}

    # Calcular la frecuencia media de visitas por hexágono
    frecuencia_visitas_media = {hex_id: sum(visitas.values()) / len(visitas) for hex_id, visitas in frecuencia_visitas.items()}

    # Convertir resultados a DataFrames
    df_densidad = pd.DataFrame(list(densidad_mobility.items()), columns=['hex_id', 'mobility_density'])
    df_tiempo = pd.DataFrame(list(tiempo_permanencia_promedio.items()), columns=['hex_id', 'avg_time_in_hex'])
    df_varianza = pd.DataFrame(list(tiempo_permanencia_varianza_promedio.items()), columns=['hex_id', 'time_in_hex_variance'])
    df_frecuencia = pd.DataFrame(list(frecuencia_visitas_media.items()), columns=['hex_id', 'avg_visits_per_device'])

    # Unir resultados en un solo DataFrame
    df_features = df_densidad.merge(df_tiempo, on='hex_id', how='outer')\
                              .merge(df_varianza, on='hex_id', how='outer')\
                              .merge(df_frecuencia, on='hex_id', how='outer')

    # Imputación de valores faltantes con KNN Imputer
    imputer = KNNImputer(n_neighbors=5)
    df_features.iloc[:, 1:] = imputer.fit_transform(df_features.iloc[:, 1:])

    return df_features

if __name__ == "__main__":
    ruta_mobility = './data/mobility_data.parquet'
    # Ajustar resolución inicial y reducida
    resolucion_inicial = 9
    resolucion_reducida = 8  # Cambiar a None si no deseas reducir
    features_mobility = procesar_mobility_completo(ruta_mobility, resolucion_inicial, resolucion_reducida)
    print("Características de movilidad calculadas:\n", features_mobility.head())
    # Guardar las características de movilidad en un archivo CSV para su posterior uso
    features_mobility.to_csv('./data/features_mobility.csv', index=False)

