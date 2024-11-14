# generar_predicciones_finales.py

import pandas as pd

def generar_predicciones(ruta_test, ruta_salida, modelo):
    # Cargar el conjunto de datos de prueba enriquecido
    test_data = pd.read_csv(ruta_test)
    
    # Separar características (X) de prueba, excluyendo 'hex_id' y 'cost_of_living'
    X_test = test_data.drop(columns=['hex_id', 'cost_of_living'])
    
    # Imputar cualquier valor faltante en X_test con 0 (en caso de que queden algunos)
    X_test['mobility_density'].fillna(0, inplace=True)
    X_test['avg_time_in_hex'].fillna(0, inplace=True)
    
    # Generar predicciones
    test_data['cost_of_living'] = modelo.predict(X_test)
    
    # Guardar el archivo de salida con las predicciones
    test_data[['hex_id', 'cost_of_living']].to_csv(ruta_salida, index=False)
    print("Predicciones finales generadas y guardadas en:", ruta_salida)

if __name__ == "__main__":
    # Importar el modelo entrenado y ajustado
    from ajustar_modelo_gbr import ajustar_hyperparametros_gbr
    ruta_train = './data/train_enriched.csv'
    mejor_modelo = ajustar_hyperparametros_gbr(ruta_train)
    
    # Generar predicciones para el conjunto de prueba y guardarlas en 'submission.csv'
    ruta_test = './data/test_enriched.csv'
    ruta_salida = './data/submission.csv'
    generar_predicciones(ruta_test, ruta_salida, mejor_modelo)

