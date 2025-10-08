# ml helper: loads model if exists and predict a probability
import os
import joblib
import numpy as np

MODEL_PATH = os.getenv("BIOCATCH_MODEL_PATH", os.path.join(os.path.dirname(__file__), "..", "..", "ml", "biocatch_toy_model.joblib"))

def load_model():
    if os.path.exists(MODEL_PATH):
        try:
            m = joblib.load(MODEL_PATH)
            return m
        except Exception:
            return None
    return None

_model = load_model()

def predict_score(features: dict):
    """
    features keys: sea_temp, salinity, tide_height, moon_phase, last_catch_count
    Returns score in 0..1
    If trained model available, uses it, otherwise falls back to heuristic.
    """
    if _model is not None:
        # ensure order
        X = [[
            features.get('sea_temp', 27.0),
            features.get('salinity', 34.0),
            features.get('tide_height', 1.0),
            features.get('moon_phase', 0.5),
            features.get('last_catch_count', 1)
        ]]
        try:
            pred = _model.predict(X)
            return float(max(0.0, min(1.0, float(pred[0]))))
        except Exception:
            pass

    # heuristic fallback
    temp = features.get('sea_temp', 27.0)
    sal = features.get('salinity', 34.0)
    tide = features.get('tide_height', 1.0)
    moon = features.get('moon_phase', 0.5)
    last = features.get('last_catch_count', 1)

    score = 0.0
    if 24 <= temp <= 30:
        score += 0.4
    else:
        score += max(0, 0.4 - abs(temp - 27) * 0.02)

    if 30 <= sal <= 38:
        score += 0.2
    else:
        score += max(0, 0.2 - abs(sal - 34) * 0.01)

    score += min(0.2, tide * 0.1)
    score += (1 - abs(moon - 0.5)) * 0.2
    score += min(0.2, last * 0.05)

    return float(np.clip(score, 0, 1))
