import pickle
import json
from sklearn.linear_model import LogisticRegression # type: ignore

# Load the scikit-learn model from the .pkl file
with open('model.pkl', 'rb') as file:
    model = pickle.load(file)

# Convert the model to a JSON-friendly format
model_json = {
    'type': type(model).__name__,
    'params': model.get_params(),
    # Include any additional information needed for reconstruction
}

# Save the JSON representation to a .json file
with open('model.json', 'w') as file:
    json.dump(model_json, file)
