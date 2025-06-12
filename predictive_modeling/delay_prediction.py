"""
Neural Network-Based Delay Prediction with PCA-Based Feature Selection.

This script assumes precomputed features (including delay_score, efficiency_index, etc.)
and actual delay labels. It applies PCA to reduce feature dimensionality and then uses
a feedforward neural network to predict delay values.

Input:
- X: Feature matrix (pandas DataFrame), already engineered
- y: Delay target (Series or column), e.g., actual delay time in minutes

Output:
- Trained NN model
- Loss curve
- Predicted vs actual delay scatter plot
"""

import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping

X = pd.read_csv(r"E:\sid\TU Darmstadt\Module und Lehrveranstaltungen\WS2022\MLA practical\engineered_features.csv")
y = pd.read_csv(r"E:\sid\TU Darmstadt\Module und Lehrveranstaltungen\WS2022\MLA practical\target_delay.csv")["delay"]

# 1. Normalize features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 2. PCA for feature reduction
pca = PCA(n_components=0.95)  # retain 95% variance
X_pca = pca.fit_transform(X_scaled)

# 3. Split data (train/test)
X_train, X_test, y_train, y_test = train_test_split(X_pca, y, test_size=0.2, random_state=42)

# 4. Define Neural Network model
model = Sequential([
    Dense(64, activation='relu', input_shape=(X_train.shape[1],)),
    Dropout(0.2),
    Dense(32, activation='relu'),
    Dense(1)  # Output layer for regression
])

model.compile(optimizer='adam', loss='mse', metrics=['mae'])

# 5. Train with early stopping
early_stop = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)
history = model.fit(
    X_train, y_train,
    validation_split=0.2,
    epochs=200,
    batch_size=32,
    callbacks=[early_stop],
    verbose=1
)

# 6. Evaluation
y_pred = model.predict(X_test).flatten()
mse = mean_squared_error(y_test, y_pred)
print(f"Test MSE: {mse:.2f}")

# 7. Plot learning curve
plt.plot(history.history['loss'], label='Train Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.title("Training Loss Curve")
plt.xlabel("Epochs")
plt.ylabel("Loss (MSE)")
plt.legend()
plt.show()

# 8. Plot predicted vs actual
plt.figure()
plt.scatter(y_test, y_pred, alpha=0.5)
plt.xlabel("Actual Delay")
plt.ylabel("Predicted Delay")
plt.title("Predicted vs Actual Delay")
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--')
plt.show()
