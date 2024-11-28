# entrenar_modelo2.py

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import ParameterGrid
import numpy as np
import lightgbm as lgb
from tqdm import tqdm
import warnings

# Suprimir warnings globales
warnings.filterwarnings("ignore")

def entrenar_y_optimizar_lightgbm_tqdm(ruta_train):
    print("Cargando datos...")
    train_data = pd.read_csv(ruta_train)

    print("Separando características y etiquetas...")
    X = train_data.drop(columns=['hex_id', 'cost_of_living'])
    y = train_data['cost_of_living']

    print("Normalizando características...")
    features_to_normalize = [
        'mobility_density', 'avg_time_in_hex', 'avg_temperature', 
        'rainfall_mm', 'sunshine_hours', 'time_in_hex_variance', 
        'avg_visits_per_device'
    ]
    scaler = StandardScaler()
    X[features_to_normalize] = scaler.fit_transform(X[features_to_normalize])

    print("Diagnóstico: valores NaN después de la normalización:")
    print(X.isnull().sum())

    print("Dividiendo datos en entrenamiento y validación (60% validación)...")
    X_train, X_valid, y_train, y_valid = train_test_split(X, y, test_size=0.6, random_state=42)

    print("Inicializando modelo LightGBM...")
    model = lgb.LGBMRegressor(
        boosting_type='gbdt', 
        objective='regression', 
        random_state=42, 
        n_jobs=-1, 
        min_split_gain=0.01, 
        verbosity=-1  # Silenciar los warnings
    )

    param_dist = {
        'num_leaves': [15, 31, 50, 75],           
        'max_depth': [5, 10, 15, 20, 25],         
        'learning_rate': [0.005, 0.01, 0.02, 0.03],  
        'n_estimators': [100, 200, 300, 500],     
        'subsample': [0.6, 0.7, 0.8, 0.9],       
        'colsample_bytree': [0.7, 0.8, 0.9, 1.0], 
        'reg_alpha': [0, 0.05, 0.1, 0.2],         
        'reg_lambda': [0.01, 0.05, 0.1, 0.2]      
    }

    param_grid = list(ParameterGrid(param_dist))[:30000]  # Limitar a 30000 combinaciones
    print(f"Total de combinaciones: {len(param_grid)}")

    best_score = float("inf")
    best_params = None

    print("Optimizando hiperparámetros...")
    for params in tqdm(param_grid, desc="Evaluando combinaciones", total=len(param_grid)):
        model.set_params(**params)
        model.fit(
            X_train, y_train,
            eval_set=[(X_valid, y_valid)],
            eval_metric='rmse',
            callbacks=[lgb.early_stopping(stopping_rounds=50, verbose=False)]  # Silenciar logs por iteración
        )

        y_pred = model.predict(X_valid)
        rmse = np.sqrt(mean_squared_error(y_valid, y_pred))

        if rmse < best_score:
            best_score = rmse
            best_params = params

    print("\nMejores hiperparámetros:", best_params)
    print(f"Mejor RMSE en validación: {best_score:.6f}")

    print("Entrenando modelo final con los mejores parámetros...")

    best_model = lgb.LGBMRegressor(
        **best_params,
        min_split_gain=0.01,
        random_state=42,
        n_jobs=-1,
        verbosity=-1
    )
    
    best_model.fit(
        X_train, y_train,
        eval_set=[(X_valid, y_valid)],
        eval_metric='rmse',
        callbacks=[lgb.early_stopping(stopping_rounds=100, verbose=False)]  # Más paciencia
    )

    print("Guardando metricas y características...")
    y_pred = best_model.predict(X_valid)
    rmse = np.sqrt(mean_squared_error(y_valid, y_pred))

    with open('./data/metrics_lightgbm_tqdm.txt', 'w') as f:
        f.write(f"Mejores Hiperparámetros: {best_params}\n")
        f.write(f"Mejor RMSE promedio en validación cruzada: {best_score:.6f}\n")
        f.write(f"RMSE en conjunto de validación: {rmse:.6f}\n")

    importances = best_model.feature_importances_
    feature_names = X.columns
    importancia_df = pd.DataFrame({'feature': feature_names, 'importance': importances}).sort_values(by='importance', ascending=False)
    importancia_df.to_csv('./data/feature_importance_lightgbm_tqdm.csv', index=False)

    return best_model


if __name__ == "__main__":
    ruta_train = './data/train_enriched.csv'
    modelo_lightgbm = entrenar_y_optimizar_lightgbm_tqdm(ruta_train)

