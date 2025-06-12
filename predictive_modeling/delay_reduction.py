"""
This script performs delay reduction using black-box optimization (scipy minimize).
It assumes a trained neural network that predicts delay, and attempts to adjust
controllable features (e.g., avg_speed, num_switches) to minimize predicted delay.

Steps:
1. Load engineered features and target delay.
2. Preprocess using StandardScaler and PCA (trained on the same dataset).
3. Train a neural network (or load an existing one).
4. Use scipy.optimize.minimize to find feature values that reduce predicted delay.

Note:
- Assumes the neural network is trained on PCA-reduced data.
- Works per sample (can be extended to batch optimization).
"""

import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.callbacks import EarlyStopping
from scipy.optimize import minimize

# Load features and delay target
X = pd.read_csv(r"E:\sid\TU Darmstadt\Module und Lehrveranstaltungen\WS2022\MLA practical\engineered_features.csv")
y = pd.read_csv(r"E:\sid\TU Darmstadt\Module und Lehrveranstaltungen\WS2022\MLA practical\target_delay.csv")["delay"]

# === Step 1: Preprocessing ===
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

pca = PCA(n_components=0.95)
X_pca = pca.fit_transform(X_scaled)

# === Step 2: Train neural network ===
X_train, X_test, y_train, y_test = train_test_split(X_pca, y, test_size=0.2, random_state=42)

model = Sequential([
    Dense(64, activation='relu', input_shape=(X_pca.shape[1],)),
    Dense(32, activation='relu'),
    Dense(1)  # Regression output
])

model.compile(optimizer='adam', loss='mse')
model.fit(X_train, y_train, validation_split=0.2,
          epochs=100, batch_size=32,
          callbacks=[EarlyStopping(patience=10, restore_best_weights=True)],
          verbose=0)

# === Step 3: Optimization for delay reduction ===

# Sample to optimize
x_original = X.iloc[0].copy()

# Controllable features
controllable = ['avg_speed', 'num_switches', 'track_utilization']
fixed = [f for f in X.columns if f not in controllable]

# Preprocessing function
def preprocess(row):
    row_df = pd.DataFrame([row])
    scaled = scaler.transform(row_df)
    reduced = pca.transform(scaled)
    return reduced

# Objective: minimize predicted delay
def objective(x_var):
    x_new = x_original.copy()
    x_new[controllable] = x_var
    x_input = preprocess(x_new)
    pred = model.predict(x_input, verbose=0).flatten()[0]
    return pred

# Initial values and bounds
x0 = x_original[controllable].values
bounds = [
    (60, 160),       # avg_speed [km/h]
    (1, 10),         # num_switches
    (0.3, 1.0)       # track_utilization
]

# Run optimization
result = minimize(objective, x0, bounds=bounds, method='L-BFGS-B')

# === Step 4: Output results ===
optimized_values = result.x
original_delay = objective(x0)
optimized_delay = result.fun

print(f"Original delay:   {original_delay:.2f} minutes")
print(f"Optimized delay:  {optimized_delay:.2f} minutes")
print("Suggested adjustments:")
for f, old, new in zip(controllable, x0, optimized_values):
    print(f"  {f}: {old:.2f} → {new:.2f}")
