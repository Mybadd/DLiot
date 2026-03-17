import torch
import torch.nn as nn
import pandas as pd
import numpy as np
import joblib
import config
from dataset_adapter import preprocess_dataset
from sklearn.metrics import classification_report, confusion_matrix

class IoTAutoencoder(nn.Module):
    def __init__(self, input_dim):
        super(IoTAutoencoder, self).__init__()
        # NEW DEEPER ARCHITECTURE (Must match 2_train_model.py exactly)
        self.encoder = nn.Sequential(
            nn.Linear(input_dim, 12), nn.ReLU(),
            nn.Linear(12, 6), nn.ReLU(),
            nn.Linear(6, 3) 
        )
        self.decoder = nn.Sequential(
            nn.Linear(3, 6), nn.ReLU(),
            nn.Linear(6, 12), nn.ReLU(),
            nn.Linear(12, input_dim)
        )
    def forward(self, x): return self.decoder(self.encoder(x))

def evaluate_dl_model():
    print("-" * 50)
    print("[*] Evaluating Model on Test Set...")
    
    model = IoTAutoencoder(config.INPUT_DIM)
    model.load_state_dict(torch.load(config.MODEL_SAVE_PATH))
    model.eval()
    threshold = joblib.load(config.THRESHOLD_PATH)
    
    all_preds, all_labels = [], []

    for chunk in pd.read_csv(config.TEST_DATA_PATH, chunksize=100000):
        # 1. Preprocess using the saved scaler (is_training=False)
        X_scaled = preprocess_dataset(chunk, is_training=False)
        X_tensor = torch.FloatTensor(X_scaled.values)
        
        with torch.no_grad():
            recons = model(X_tensor)
            mse = torch.mean((recons - X_tensor)**2, dim=1).numpy()
            preds = ["Attack" if e > threshold else "Normal" for e in mse]
            
        all_preds.extend(preds)
        
        # Standardize labels for the report
        label_col = next((c for c in chunk.columns if 'label' in c.lower()), None)
        labels = chunk[label_col].apply(lambda x: "Normal" if str(x).lower() in ['normal', 'benign', 'benigntraffic'] else "Attack")
        all_labels.extend(labels.tolist())

    print("\n" + "="*40 + "\n      FINAL DL PERFORMANCE\n" + "="*40)
    print(f"Confusion Matrix:\n{confusion_matrix(all_labels, all_preds, labels=['Normal', 'Attack'])}")
    print("-" * 40)
    print(classification_report(all_labels, all_preds))

if __name__ == "__main__":
    evaluate_dl_model() 