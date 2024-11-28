# generar_caracteristicas.py

import pandas as pd
import h3

def generar_caracteristicas_mobility(mobility_data):
    # Convertir coordenadas de latitud y longitud a índice H3
    mobility_data['h3_index'] = mobility_data.apply(
        lambda row: h3.latlng_to_cell(row['lat'], row['lon'], resolution=9), axis=1
    )

    # Calcular densidad de movilidad: cantidad de dispositivos únicos por hexágono
    mobility_density = mobility_data.groupby('h3_index')['device_id'].nunique().reset_index()
    mobility_density.columns = ['hex_id', 'mobility_density']

    # Calcular tiempo de permanencia promedio en cada hexágono
    mobility_data = mobility_data.sort_values(by=['device_id', 'timestamp'])
    mobility_data['time_diff'] = mobility_data.groupby('device_id')['timestamp'].diff()
    mobility_data['same_hex'] = mobility_data['h3_index'] == mobility_data.groupby('device_id')['h3_index'].shift()
    mobility_time_in_hex = mobility_data[mobility_data['same_hex']].groupby('h3_index')['time_diff'].mean().reset_index()
    mobility_time_in_hex.columns = ['hex_id', 'avg_time_in_hex']

    # Unir las características derivadas en un solo DataFrame
    features = pd.merge(mobility_density, mobility_time_in_hex, on='hex_id', how='outer')
    print("Características generadas de mobility_data:\n", features.head())

    return features

if __name__ == "__main__":
    # Asegurarse de cargar mobility_data de cargar_datos.py
    from cargar_datos import cargar_datos
    _, _, mobility_data = cargar_datos()
    
    features = generar_caracteristicas_mobility(mobility_data)

