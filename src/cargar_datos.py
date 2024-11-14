# cargar_datos.py

import pandas as pd

def cargar_datos():
    # Cargar archivos CSV
    train_data = pd.read_csv('./data/train.csv')
    test_data = pd.read_csv('./data/test.csv')
    
    # Cargar una muestra de 100,000 filas de mobility_data
    mobility_data = pd.read_parquet('./data/mobility_data.parquet', engine='pyarrow', columns=None).sample(100000)
    
    # Verificar las primeras filas de cada archivo
    print("Train Data Head:\n", train_data.head())
    print("\nTest Data Head:\n", test_data.head())
    print("\nMobility Data Head:\n", mobility_data.head())

    return train_data, test_data, mobility_data

if __name__ == "__main__":
    train_data, test_data, mobility_data = cargar_datos()

