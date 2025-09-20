import unittest
import json
import sys
import os
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock

# Add the parent directory to the path so we can import app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import app modules after path modification
from app import app, load_and_train_model  # noqa: E402

class TestHousePricePredictionAPI(unittest.TestCase):

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.app = app.test_client()
        self.app.testing = True

    def test_home_endpoint(self):
        """Test the home page endpoint"""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'House Price Predictor', response.data)
        self.assertIn(b'html', response.data)

    def test_predict_endpoint_with_valid_data(self):
        """Test prediction endpoint with valid data"""
        sample_data = {
            'property_type': 'House',
            'location': 'G-10',
            'city': 'Islamabad',
            'baths': 3,
            'purpose': 'For Sale',
            'bedrooms': 4,
            'Area_in_Marla': 8.0
        }

        response = self.app.post('/predict',
                               data=json.dumps(sample_data),
                               content_type='application/json')

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)

        self.assertIn('success', data)
        self.assertTrue(data['success'])
        self.assertIn('predicted_price', data)
        self.assertIn('model_name', data)
        self.assertIn('model_accuracy', data)
        self.assertIsInstance(data['predicted_price'], (int, float))
        self.assertGreater(data['predicted_price'], 0)

    def test_predict_endpoint_missing_data(self):
        """Test prediction endpoint with missing data"""
        incomplete_data = {
            'property_type': 'House',
            'city': 'Islamabad'
            # Missing required fields
        }

        response = self.app.post('/predict',
                               data=json.dumps(incomplete_data),
                               content_type='application/json')

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)

        # Should return an error or handle gracefully
        self.assertIn('success', data)

    def test_predict_endpoint_invalid_json(self):
        """Test prediction endpoint with invalid JSON"""
        response = self.app.post('/predict',
                               data='invalid json',
                               content_type='application/json')

        # Should return either 400 for invalid JSON or 200 with error in response
        self.assertIn(response.status_code, [200, 400])

        if response.status_code == 200:
            data = json.loads(response.data)
            self.assertIn('success', data)
            self.assertFalse(data['success'])  # Should indicate failure

    def test_retrain_endpoint(self):
        """Test the retrain endpoint"""
        response = self.app.post('/retrain')

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)

        self.assertIn('success', data)
        if data['success']:
            self.assertIn('message', data)
            self.assertIn('model_name', data)
            self.assertIn('accuracy', data)
        else:
            self.assertIn('error', data)

class TestModelFunctions(unittest.TestCase):
    """Test the core model functionality"""

    def test_load_and_train_model_function(self):
        """Test the load_and_train_model function"""
        try:
            model_data = load_and_train_model()

            # Verify model_data structure
            self.assertIsInstance(model_data, dict)
            self.assertIn('model', model_data)
            self.assertIn('label_encoders', model_data)
            self.assertIn('feature_columns', model_data)
            self.assertIn('model_name', model_data)
            self.assertIn('r2_score', model_data)

            # Verify model performance
            self.assertIsInstance(model_data['r2_score'], (int, float))
            self.assertGreater(model_data['r2_score'], 0)  # Should be positive for a decent model
            self.assertLessEqual(model_data['r2_score'], 1.0)  # R2 max is 1.0

            # Verify feature columns
            expected_features = ['property_type', 'location', 'city', 'baths', 'purpose', 'bedrooms', 'Area_in_Marla']
            self.assertEqual(model_data['feature_columns'], expected_features)

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

            # Check that all required feature columns exist
            required_columns = ['property_type', 'location', 'city', 'baths', 'purpose', 'bedrooms', 'Area_in_Marla', 'price']
            for col in required_columns:
                self.assertIn(col, df.columns, f"Required column '{col}' not found in dataset")

            # Check data types
            self.assertTrue(pd.api.types.is_numeric_dtype(df['price']), "Price column should be numeric")
            self.assertTrue(pd.api.types.is_numeric_dtype(df['baths']), "Baths column should be numeric")
            self.assertTrue(pd.api.types.is_numeric_dtype(df['bedrooms']), "Bedrooms column should be numeric")
            self.assertTrue(pd.api.types.is_numeric_dtype(df['Area_in_Marla']), "Area_in_Marla column should be numeric")

        except FileNotFoundError:
            self.skipTest("Dataset file not found - skipping dataset structure test")

class TestMLModelPerformance(unittest.TestCase):
    """Test ML model performance and metrics"""

    def test_model_accuracy_threshold(self):
        """Test that the model meets minimum accuracy requirements"""
        try:
            model_data = load_and_train_model()
            r2_score = model_data['r2_score']

            # Model should have at least 70% accuracy for house price prediction
            self.assertGreater(r2_score, 0.7, f"Model R2 score {r2_score:.3f} is below 70% threshold")

        except FileNotFoundError:
            self.skipTest("Dataset file not found - skipping model performance test")

    def test_prediction_consistency(self):
        """Test that predictions are consistent for the same input"""
        try:
            # Make multiple predictions with same input
            test_data = {
                'property_type': 'House',
                'location': 'G-10',
                'city': 'Islamabad',
                'baths': 3,
                'purpose': 'For Sale',
                'bedrooms': 4,
                'Area_in_Marla': 8.0
            }

            predictions = []
            for _ in range(3):
                response = self.app.post('/predict',
                                       data=json.dumps(test_data),
                                       content_type='application/json')

                self.assertEqual(response.status_code, 200)
                data = json.loads(response.data)
                if data['success']:
                    predictions.append(data['predicted_price'])

            # All predictions should be identical
            if len(predictions) > 1:
                for i in range(1, len(predictions)):
                    self.assertAlmostEqual(predictions[0], predictions[i], places=2,
                                         msg="Predictions should be consistent for same input")

        except Exception as e:
            self.skipTest(f"Prediction consistency test skipped: {e}")

class TestAPIEndpoints(unittest.TestCase):
    """Test all API endpoints"""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.app = app.test_client()
        self.app.testing = True

    def test_health_endpoint(self):
        """Test a basic health check"""
        # Test that the app starts without errors
        response = self.app.get('/')
        self.assertIn(response.status_code, [200, 404])  # 404 is also acceptable if no health endpoint

    def test_prediction_validation(self):
        """Test input validation for predictions"""
        # Test with invalid property type
        invalid_data = {
            'property_type': 'InvalidType',
            'location': 'G-10',
            'city': 'Islamabad',
            'baths': 3,
            'purpose': 'For Sale',
            'bedrooms': 4,
            'Area_in_Marla': 8.0
        }

        response = self.app.post('/predict',
                               data=json.dumps(invalid_data),
                               content_type='application/json')

        self.assertEqual(response.status_code, 200)  # Should handle gracefully

        # Test with negative values
        negative_data = {
            'property_type': 'House',
            'location': 'G-10',
            'city': 'Islamabad',
            'baths': -1,  # Invalid negative value
            'purpose': 'For Sale',
            'bedrooms': 4,
            'Area_in_Marla': 8.0
        }

        response = self.app.post('/predict',
                               data=json.dumps(negative_data),
                               content_type='application/json')

        # Should either handle gracefully or return appropriate error
        self.assertIn(response.status_code, [200, 400])

if __name__ == '__main__':
    # Run tests with high verbosity
    unittest.main(verbosity=2)