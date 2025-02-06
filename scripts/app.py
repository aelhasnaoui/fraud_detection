# fraud_detection/app.py

from flask import Flask, request, jsonify
from joblib import load
import pandas as pd
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

# Load the trained model
model = load("models/random_forest_model.pkl")

# Define the expected feature names (in the same order as during training)
EXPECTED_FEATURES = [
    "V1", "V2", "V3", "V4", "V5", "V6", "V7", "V8", "V9", "V10",
    "V11", "V12", "V13", "V14", "V15", "V16", "V17", "V18", "V19", "V20",
    "V21", "V22", "V23", "V24", "V25", "V26", "V27", "V28", "Amount"
]

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get input data from the request
        data = request.json

        # Ensure the input data has the correct feature names and order
        df = pd.DataFrame([data])
        df = df[EXPECTED_FEATURES]  # Reorder columns to match the training data

        # Make prediction
        prediction = model.predict(df)[0]

        # Return the result as JSON
        return jsonify({"prediction": int(prediction)})
    except KeyError as e:
        return jsonify({"error": f"Missing feature: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)