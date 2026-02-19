import pickle
import numpy as np

class ModelService:

    def __init__(self):
        with open("ml_models/rf_tuned_model.pkl", "rb") as f:
            self.model = pickle.load(f)

        with open("ml_models/scaler.pkl", "rb") as f:
            self.scaler = pickle.load(f)

    def predict(self, features):
        features = np.array(features).reshape(1, -1)
        scaled = self.scaler.transform(features)

        prediction = self.model.predict(scaled)[0]
        probabilities = self.model.predict_proba(scaled)[0]

        confidence = max(probabilities)

        return prediction, float(confidence)
