import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
import pandas as pd
import numpy as np
import joblib
import config
import os
from dataset_adapter import preprocess_dataset

class IoTAutoencoder(nn.Module):
    def __init__(self, input_dim):
        super(IoTAutoencoder, self).__init__()
        # Deeper layers to capture complex patterns
        self.encoder = nn.Sequential(
            nn.Linear(input_dim, 12), nn.ReLU(),
            nn.Linear(12, 6), nn.ReLU(),
            nn.Linear(6, 3) # Latent Dim 3
        )
        self.decoder = nn.Sequential(
            nn.Linear(3, 6), nn.ReLU(),
            nn.Linear(6, 12), nn.ReLU(),
            nn.Linear(12, input_dim)
        )
    def forward(self, x): return self.decoder(self.encoder(x))

def train_dl_model():
    print("-" * 50)
    print("[*] Training Deep Learning Autoencoder...")
    
    df = pd.read_csv(config.CLEAN_DATA_PATH)
    # Filter for Benign only
    train_df = df[df[config.LABEL_COLUMN].astype(str).str.lower() == config.NORMAL_LABEL.lower()]
    
    print(f"[*] Training on {len(train_df)} rows of Normal traffic.")
    
    # Preprocess with is_training=True
    X_train_scaled = preprocess_dataset(train_df, is_training=True)
    X_tensor = torch.FloatTensor(X_train_scaled.values)
    
    model = IoTAutoencoder(config.INPUT_DIM)
    optimizer = optim.Adam(model.parameters(), lr=config.LEARNING_RATE)
    criterion = nn.MSELoss()
    
    loader = DataLoader(TensorDataset(X_tensor), batch_size=config.BATCH_SIZE, shuffle=True)
    
    model.train()
    for epoch in range(config.EPOCHS):
        total_loss = 0
        for batch in loader:
            inputs = batch[0]
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, inputs)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
        
        if (epoch + 1) % 5 == 0 or epoch == 0:
            print(f"    Epoch [{epoch+1}/{config.EPOCHS}], Avg Loss: {total_loss/len(loader):.6f}")

    # Calculate 98th Percentile Threshold
    model.eval()
    with torch.no_grad():
        preds = model(X_tensor)
        mse = torch.mean((preds - X_tensor)**2, dim=1)
        threshold = np.percentile(mse.numpy(), 75) 
    
    torch.save(model.state_dict(), config.MODEL_SAVE_PATH)
    joblib.dump(threshold, config.THRESHOLD_PATH)
    print(f"[*] SUCCESS: Model saved. Threshold: {threshold:.6f}")

if __name__ == "__main__":
    train_dl_model()