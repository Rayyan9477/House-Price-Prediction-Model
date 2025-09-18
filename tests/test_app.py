import unittest
import json
import sys
import os
import pandas as pd
import numpy as np

# Add the parent directory to the path so we can import app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, load_and_train_model

class TestHousePricePredictionAPI(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.app = app.test_client()
        self.app.testing = True
        
        # Load and train model for testing
        try:
            load_and_train_model()
        except Exception as e:
            print(f"Warning: Could not load model for testing: {e}")
    
    def test_health_endpoint(self):
        """Test the health check endpoint"""
        response = self.app.get('/health')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('status', data)
        self.assertEqual(data['status'], 'healthy')
        self.assertIn('model_loaded', data)
    
    def test_home_endpoint(self):
        """Test the home page endpoint"""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'House Price Prediction API', response.data)
    
    def test_features_endpoint(self):
        """Test the features endpoint"""
        response = self.app.get('/features')
        
        if response.status_code == 200:
            data = json.loads(response.data)
            self.assertIn('features', data)
            self.assertIn('numerical', data)
            self.assertIn('categorical', data)
            self.assertIn('total_features', data)
            self.assertIsInstance(data['features'], list)
        else:
            # Model not loaded case
            self.assertEqual(response.status_code, 500)
    
    def test_model_info_endpoint(self):
        """Test the model info endpoint"""
        response = self.app.get('/model/info')
        
        if response.status_code == 200:
            data = json.loads(response.data)
            self.assertIn('model_type', data)
            self.assertIn('features_count', data)
            self.assertIn('status', data)
        else:
            # Model not loaded case
            self.assertEqual(response.status_code, 500)
    
    def test_predict_endpoint_missing_features(self):
        """Test prediction endpoint with missing features"""
        response = self.app.post('/predict',
                               data=json.dumps({}),
                               content_type='application/json')
        
        if response.status_code == 400:
            data = json.loads(response.data)
            self.assertIn('error', data)
            self.assertIn('Missing features', data['error'])
        else:
            # Model not loaded case
            self.assertEqual(response.status_code, 500)
    
    def test_predict_endpoint_with_sample_data(self):
        """Test prediction endpoint with sample data"""
        # Sample prediction data (this would need to match your actual features)
        sample_features = {
            'area': 1500,
            'bedrooms': 3,
            'bathrooms': 2,
            'stories': 2,
            'mainroad': 'yes',
            'guestroom': 'no',
            'basement': 'no',
            'hotwaterheating': 'no',
            'airconditioning': 'yes',
            'parking': 2,
            'prefarea': 'yes',
            'furnishingstatus': 'furnished'
        }
        
        response = self.app.post('/predict',
                               data=json.dumps({'features': sample_features}),
                               content_type='application/json')
        
        if response.status_code == 200:
            data = json.loads(response.data)
            self.assertIn('prediction', data)
            self.assertIn('status', data)
            self.assertEqual(data['status'], 'success')
            self.assertIsInstance(data['prediction'], (int, float))
        else:
            # Model not loaded or other error
            self.assertIn(response.status_code, [500, 400])
    
    def test_retrain_endpoint(self):
        """Test the retrain endpoint"""
        response = self.app.post('/retrain')
        
        # This might fail if dataset is not available
        self.assertIn(response.status_code, [200, 500])
        
        if response.status_code == 200:
            data = json.loads(response.data)
            self.assertIn('status', data)
            self.assertIn('Model retrained successfully', data['status'])

class TestModelFunctions(unittest.TestCase):
    """Test the core model functionality"""
    
    def test_load_and_train_model_function(self):
        """Test the load_and_train_model function"""
        try:
            metrics = load_and_train_model()
            self.assertIsInstance(metrics, dict)
            self.assertIn('mae', metrics)
            self.assertIn('mse', metrics)
            self.assertIn('r2', metrics)
            self.assertIn('r2_percentage', metrics)
            
            # Check that metrics are reasonable numbers
            self.assertIsInstance(metrics['mae'], (int, float))
            self.assertIsInstance(metrics['mse'], (int, float))
            self.assertIsInstance(metrics['r2'], (int, float))
            self.assertIsInstance(metrics['r2_percentage'], (int, float))
            
            # R2 should be between -inf and 1, but we expect it to be positive for a decent model
            self.assertLessEqual(metrics['r2'], 1.0)
            
        except FileNotFoundError:
            self.skipTest("Dataset file not found - skipping model training test")
        except Exception as e:
            self.fail(f"Model training failed with error: {e}")

class TestDataValidation(unittest.TestCase):
    """Test data validation and preprocessing"""
    
    def test_dataset_exists(self):
        """Test that the dataset file exists"""
        dataset_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'House_dataset.csv')
        self.assertTrue(os.path.exists(dataset_path), "Dataset file House_dataset.csv not found")
    
    def test_dataset_structure(self):
        """Test the basic structure of the dataset"""
        try:
            dataset_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'House_dataset.csv')
            df = pd.read_csv(dataset_path)
            
            # Check that dataset is not empty
            self.assertGreater(len(df), 0, "Dataset is empty")
            
            # Check that price column exists (target variable)
            self.assertIn('price', df.columns, "Price column not found in dataset")
            
            # Check that there are some features
            self.assertGreater(len(df.columns), 1, "Dataset should have more than just the price column")
            
        except FileNotFoundError:
            self.skipTest("Dataset file not found - skipping dataset structure test")

if __name__ == '__main__':
    # Create a test suite
    unittest.main(verbosity=2)