"""
Tests unitarios para el proyecto de clustering PYMEs
==================================================

Este módulo contiene tests para validar la funcionalidad
del sistema de clustering y predicción.
"""

import unittest
import pandas as pd
import numpy as np
import sys
import os

# Agregar el directorio del proyecto al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils import (
    validate_clustering_stability,
    calculate_business_metrics,
    detect_outliers_iqr,
    calculate_forecast_accuracy
)

class TestClusteringUtils(unittest.TestCase):
    """Tests para las utilidades de clustering."""
    
    def setUp(self):
        """Configuración inicial para los tests."""
        # Crear datos de prueba
        np.random.seed(42)
        self.test_data = pd.DataFrame({
            'ingresos_totales': np.random.normal(25000, 10000, 100),
            'numero_transacciones': np.random.poisson(25, 100),
            'ticket_promedio': np.random.normal(1000, 300, 100),
            'productos_unicos': np.random.poisson(15, 100),
            'periodo_actividad_dias': np.random.normal(750, 100, 100),
            'cluster_kmedoids': np.random.choice([0, 1, 2], 100)
        })
        
        # Asegurar valores positivos
        self.test_data['ingresos_totales'] = np.abs(self.test_data['ingresos_totales'])
        self.test_data['ticket_promedio'] = np.abs(self.test_data['ticket_promedio'])
        self.test_data['periodo_actividad_dias'] = np.abs(self.test_data['periodo_actividad_dias'])
    
    def test_calculate_business_metrics(self):
        """Test para el cálculo de métricas de negocio."""
        metrics = calculate_business_metrics(self.test_data)
        
        # Verificar que se calculen métricas para todos los clusters
        self.assertEqual(len(metrics), 3)
        
        # Verificar que cada cluster tenga las métricas esperadas
        for cluster_id in [0, 1, 2]:
            self.assertIn(cluster_id, metrics)
            self.assertIn('count', metrics[cluster_id])
            self.assertIn('revenue_mean', metrics[cluster_id])
            self.assertIn('efficiency_ratio', metrics[cluster_id])
            
            # Verificar que los valores sean positivos
            self.assertGreater(metrics[cluster_id]['revenue_mean'], 0)
            self.assertGreater(metrics[cluster_id]['count'], 0)
    
    def test_detect_outliers_iqr(self):
        """Test para detección de outliers."""
        # Agregar un outlier obvio
        test_data_with_outlier = self.test_data.copy()
        test_data_with_outlier.loc[0, 'ingresos_totales'] = 1000000  # Outlier
        
        outliers = detect_outliers_iqr(test_data_with_outlier, 'ingresos_totales')
        
        # Verificar que se detecte al menos un outlier
        self.assertTrue(outliers.any())
        
        # Verificar que el primer registro sea outlier
        self.assertTrue(outliers.iloc[0])
    
    def test_calculate_forecast_accuracy(self):
        """Test para el cálculo de precisión de pronósticos."""
        # Datos de prueba
        actual = np.array([100, 110, 120, 130, 140])
        predicted = np.array([98, 112, 118, 132, 138])
        
        metrics = calculate_forecast_accuracy(actual, predicted)
        
        # Verificar que se calculen todas las métricas
        expected_metrics = ['MAE', 'MSE', 'RMSE', 'MAPE', 'R²']
        for metric in expected_metrics:
            self.assertIn(metric, metrics)
            self.assertIsInstance(metrics[metric], (int, float))
        
        # Verificar que MAPE esté en rango razonable
        self.assertGreater(metrics['MAPE'], 0)
        self.assertLess(metrics['MAPE'], 100)
    
    def test_forecast_accuracy_with_nans(self):
        """Test para manejo de valores NaN en precisión."""
        actual = np.array([100, np.nan, 120, 130, 140])
        predicted = np.array([98, 112, np.nan, 132, 138])
        
        metrics = calculate_forecast_accuracy(actual, predicted)
        
        # Verificar que se manejen los NaN correctamente
        self.assertIn('MAE', metrics)
        self.assertFalse(np.isnan(metrics['MAE']))

class TestDataIntegrity(unittest.TestCase):
    """Tests para verificar la integridad de los datos."""
    
    def test_file_existence(self):
        """Verificar que los archivos necesarios existen."""
        required_files = [
            'requirements.txt',
            'README.md',
            'app.py',
            'config.py',
            'utils.py'
        ]
        
        for file in required_files:
            self.assertTrue(os.path.exists(file), f"Archivo {file} no encontrado")
    
    def test_requirements_format(self):
        """Verificar que requirements.txt tenga el formato correcto."""
        if os.path.exists('requirements.txt'):
            with open('requirements.txt', 'r') as f:
                content = f.read()
                
            # Verificar que contenga las librerías principales
            required_libs = ['streamlit', 'pandas', 'plotly', 'scikit-learn']
            for lib in required_libs:
                self.assertIn(lib, content.lower(), f"Librería {lib} no encontrada en requirements.txt")

class TestConfigIntegrity(unittest.TestCase):
    """Tests para verificar la configuración."""
    
    def test_config_imports(self):
        """Verificar que la configuración se pueda importar."""
        try:
            import config
            self.assertTrue(hasattr(config, 'CLUSTERING_CONFIG'))
            self.assertTrue(hasattr(config, 'CLUSTER_NAMES'))
            self.assertTrue(hasattr(config, 'FILE_PATHS'))
        except ImportError as e:
            self.fail(f"No se pudo importar config.py: {e}")
    
    def test_cluster_config_consistency(self):
        """Verificar consistencia en la configuración de clusters."""
        import config
        
        # Verificar que todos los clusters tengan nombres
        self.assertEqual(len(config.CLUSTER_NAMES), 3)
        
        # Verificar que todos los clusters tengan colores
        self.assertEqual(len(config.CLUSTER_COLORS), 3)
        
        # Verificar que las rutas de pronósticos sean consistentes
        self.assertEqual(len(config.FILE_PATHS['forecasts']), 3)

def run_all_tests():
    """Ejecutar todos los tests."""
    # Crear suite de tests
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Agregar todos los tests
    suite.addTests(loader.loadTestsFromTestCase(TestClusteringUtils))
    suite.addTests(loader.loadTestsFromTestCase(TestDataIntegrity))
    suite.addTests(loader.loadTestsFromTestCase(TestConfigIntegrity))
    
    # Ejecutar tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()

if __name__ == '__main__':
    print("🧪 Ejecutando tests del proyecto de clustering PYMEs...")
    print("=" * 60)
    
    success = run_all_tests()
    
    print("=" * 60)
    if success:
        print("✅ Todos los tests pasaron exitosamente!")
    else:
        print("❌ Algunos tests fallaron. Revisar errores arriba.")
    
    print("\n💡 Para ejecutar tests específicos:")
    print("python test_project.py TestClusteringUtils.test_calculate_business_metrics")
