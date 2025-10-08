# train_model.py
# creates a toy regressor model for demo and saves to ml/biocatch_toy_model.joblib
import numpy as np
import joblib
from sklearn.ensemble import RandomForestRegressor
import os

X = []
y = []
for i in range(2000):
    temp = np.random.normal(27, 3)
    sal = np.random.normal(34, 2)
    tide = np.random.uniform(0, 2)
    moon = np.random.uniform(0, 1)
    last = np.random.poisson(1)
    score = 0.0
    if 24 <= temp <= 30:
        score += 0.4
    if 30 <= sal <= 38:
        score += 0.2
    score += min(0.2, tide * 0.1)
    score += (1 - abs(moon - 0.5)) * 0.2
    score += min(0.2, last * 0.05)
    noise = np.random.normal(0, 0.05)
    yval = max(0, min(1, score + noise))
    X.append([temp, sal, tide, moon, last])
    y.append(yval)

X = np.array(X)
y = np.array(y)

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X, y)

out_dir = os.path.dirname(__file__)
out_path = os.path.join(out_dir, "biocatch_toy_model.joblib")
joblib.dump(model, out_path)
print("Saved toy model to:", out_path)
