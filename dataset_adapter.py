import pandas as pd
import numpy as np
from sklearn.preprocessing import RobustScaler
import joblib
import os
import config

def preprocess_dataset(df, is_training=False):
    # 1. Select only features we want
    X = df[config.SELECTED_FEATURES].copy()
    
    # 2. Critical: Handle Infinities and NaNs from the 'Rate' features
    X = X.replace([np.inf, -np.inf], np.nan)
    X = X.fillna(0)
    
    # 3. Scaling Logic
    os.makedirs("models", exist_ok=True)
    
    if is_training:
        # We use RobustScaler to ignore outliers in network traffic
        scaler = RobustScaler()
        X_scaled = scaler.fit_transform(X)
        joblib.dump(scaler, "models/scaler.pkl")
        print("[*] Scaler fitted on training data and saved.")
    else:
        # Load the existing scaler for evaluation/UI
        if not os.path.exists("models/scaler.pkl"):
            raise FileNotFoundError("Scaler not found! Train the model first.")
        scaler = joblib.load("models/scaler.pkl")
        X_scaled = scaler.transform(X)
        
    return pd.DataFrame(X_scaled, columns=config.SELECTED_FEATURES)