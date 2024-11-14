import unittest
import pandas as pd
import os
from src.cargar_datos import cargar_datos
from src.procesar_mobility import procesar_mobility_en_bloques
from src.integrar_caracteristicas import integrar_caracteristicas
from src.entrenar_modelo import entrenar_y_evaluar_modelo
from src.ajustar_modelo_gbr import ajustar_hyperparametros_gbr
from src.generar_predicciones_finales import generar_predicciones

class TestChallenge(unittest.TestCase):

    def setUp(self):
        # Configurar rutas para pruebas
        self.ruta_train = './data/train.csv'
        self.ruta_test = './data/test.csv'
        self.ruta_mobility = './data/mobility_data.parquet'
        self.ruta_features_mobility = './data/features_mobility.csv'
        self.ruta_train_enriched = './data/train_enriched.csv'
        self.ruta_test_enriched = './data/test_enriched.csv'
        self.ruta_submission = './data/submission.csv'

    def test_cargar_datos(self):
        # Verificar que los datos de entrenamiento y prueba se cargan correctamente
        train_data, test_data = cargar_datos(self.ruta_train, self.ruta_test)
        self.assertFalse(train_data.empty, "El archivo de entrenamiento está vacío.")
        self.assertFalse(test_data.empty, "El archivo de prueba está vacío.")

    def test_procesar_mobility_en_bloques(self):
        # Probar que las características de movilidad se generan correctamente
        features_mobility = procesar_mobility_en_bloques(self.ruta_mobility)
        self.assertFalse(features_mobility.empty, "No se generaron características de movilidad.")
        self.assertIn('mobility_density', features_mobility.columns)
        self.assertIn('avg_time_in_hex', features_mobility.columns)

    def test_integrar_caracteristicas(self):
        # Probar que las características se integran correctamente
        integrar_caracteristicas(self.ruta_train, self.ruta_test, self.ruta_features_mobility,
                                 self.ruta_train_enriched, self.ruta_test_enriched)
        self.assertTrue(os.path.exists(self.ruta_train_enriched), "train_enriched.csv no fue creado.")
        self.assertTrue(os.path.exists(self.ruta_test_enriched), "test_enriched.csv no fue creado.")
        train_enriched = pd.read_csv(self.ruta_train_enriched)
        test_enriched = pd.read_csv(self.ruta_test_enriched)
        self.assertIn('mobility_density', train_enriched.columns)
        self.assertIn('avg_time_in_hex', test_enriched.columns)

    def test_entrenar_y_evaluar_modelo(self):
        # Probar que el modelo se entrena y evalúa sin errores
        rmse = entrenar_y_evaluar_modelo(self.ruta_train_enriched)
        self.assertGreater(rmse, 0, "RMSE debe ser un valor positivo.")
        self.assertLess(rmse, 1, "El RMSE es inesperadamente alto; podría haber un error.")

    def test_ajustar_hyperparametros_gbr(self):
        # Probar que los mejores hiperparámetros se ajustan correctamente
        modelo = ajustar_hyperparametros_gbr(self.ruta_train_enriched)
        self.assertIsNotNone(modelo, "No se ajustó ningún modelo.")
        self.assertGreater(modelo.n_estimators, 0, "n_estimators debería ser positivo.")
        self.assertGreater(modelo.learning_rate, 0, "learning_rate debería ser positivo.")

    def test_generar_predicciones(self):
        # Probar que el archivo de predicciones se genera correctamente
        generar_predicciones(self.ruta_test_enriched, self.ruta_submission)
        self.assertTrue(os.path.exists(self.ruta_submission), "El archivo de predicciones no fue creado.")
        submission_data = pd.read_csv(self.ruta_submission)
        self.assertEqual(len(submission_data), 511, "El archivo de predicciones debería tener 511 filas.")
        self.assertIn('hex_id', submission_data.columns)
        self.assertIn('cost_of_living', submission_data.columns)

if __name__ == '__main__':
    unittest.main()

