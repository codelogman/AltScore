# ajustar_modelo_gbr.py

import pandas as pd
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error
import numpy as np

def ajustar_hyperparametros_gbr(ruta_train):
    # Cargar el conjunto de datos de entrenamiento enriquecido
    train_data = pd.read_csv(ruta_train)
    
    # Separar características (X) y variable objetivo (y)
    X = train_data.drop(columns=['hex_id', 'cost_of_living'])  # Excluir hex_id y cost_of_living de X
    y = train_data['cost_of_living']
    
    # Dividir en conjuntos de entrenamiento y validación
    X_train, X_valid, y_train, y_valid = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Imputar valores faltantes en las columnas específicas con 0
    X_train['mobility_density'].fillna(0, inplace=True)
    X_train['avg_time_in_hex'].fillna(0, inplace=True)
    X_valid['mobility_density'].fillna(0, inplace=True)
    X_valid['avg_time_in_hex'].fillna(0, inplace=True)

    # Definir el modelo y los parámetros para la búsqueda aleatoria
    gbr = GradientBoostingRegressor(random_state=42)
    param_dist = {
        'n_estimators': [50, 100, 200],
        'max_depth': [3, 5, 7],
        'learning_rate': [0.01, 0.05, 0.1],
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [1, 2, 4]
    }
    
    # Realizar la búsqueda aleatoria
    random_search = RandomizedSearchCV(
        gbr, param_distributions=param_dist, n_iter=10,
        scoring='neg_root_mean_squared_error', cv=3, random_state=42, n_jobs=-1
    )
    random_search.fit(X_train, y_train)

    # Mejor modelo y evaluación
    best_gbr = random_search.best_estimator_
    y_pred_best = best_gbr.predict(X_valid)
    rmse_best = np.sqrt(mean_squared_error(y_valid, y_pred_best))
    print(f"Mejores hiperparámetros encontrados: {random_search.best_params_}")
    print(f"RMSE del mejor modelo en el conjunto de validación: {rmse_best}")
    
    return best_gbr

if __name__ == "__main__":
    ruta_train = './data/train_enriched.csv'
    mejor_modelo = ajustar_hyperparametros_gbr(ruta_train)

