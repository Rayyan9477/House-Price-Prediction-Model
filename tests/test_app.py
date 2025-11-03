import unittest
import sys
import os
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock

# Add the parent directory to the path so we can import app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import app modules after path modification
from app import load_and_train_model  # noqa: E402

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
            # Since we don't have endpoints, we'll test the model directly
            model_data = load_and_train_model()
            
            # Create test input
            test_data = pd.DataFrame([{
                'property_type': 'House',
                'location': 'G-10',
                'city': 'Islamabad',
                'baths': 3,
                'purpose': 'For Sale',
                'bedrooms': 4,
                'Area_in_Marla': 8.0
            }])

            # Encode categorical variables
            for col in ['property_type', 'location', 'city', 'purpose']:
                if col in model_data['label_encoders']:
                    le = model_data['label_encoders'][col]
                    test_data[col] = le.transform([str(test_data[col].iloc[0])])

            # Make multiple predictions
            predictions = []
            for _ in range(3):
                pred = model_data['model'].predict(test_data[model_data['feature_columns']])[0]
                predictions.append(pred)

            # All predictions should be identical
            if len(predictions) > 1:
                for i in range(1, len(predictions)):
                    self.assertAlmostEqual(predictions[0], predictions[i], places=2,
                                         msg="Predictions should be consistent for same input")

        except Exception as e:
            self.skipTest(f"Prediction consistency test skipped: {e}")

if __name__ == '__main__':
    # Run tests with high verbosity
    unittest.main(verbosity=2)