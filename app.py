import pickle
import json
from flask import Flask, render_template, request, jsonify
import pandas as pd
from pymongo import MongoClient
from joblib import dump, load

from url_shield import url_features

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secrets.token_hex(16)'  # Set a secret key for CSRF protection

# MongoDB connection
cluster_uri = "<MONGODB_URI>" #insert your mongodb url
client = MongoClient(cluster_uri)

# Check if the connection is established
try:
    client.server_info()
    print("Connected to MongoDB Atlas")
except Exception as e:
    print("Failed to connect to MongoDB Atlas:", e)

db = client['Phishing']  # Connect to the database named 'Phishing'
collection = db['phishingdata']  # Collection name 'phishingdata'

# Load the scikit-learn model from the .pkl file
try:
    with open('model.pkl', 'rb') as file:
        model = pickle.load(file)
        print("Model loaded successfully.")
except Exception as e:
    model = None  # Set model to None if loading fails
    print(f"Error loading model: {e}")

# Only dump the model if it was loaded successfully
if model:
    dump(model, 'model.joblib')  # Save the model to joblib format
else:
    print("Model was not loaded, skipping dump.")

@app.route('/submit_contact_form', methods=['POST'])
def submit_contact_form():
    if request.method == 'POST':
        email = request.form['email']
        phishing_website = request.form['phishing_website']
        description = request.form['description']
        
        # Store the report in MongoDB
        report_data = {
            'email': email,
            'phishing_website': phishing_website,
            'description': description
        }
        collection.insert_one(report_data)
        
        return "Thank you for reporting the phishing website! Your report has been submitted."
    else:
        return "Method not allowed", 405

@app.route('/') 
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    input_url = request.form.get('input_url') 
    if input_url != '' and model is not None:  # Check if model is loaded
        # Assuming url_features.get_prediction_from_url uses the loaded model to make predictions
        prediction_result = url_features.get_prediction_from_url(input_url, model) 
        return render_template('index.html', url=input_url, prediction=prediction_result)
    else:
        prediction_result = "Input field for the URL cannot be empty or model not loaded."
        return render_template('index.html', prediction=prediction_result)

if __name__ == '__main__':
    app.run(debug=True)
