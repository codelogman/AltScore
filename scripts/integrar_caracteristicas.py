# integrar_caracteristicas.py
import pandas as pd
from sklearn.impute import KNNImputer

def integrar_caracteristicas(ruta_train, ruta_test, ruta_features, ruta_salida_train, ruta_salida_test):
    # Cargar los datos de entrenamiento y prueba
    print("Cargando datos de entrenamiento y prueba...")
    train_data = pd.read_csv(ruta_train)
    test_data = pd.read_csv(ruta_test)
    
    # Cargar las características de movilidad y climáticas
    print("Cargando características de movilidad y climáticas...")
    features_mobility = pd.read_csv(ruta_features)
    
    # Unir las características con los datos de entrenamiento y prueba usando 'hex_id'
    print("Uniendo características con datos de entrenamiento y prueba...")
    train_data = train_data.merge(features_mobility, on='hex_id', how='left')
    test_data = test_data.merge(features_mobility, on='hex_id', how='left')
    
    # Diagnóstico de valores faltantes
    print("Valores NaN en datos de entrenamiento después de la unión:")
    print(train_data.isnull().sum())
    print("Valores NaN en datos de prueba después de la unión:")
    print(test_data.isnull().sum())
    
    # Imputar valores faltantes con KNNImputer
    print("Imputando valores faltantes con KNNImputer...")
    imputer = KNNImputer(n_neighbors=5, weights="uniform")
    
    # Seleccionar columnas numéricas para imputar
    cols_to_impute = train_data.select_dtypes(include=['float64', 'int64']).columns
    train_data[cols_to_impute] = imputer.fit_transform(train_data[cols_to_impute])
    test_data[cols_to_impute] = imputer.transform(test_data[cols_to_impute])
    
    # Guardar los datos enriquecidos en nuevos archivos CSV
    print(f"Guardando datos enriquecidos en {ruta_salida_train} y {ruta_salida_test}...")
    train_data.to_csv(ruta_salida_train, index=False)
    test_data.to_csv(ruta_salida_test, index=False)
    print("Características integradas y guardadas exitosamente.")

if __name__ == "__main__":
    ruta_train = './data/train.csv'
    ruta_test = './data/test.csv'
    ruta_features = './data/features_mobility_climatic.csv'
    ruta_salida_train = './data/train_enriched.csv'
    ruta_salida_test = './data/test_enriched.csv'
    
    integrar_caracteristicas(ruta_train, ruta_test, ruta_features, ruta_salida_train, ruta_salida_test)

