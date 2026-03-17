import torch
import joblib
import pandas as pd
import config
from dataset_adapter import preprocess_dataset
import time
import os
import csv

# 1. Architecture (Synchronized with your 93% model)
class IoTAutoencoder(torch.nn.Module):
    def __init__(self, input_dim):
        super().__init__()
        self.encoder = torch.nn.Sequential(
            torch.nn.Linear(input_dim, 12), torch.nn.ReLU(),
            torch.nn.Linear(12, 6), torch.nn.ReLU(),
            torch.nn.Linear(6, 3) 
        )
        self.decoder = torch.nn.Sequential(
            torch.nn.Linear(3, 6), torch.nn.ReLU(),
            torch.nn.Linear(6, 12), torch.nn.ReLU(),
            torch.nn.Linear(12, input_dim)
        )
    def forward(self, x): return self.decoder(self.encoder(x))

def log_detection(mse, status):
    """Saves attack data to a persistent CSV log"""
    log_file = "detection_log.csv"
    file_exists = os.path.isfile(log_file)
    
    with open(log_file, mode='a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(['Timestamp', 'Anomaly_Score', 'Detection_Status'])
        
        writer.writerow([time.strftime('%Y-%m-%d %H:%M:%S'), f"{mse:.6f}", status])

def run_detector():
    print("="*50)
    print("🛡️  IoT LIVE INTRUSION DETECTION SYSTEM ACTIVE")
    print("="*50)

    # Load Model & Threshold
    model = IoTAutoencoder(config.INPUT_DIM)
    model.load_state_dict(torch.load(config.MODEL_SAVE_PATH))
    model.eval()
    threshold = joblib.load(config.THRESHOLD_PATH)
    
    print(f"[*] Monitoring network... (Threshold: {threshold:.6f})")
    print("[*] Logs will be saved to detection_log.csv")

    try:
        while True:
            if os.path.exists("live_stream.csv"):
                data = pd.read_csv("live_stream.csv").tail(1)
                os.remove("live_stream.csv") 
                
                # Predict
                X_scaled = preprocess_dataset(data, is_training=False)
                X_tensor = torch.FloatTensor(X_scaled.values)
                
                with torch.no_grad():
                    recons = model(X_tensor)
                    mse = torch.mean((recons - X_tensor)**2, dim=1).item()
                
                status = "🚨 ATTACK" if mse > threshold else "✅ Normal"
                color = "\033[91m" if mse > threshold else "\033[92m"
                
                # Print to console
                print(f"[{time.strftime('%H:%M:%S')}] Score: {mse:.4f} | Status: {color}{status}\033[0m")
                
                # Save only Attacks to the persistent log
                if mse > threshold:
                    log_detection(mse, "MALICIOUS_TRAFFIC_DETECTED")
                
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\n[*] Shutting down IDS...")

if __name__ == "__main__":
    run_detector()