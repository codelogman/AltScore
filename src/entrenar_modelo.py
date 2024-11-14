# entrenar_modelo.py

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import numpy as np

def entrenar_y_evaluar_modelo(ruta_train):
    # Cargar el conjunto de datos de entrenamiento enriquecido
    train_data = pd.read_csv(ruta_train)
    
    # Separar características (X) y variable objetivo (y)
    X = train_data.drop(columns=['hex_id', 'cost_of_living'])  # Excluir hex_id y cost_of_living de X
    y = train_data['cost_of_living']
    
    # Dividir en conjuntos de entrenamiento y validación
    X_train, X_valid, y_train, y_valid = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Diagnóstico: Verificar columnas con valores NaN antes de la imputación
    print("Valores NaN en X_train antes de imputar:")
    print(X_train.isnull().sum()[X_train.isnull().sum() > 0])
    print("\nValores NaN en X_valid antes de imputar:")
    print(X_valid.isnull().sum()[X_valid.isnull().sum() > 0])

    # Imputar valores faltantes en las columnas específicas con 0
    X_train['mobility_density'].fillna(0, inplace=True)
    X_train['avg_time_in_hex'].fillna(0, inplace=True)
    X_valid['mobility_density'].fillna(0, inplace=True)
    X_valid['avg_time_in_hex'].fillna(0, inplace=True)
    
    # Verificar si aún quedan valores NaN después de la imputación
    print("\nValores NaN en X_train después de imputar:")
    print(X_train.isnull().sum()[X_train.isnull().sum() > 0])
    print("\nValores NaN en X_valid después de imputar:")
    print(X_valid.isnull().sum()[X_valid.isnull().sum() > 0])

    # Crear y entrenar el modelo solo si no hay valores NaN
    if X_train.isnull().sum().sum() == 0 and X_valid.isnull().sum().sum() == 0:
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        
        # Predecir en el conjunto de validación
        y_pred = model.predict(X_valid)
        
        # Calcular el error RMSE
        rmse = np.sqrt(mean_squared_error(y_valid, y_pred))
        print(f"Root Mean Squared Error (RMSE) en el conjunto de validación: {rmse}")
        return model
    else:
        print("Error: Aún existen valores NaN después de la imputación. Revisa los datos.")

if __name__ == "__main__":
    ruta_train = './data/train_enriched.csv'
    modelo = entrenar_y_evaluar_modelo(ruta_train)

