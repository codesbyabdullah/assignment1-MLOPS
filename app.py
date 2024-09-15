
from flask import Flask, request, render_template_string
import joblib
import os
import numpy as np
import pandas as pd

app = Flask(__name__)

# Load the trained model
model_path = 'model.pkl'
if not os.path.exists(model_path):
    raise FileNotFoundError(f"Model file '{model_path}' not found. Please ensure the file exists.")
model = joblib.load(model_path)

# HTML Template for the frontend
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>House Price Prediction</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        input[type="text"], select { padding: 10px; margin: 10px 0; width: 100%; }
        input[type="submit"] { padding: 10px 20px; background: #28a745; color: white; border: none; }
        .result { margin-top: 20px; font-weight: bold; }
    </style>
</head>
<body>
    <h2>House Price Prediction</h2>
    <form action="/predict" method="post">
        <label>Area (in sq ft):</label>
        <input type="text" name="Area" required>
        <label>Number of Bedrooms:</label>
        <input type="text" name="No_of_Bedrooms" required>
        <label>Location:</label>
        <select name="Location" required>
            <option value="">Select Location</option>
            <option value="JP Nagar Phase 1">JP Nagar Phase 1</option>
            <option value="Dasarahalli on Tumkur Road">Dasarahalli on Tumkur Road</option>
            <option value="Kannur on Thanisandra Main Road">Kannur on Thanisandra Main Road</option>
            <option value="Doddanekundi">Doddanekundi</option>
            <option value="Kengeri">Kengeri</option>
            <!-- Add other locations as needed -->
        </select>
        <input type="submit" value="Predict">
    </form>
    <div class="result">{{ prediction_text }}</div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(html_template)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Collect input features from the form
        area = float(request.form['Area'])
        bedrooms = int(request.form['No_of_Bedrooms'])
        location = request.form['Location']

        # Prepare input for the model
        input_data = pd.DataFrame([[area, bedrooms, location]], columns=['Area', 'No. of Bedrooms', 'Location'])

        # Predict the price
        prediction = model.predict(input_data)

        # Apply a minimum bound to the prediction
        output = max(0, np.round(prediction[0], 2))  # Ensures the price is not negative

        return render_template_string(html_template, prediction_text=f"Predicted Price: {output} units")
    except Exception as e:
        return render_template_string(html_template, prediction_text=f"Error: {str(e)}")

if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=5000)
