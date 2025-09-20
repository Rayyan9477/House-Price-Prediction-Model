from flask import Flask, request, jsonify, render_template_string
import pandas as pd
import pickle
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import os

app = Flask(__name__)

# Load or train model
MODEL_FILE = 'house_price_model.pkl'

def load_and_train_model():
    """Load dataset, train multiple models, and save the best one"""
    # Load dataset
    df = pd.read_csv('House_dataset.csv')

    # Remove first column if it's unnamed index
    if df.columns[0] in ['Unnamed: 0', '']:
        df = df.drop(df.columns[0], axis=1)

    # Handle missing values
    df = df.dropna()

    # Prepare features and target
    feature_columns = ['property_type', 'location', 'city', 'baths', 'purpose', 'bedrooms', 'Area_in_Marla']
    X = df[feature_columns].copy()
    y = df['price']

    # Encode categorical variables
    label_encoders = {}
    categorical_columns = ['property_type', 'location', 'city', 'purpose']

    for col in categorical_columns:
        le = LabelEncoder()
        X[col] = le.fit_transform(X[col].astype(str))
        label_encoders[col] = le

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train multiple models
    models = {
        'RandomForest': RandomForestRegressor(n_estimators=100, random_state=42),
        'LinearRegression': LinearRegression(),
        'DecisionTree': DecisionTreeRegressor(random_state=42)
    }

    best_model = None
    best_score = float('-inf')
    best_name = ''

    print("Training and evaluating models...")
    for name, model in models.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        r2 = r2_score(y_test, y_pred)
        mae = mean_absolute_error(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))

        print(f"{name}: R2={r2:.4f}, MAE={mae:.2f}, RMSE={rmse:.2f}")

        if r2 > best_score:
            best_score = r2
            best_model = model
            best_name = name

    print(f"Best model: {best_name} with R2 score: {best_score:.4f}")

    # Save best model and encoders
    model_data = {
        'model': best_model,
        'label_encoders': label_encoders,
        'feature_columns': feature_columns,
        'model_name': best_name,
        'r2_score': best_score
    }

    with open(MODEL_FILE, 'wb') as f:
        pickle.dump(model_data, f)

    print(f"Model saved to {MODEL_FILE}")
    return model_data

def reconstruct_model_if_needed():
    """Reconstruct model from parts if main file doesn't exist"""
    if not os.path.exists(MODEL_FILE) and os.path.exists('model_parts.info'):
        print("Model file not found, reconstructing from parts...")

        # Read info
        with open('model_parts.info', 'rb') as f:
            info = pickle.load(f)

        total_parts = info['total_parts']

        # Check if all parts exist
        all_parts_exist = True
        for i in range(1, total_parts + 1):
            part_filename = f'house_price_model.pkl.part{i:02d}'
            if not os.path.exists(part_filename):
                all_parts_exist = False
                break

        if all_parts_exist:
            # Reconstruct file
            with open(MODEL_FILE, 'wb') as outfile:
                for i in range(1, total_parts + 1):
                    part_filename = f'house_price_model.pkl.part{i:02d}'
                    with open(part_filename, 'rb') as infile:
                        outfile.write(infile.read())
            print(f"Model reconstructed successfully from {total_parts} parts")
        else:
            print("Some model parts are missing, will train new model")

def load_model():
    """Load trained model or train new one if not exists"""
    # First try to reconstruct from parts if needed
    reconstruct_model_if_needed()

    if os.path.exists(MODEL_FILE):
        with open(MODEL_FILE, 'rb') as f:
            return pickle.load(f)
    else:
        return load_and_train_model()

# Load model on startup
model_data = load_model()

@app.route('/')
def home():
    """Serve the main HTML page"""
    html_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>House Price Predictor</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }

            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
            }

            .container {
                max-width: 800px;
                margin: 0 auto;
                background: white;
                border-radius: 15px;
                box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                overflow: hidden;
            }

            .header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 30px;
                text-align: center;
            }

            .header h1 {
                font-size: 2.5em;
                margin-bottom: 10px;
            }

            .header p {
                font-size: 1.1em;
                opacity: 0.9;
            }

            .form-container {
                padding: 40px;
            }

            .form-group {
                margin-bottom: 25px;
            }

            .form-group label {
                display: block;
                margin-bottom: 8px;
                font-weight: 600;
                color: #333;
                font-size: 1.1em;
            }

            .form-group input, .form-group select {
                width: 100%;
                padding: 12px 15px;
                border: 2px solid #e1e5e9;
                border-radius: 8px;
                font-size: 1em;
                transition: border-color 0.3s ease;
            }

            .form-group input:focus, .form-group select:focus {
                outline: none;
                border-color: #667eea;
                box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
            }

            .form-row {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 20px;
            }

            .predict-btn {
                width: 100%;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border: none;
                padding: 15px;
                font-size: 1.2em;
                font-weight: 600;
                border-radius: 8px;
                cursor: pointer;
                transition: transform 0.3s ease;
            }

            .predict-btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
            }

            .result {
                margin-top: 30px;
                padding: 20px;
                background: #f8f9fa;
                border-radius: 8px;
                border-left: 4px solid #667eea;
                display: none;
            }

            .result.show {
                display: block;
                animation: slideIn 0.5s ease;
            }

            @keyframes slideIn {
                from { opacity: 0; transform: translateY(20px); }
                to { opacity: 1; transform: translateY(0); }
            }

            .price {
                font-size: 2em;
                font-weight: bold;
                color: #667eea;
                margin-bottom: 10px;
            }

            .model-info {
                color: #666;
                font-size: 0.9em;
            }

            @media (max-width: 600px) {
                .form-row {
                    grid-template-columns: 1fr;
                }

                .header h1 {
                    font-size: 2em;
                }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🏠 House Price Predictor</h1>
                <p>Get accurate price predictions using advanced ML algorithms</p>
            </div>

            <div class="form-container">
                <form id="predictionForm">
                    <div class="form-row">
                        <div class="form-group">
                            <label for="property_type">Property Type:</label>
                            <select id="property_type" name="property_type" required>
                                <option value="">Select Type</option>
                                <option value="House">House</option>
                                <option value="Flat">Flat</option>
                                <option value="Penthouse">Penthouse</option>
                                <option value="Studio">Studio</option>
                            </select>
                        </div>

                        <div class="form-group">
                            <label for="city">City:</label>
                            <select id="city" name="city" required>
                                <option value="">Select City</option>
                                <option value="Islamabad">Islamabad</option>
                                <option value="Rawalpindi">Rawalpindi</option>
                                <option value="Lahore">Lahore</option>
                                <option value="Karachi">Karachi</option>
                            </select>
                        </div>
                    </div>

                    <div class="form-group">
                        <label for="location">Location:</label>
                        <input type="text" id="location" name="location" placeholder="e.g., G-10, DHA Defence" required>
                    </div>

                    <div class="form-row">
                        <div class="form-group">
                            <label for="bedrooms">Bedrooms:</label>
                            <input type="number" id="bedrooms" name="bedrooms" min="1" max="10" required>
                        </div>

                        <div class="form-group">
                            <label for="baths">Bathrooms:</label>
                            <input type="number" id="baths" name="baths" min="1" max="10" required>
                        </div>
                    </div>

                    <div class="form-row">
                        <div class="form-group">
                            <label for="Area_in_Marla">Area (Marla):</label>
                            <input type="number" id="Area_in_Marla" name="Area_in_Marla" step="0.1" min="1" required>
                        </div>

                        <div class="form-group">
                            <label for="purpose">Purpose:</label>
                            <select id="purpose" name="purpose" required>
                                <option value="">Select Purpose</option>
                                <option value="For Sale">For Sale</option>
                                <option value="For Rent">For Rent</option>
                            </select>
                        </div>
                    </div>

                    <button type="submit" class="predict-btn">🔮 Predict Price</button>
                </form>

                <div id="result" class="result">
                    <div class="price" id="predicted-price"></div>
                    <div class="model-info">
                        Model: <span id="model-name"></span> |
                        Accuracy: <span id="model-accuracy"></span>
                    </div>
                </div>
            </div>
        </div>

        <script>
            document.getElementById('predictionForm').addEventListener('submit', async function(e) {
                e.preventDefault();

                const formData = new FormData(this);
                const data = Object.fromEntries(formData.entries());

                // Convert numeric fields
                data.bedrooms = parseInt(data.bedrooms);
                data.baths = parseInt(data.baths);
                data.Area_in_Marla = parseFloat(data.Area_in_Marla);

                try {
                    const response = await fetch('/predict', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify(data)
                    });

                    const result = await response.json();

                    if (result.success) {
                        document.getElementById('predicted-price').textContent =
                            `PKR ${result.predicted_price.toLocaleString()}`;
                        document.getElementById('model-name').textContent = result.model_name;
                        document.getElementById('model-accuracy').textContent =
                            `${(result.model_accuracy * 100).toFixed(1)}%`;
                        document.getElementById('result').classList.add('show');
                    } else {
                        alert('Error: ' + result.error);
                    }
                } catch (error) {
                    alert('Error making prediction: ' + error.message);
                }
            });
        </script>
    </body>
    </html>
    """
    return render_template_string(html_template)

@app.route('/predict', methods=['POST'])
def predict():
    """Handle prediction requests"""
    try:
        # Validate JSON
        if not request.is_json:
            return jsonify({
                'success': False,
                'error': 'Content-Type must be application/json'
            }), 400

        data = request.get_json()

        if data is None:
            return jsonify({
                'success': False,
                'error': 'Invalid JSON data'
            }), 400

        # Create input dataframe
        input_data = pd.DataFrame([data])

        # Encode categorical variables
        for col in ['property_type', 'location', 'city', 'purpose']:
            if col in model_data['label_encoders']:
                le = model_data['label_encoders'][col]
                try:
                    input_data[col] = le.transform([str(data[col])])
                except ValueError:
                    # Handle unknown categories by using the most frequent one
                    input_data[col] = le.transform([le.classes_[0]])

        # Make prediction
        prediction = model_data['model'].predict(input_data[model_data['feature_columns']])[0]

        return jsonify({
            'success': True,
            'predicted_price': float(prediction),
            'model_name': model_data['model_name'],
            'model_accuracy': float(model_data['r2_score'])
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/retrain', methods=['POST'])
def retrain():
    """Retrain the model with fresh data"""
    try:
        global model_data
        model_data = load_and_train_model()
        return jsonify({
            'success': True,
            'message': 'Model retrained successfully',
            'model_name': model_data['model_name'],
            'accuracy': float(model_data['r2_score'])
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

if __name__ == '__main__':
    print("Starting House Price Prediction App...")
    print("Visit http://localhost:5000 to use the application")
    app.run(debug=True, host='0.0.0.0', port=5000)