# integrar_caracteristicas.py

import pandas as pd

def integrar_caracteristicas(ruta_train, ruta_test, ruta_features, ruta_salida_train, ruta_salida_test):
    # Cargar los datos de entrenamiento y prueba
    train_data = pd.read_csv(ruta_train)
    test_data = pd.read_csv(ruta_test)
    
    # Cargar las características de movilidad
    features_mobility = pd.read_csv(ruta_features)
    
    # Unir las características con los datos de entrenamiento y prueba usando 'hex_id'
    train_data = train_data.merge(features_mobility, on='hex_id', how='left')
    test_data = test_data.merge(features_mobility, on='hex_id', how='left')
    
    # Imputar valores faltantes en las nuevas características con la media
    train_data['mobility_density'].fillna(train_data['mobility_density'].mean(), inplace=True)
    train_data['avg_time_in_hex'].fillna(train_data['avg_time_in_hex'].mean(), inplace=True)
    test_data['mobility_density'].fillna(test_data['mobility_density'].mean(), inplace=True)
    test_data['avg_time_in_hex'].fillna(test_data['avg_time_in_hex'].mean(), inplace=True)
    
    # Guardar los datos enriquecidos en nuevos archivos CSV
    train_data.to_csv(ruta_salida_train, index=False)
    test_data.to_csv(ruta_salida_test, index=False)
    print("Características integradas y guardadas en los archivos de salida.")

if __name__ == "__main__":
    ruta_train = './data/train.csv'
    ruta_test = './data/test.csv'
    ruta_features = './data/features_mobility.csv'
    ruta_salida_train = './data/train_enriched.csv'
    ruta_salida_test = './data/test_enriched.csv'
    
    integrar_caracteristicas(ruta_train, ruta_test, ruta_features, ruta_salida_train, ruta_salida_test)

