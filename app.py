from flask import Flask, request, jsonify
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer

app = Flask(__name__)

# Global variables for the model and preprocessing
model_pipeline = None
feature_columns = None
numerical_cols = None
categorical_cols = None

def load_and_train_model():
    """Load dataset and train the model"""
    global model_pipeline, feature_columns, numerical_cols, categorical_cols
    
    # Load the dataset
    df = pd.read_csv("House_dataset.csv")
    
    # Distribute numerical and categorical columns
    numerical_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()

    if 'price' in numerical_cols:
        numerical_cols.remove('price')

    # Data Cleaning for Numbers
    for col in numerical_cols:
        df[col] = df[col].fillna(df[col].mean())

    # Data Cleaning for Strings
    for col in categorical_cols:
        df[col] = df[col].fillna(df[col].mode()[0])

    # Feature Engineering
    # Preprocessing for numerical and categorical data
    numerical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='mean')),
        ('scaler', StandardScaler())])

    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('onehot', OneHotEncoder(handle_unknown='ignore'))])

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numerical_transformer, numerical_cols),
            ('cat', categorical_transformer, categorical_cols)])

    # Model selection and Training
    model = RandomForestRegressor(n_estimators=100, random_state=42)

    model_pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                                   ('model', model)])

    X = df.drop('price', axis=1)
    y = df['price']
    feature_columns = X.columns.tolist()

    # Split data for training
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train the model
    model_pipeline.fit(X_train, y_train)

    # Make predictions for evaluation
    y_pred = model_pipeline.predict(X_test)

    # Evaluate the model's performance
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print("Model trained successfully!")
    print(f"Mean Absolute Error (MAE): {mae}")
    print(f"Mean Squared Error (MSE): {mse}")
    print(f"R-squared (R2): {r2}")
    
    return {
        'mae': mae,
        'mse': mse,
        'r2': r2,
        'r2_percentage': r2 * 100
    }

@app.route('/')
def home():
    """Home page with API documentation"""
    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>House Price Prediction API</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            .container { max-width: 800px; margin: 0 auto; }
            .endpoint { background-color: #f5f5f5; padding: 20px; margin: 20px 0; border-radius: 5px; }
            .method { color: #0066cc; font-weight: bold; }
            pre { background-color: #e8e8e8; padding: 10px; border-radius: 3px; overflow-x: auto; }
            h1 { color: #333; }
            h2 { color: #666; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>House Price Prediction API</h1>
            <p>A machine learning API for predicting house prices using RandomForest regression.</p>
            
            <div class="endpoint">
                <h2><span class="method">GET</span> /health</h2>
                <p>Check if the API is running and model is loaded.</p>
                <pre>Response: {"status": "healthy", "model_loaded": true}</pre>
            </div>
            
            <div class="endpoint">
                <h2><span class="method">GET</span> /model/info</h2>
                <p>Get information about the trained model performance.</p>
                <pre>Response: {"mae": 123.45, "mse": 456.78, "r2": 0.89, "r2_percentage": 89.0}</pre>
            </div>
            
            <div class="endpoint">
                <h2><span class="method">POST</span> /predict</h2>
                <p>Predict house price based on input features.</p>
                <p><strong>Request Body:</strong></p>
                <pre>{
  "features": {
    "feature1": value1,
    "feature2": value2,
    ...
  }
}</pre>
                <p><strong>Response:</strong></p>
                <pre>{"prediction": 123456.78, "status": "success"}</pre>
            </div>
            
            <div class="endpoint">
                <h2><span class="method">GET</span> /features</h2>
                <p>Get list of required features for prediction.</p>
                <pre>Response: {"features": ["feature1", "feature2", ...], "numerical": [...], "categorical": [...]}</pre>
            </div>
        </div>
    </body>
    </html>
    """
    return html_template

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': model_pipeline is not None
    })

@app.route('/model/info', methods=['GET'])
def model_info():
    """Get model performance information"""
    if model_pipeline is None:
        return jsonify({'error': 'Model not loaded'}), 500
    
    # Get the cached model metrics (you might want to store these during training)
    return jsonify({
        'model_type': 'RandomForestRegressor',
        'features_count': len(feature_columns),
        'status': 'trained'
    })

@app.route('/features', methods=['GET'])
def get_features():
    """Get the list of features required for prediction"""
    if feature_columns is None:
        return jsonify({'error': 'Model not loaded'}), 500
    
    return jsonify({
        'features': feature_columns,
        'numerical': numerical_cols,
        'categorical': categorical_cols,
        'total_features': len(feature_columns)
    })

@app.route('/predict', methods=['POST'])
def predict():
    """Predict house price based on input features"""
    if model_pipeline is None:
        return jsonify({'error': 'Model not loaded'}), 500
    
    try:
        data = request.get_json()
        
        if 'features' not in data:
            return jsonify({'error': 'Missing features in request'}), 400
        
        features = data['features']
        
        # Create DataFrame with the input features
        input_df = pd.DataFrame([features])
        
        # Ensure all required columns are present
        for col in feature_columns:
            if col not in input_df.columns:
                input_df[col] = 0  # or some default value
        
        # Reorder columns to match training data
        input_df = input_df[feature_columns]
        
        # Make prediction
        prediction = model_pipeline.predict(input_df)[0]
        
        return jsonify({
            'prediction': float(prediction),
            'status': 'success'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/retrain', methods=['POST'])
def retrain_model():
    """Retrain the model (useful for updates)"""
    try:
        metrics = load_and_train_model()
        return jsonify({
            'status': 'Model retrained successfully',
            'metrics': metrics
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    # Load and train the model on startup
    print("Loading and training model...")
    try:
        metrics = load_and_train_model()
        print("Model loaded successfully!")
    except Exception as e:
        print(f"Error loading model: {e}")

    # Run the Flask app
    # Use debug=False for production security
    # Bind to 0.0.0.0 for Docker containerization
    app.run(host='0.0.0.0', port=5000, debug=False)  # nosec