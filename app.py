import streamlit as st
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
import io

# Page configuration
st.set_page_config(
    page_title="🏠 House Price Predictor",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark theme
st.markdown("""
<style>
    /* Dark theme overrides */
    .stApp {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
        color: #ffffff;
    }
    
    .css-1d391kg, .css-12ttj6m {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
    }
    
    /* Title styling */
    .main-title {
        background: linear-gradient(45deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 3.5em;
        font-weight: 800;
        text-align: center;
        margin-bottom: 0.5em;
        text-shadow: 0 0 30px rgba(102, 126, 234, 0.3);
    }
    
    .subtitle {
        text-align: center;
        color: #b8c5d6;
        font-size: 1.2em;
        margin-bottom: 2em;
        font-style: italic;
    }
    
    /* Card styling */
    .prediction-card {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
        border: 1px solid rgba(102, 126, 234, 0.3);
        border-radius: 20px;
        padding: 2em;
        margin: 1em 0;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
    }
    
    .prediction-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.2);
    }
    
    /* Form styling */
    .stSelectbox, .stNumberInput, .stTextInput {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(102, 126, 234, 0.3);
        border-radius: 10px;
        padding: 0.5em;
        margin-bottom: 1em;
    }
    
    .stSelectbox:hover, .stNumberInput:hover, .stTextInput:hover {
        border-color: #667eea;
        box-shadow: 0 0 10px rgba(102, 126, 234, 0.2);
    }
    
    /* Button styling */
    .stButton>button {
        background: linear-gradient(45deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.8em 2em;
        font-weight: 600;
        font-size: 1.1em;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
    }
    
    /* Success message styling */
    .stSuccess {
        background: linear-gradient(135deg, rgba(40, 167, 69, 0.2) 0%, rgba(34, 197, 94, 0.2) 100%);
        border: 1px solid rgba(40, 167, 69, 0.5);
        border-radius: 15px;
        padding: 1.5em;
        color: #d4edda;
    }
    
    /* Info message styling */
    .stInfo {
        background: linear-gradient(135deg, rgba(23, 162, 184, 0.2) 0%, rgba(0, 123, 255, 0.2) 100%);
        border: 1px solid rgba(23, 162, 184, 0.5);
        border-radius: 15px;
        padding: 1em;
        color: #d1ecf1;
    }
    
    /* Sidebar styling */
    .css-1lcbmhc {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
        border-right: 1px solid rgba(102, 126, 234, 0.2);
    }
    
    /* Metric styling */
    .metric-card {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        padding: 1.5em;
        text-align: center;
        border: 1px solid rgba(102, 126, 234, 0.2);
        margin: 0.5em 0;
    }
    
    .metric-value {
        font-size: 2em;
        font-weight: bold;
        color: #667eea;
        margin-bottom: 0.5em;
    }
    
    .metric-label {
        color: #b8c5d6;
        font-size: 0.9em;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Animation for results */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .fade-in-up {
        animation: fadeInUp 0.6s ease-out;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #1a1a2e;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #667eea;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #764ba2;
    }
</style>
""", unsafe_allow_html=True)

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
        'RandomForest': RandomForestRegressor(n_estimators=100, random_state=42, min_samples_leaf=1, max_features=None),
        'LinearRegression': LinearRegression(),
        'DecisionTree': DecisionTreeRegressor(random_state=42, ccp_alpha=0.0)
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

def load_model():
    """Load trained model or train new one if not exists"""
    if os.path.exists(MODEL_FILE):
        with open(MODEL_FILE, 'rb') as f:
            return pickle.load(f)
    else:
        # Try to load from parts in memory
        if os.path.exists('model_parts.info'):
            with open('model_parts.info', 'rb') as f:
                info = pickle.load(f)
            total_parts = info['total_parts']
            # Check if all parts exist
            all_parts_exist = all(os.path.exists(f'house_price_model.pkl.part{i:02d}') for i in range(1, total_parts + 1))
            if all_parts_exist:
                # Combine parts in memory
                combined = io.BytesIO()
                for i in range(1, total_parts + 1):
                    part_filename = f'house_price_model.pkl.part{i:02d}'
                    with open(part_filename, 'rb') as infile:
                        combined.write(infile.read())
                combined.seek(0)
                return pickle.load(combined)
        # If not, train new model
        return load_and_train_model()

# Load model on startup
model_data = load_model()

# Sidebar
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 1em;">
        <h2 style="color: #667eea; margin-bottom: 0.5em;">📊 Model Insights</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Model metrics
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{model_data['model_name'][:3]}</div>
        <div class="metric-label">Best Model</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{model_data['r2_score']*100:.1f}%</div>
        <div class="metric-label">Accuracy</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Retrain button in sidebar
    if st.button("🔄 Retrain Model", key="sidebar_retrain"):
        with st.spinner("Retraining model..."):
            try:
                model_data = load_and_train_model()
                st.success("✅ Model retrained successfully!")
                st.rerun()
            except Exception as e:
                st.error(f"❌ Error retraining model: {str(e)}")
    
    st.markdown("---")
    
    # About section
    st.markdown("""
    <div style="background: rgba(255,255,255,0.05); padding: 1em; border-radius: 10px; margin-top: 1em;">
        <h4 style="color: #667eea; margin-bottom: 0.5em;">🤖 About</h4>
        <p style="color: #b8c5d6; font-size: 0.9em; line-height: 1.4;">
        This AI-powered house price predictor uses machine learning to provide accurate property valuations based on location, size, and features.
        </p>
    </div>
    """, unsafe_allow_html=True)

# Main content
st.markdown("""
<div class="main-title">🏠 House Price Predictor</div>
<div class="subtitle">Discover your property's true value with AI-powered precision</div>
""", unsafe_allow_html=True)

# Create two columns for the main content
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    <div class="prediction-card">
        <h3 style="color: #667eea; margin-bottom: 1em; text-align: center;">🔮 Property Details</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Input form
    with st.form("prediction_form"):
        # Property details section
        st.markdown("#### 🏢 Property Information")
        
        col_a, col_b = st.columns(2)
        with col_a:
            property_type = st.selectbox(
                "Property Type", 
                ["House", "Flat", "Penthouse", "Studio"],
                help="Select the type of property"
            )
            city = st.selectbox(
                "City", 
                ["Islamabad", "Rawalpindi", "Lahore", "Karachi"],
                help="Select the city where the property is located"
            )
        
        with col_b:
            bedrooms = st.number_input(
                "Bedrooms", 
                min_value=1, 
                max_value=10, 
                value=3,
                help="Number of bedrooms"
            )
            baths = st.number_input(
                "Bathrooms", 
                min_value=1, 
                max_value=10, 
                value=2,
                help="Number of bathrooms"
            )
        
        # Location and area section
        st.markdown("#### 📍 Location & Size")
        
        location = st.text_input(
            "Location", 
            placeholder="e.g., G-10, DHA Defence, Bahria Town",
            help="Specific location or area within the city"
        )
        
        col_c, col_d = st.columns(2)
        with col_c:
            area_in_marla = st.number_input(
                "Area (Marla)", 
                min_value=1.0, 
                value=5.0, 
                step=0.1,
                help="Property area in Marla"
            )
        with col_d:
            purpose = st.selectbox(
                "Purpose", 
                ["For Sale", "For Rent"],
                help="Is the property for sale or rent?"
            )
        
        # Submit button
        submitted = st.form_submit_button("� Predict Price", use_container_width=True)

with col2:
    # Results section
    st.markdown("""
    <div class="prediction-card">
        <h3 style="color: #667eea; margin-bottom: 1em; text-align: center;">💰 Prediction Results</h3>
    </div>
    """, unsafe_allow_html=True)
    
    if submitted:
        try:
            # Prepare input data
            input_data = pd.DataFrame([{
                'property_type': property_type,
                'location': location,
                'city': city,
                'baths': baths,
                'purpose': purpose,
                'bedrooms': bedrooms,
                'Area_in_Marla': area_in_marla
            }])

            # Encode categorical variables
            for col in ['property_type', 'location', 'city', 'purpose']:
                if col in model_data['label_encoders']:
                    le = model_data['label_encoders'][col]
                    try:
                        input_data[col] = le.transform([str(input_data[col].iloc[0])])
                    except ValueError:
                        # Handle unknown categories by using the most frequent one
                        input_data[col] = le.transform([le.classes_[0]])

            # Make prediction
            prediction = model_data['model'].predict(input_data[model_data['feature_columns']])[0]

            # Display result with animation
            st.markdown(f"""
            <div class="fade-in-up">
                <div style="text-align: center; margin: 2em 0;">
                    <div style="font-size: 3em; font-weight: bold; color: #667eea; margin-bottom: 0.5em;">
                        PKR {prediction:,.0f}
                    </div>
                    <div style="color: #b8c5d6; font-size: 1.1em;">
                        Estimated Property Value
                    </div>
                </div>
                
                <div style="background: rgba(102, 126, 234, 0.1); border: 1px solid rgba(102, 126, 234, 0.3); border-radius: 10px; padding: 1em; margin-top: 1em;">
                    <div style="color: #b8c5d6; font-size: 0.9em;">
                        <strong>Model:</strong> {model_data['model_name']}<br>
                        <strong>Accuracy:</strong> {(model_data['r2_score'] * 100):.1f}%
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Success message
            st.success("✅ Prediction completed successfully!")

        except Exception as e:
            st.error(f"❌ Error making prediction: {str(e)}")
    else:
        # Placeholder when no prediction is made
        st.markdown("""
        <div style="text-align: center; padding: 3em 1em; color: #666;">
            <div style="font-size: 4em; margin-bottom: 1em;">🔮</div>
            <div style="font-size: 1.2em; color: #b8c5d6;">
                Fill in the property details and click "Predict Price" to get started
            </div>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2em; color: #666;">
    <p>Built with ❤️ using Streamlit & Machine Learning</p>
    <p style="font-size: 0.8em;">© 2025 House Price Predictor</p>
</div>
""", unsafe_allow_html=True)