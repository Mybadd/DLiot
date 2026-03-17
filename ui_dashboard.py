import streamlit as st
import pandas as pd
import torch
import joblib
import config
import os
from dataset_adapter import preprocess_dataset

# 1. Architecture Definition (Must match your trained model exactly)
# UPDATE this class in ui_dashboard.py
class IoTAutoencoder(torch.nn.Module):
    def __init__(self, input_dim):
        super().__init__()
        # Matches the 12 -> 6 -> 3 architecture from your successful training
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

st.set_page_config(page_title="IoT IDS Dashboard", layout="wide")
st.title("🛡️ Deep Learning IoT Edge IDS")

# 2. Asset Loading with Error Handling
@st.cache_resource
def load_assets():
    if not os.path.exists(config.MODEL_SAVE_PATH):
        return None, None
    
    model = IoTAutoencoder(config.INPUT_DIM)
    model.load_state_dict(torch.load(config.MODEL_SAVE_PATH))
    model.eval()
    threshold = joblib.load(config.THRESHOLD_PATH)
    return model, threshold

# Global Load
model, threshold = load_assets()

# 3. Sidebar Status
if model is None:
    st.sidebar.error("❌ Model Assets Not Found")
    st.error("Please run `python 2_train_model.py` to generate the model files before using the dashboard.")
    st.stop() # Prevents NameError by stopping the script here
else:
    st.sidebar.success("✅ Model & Scaler Ready")
    st.sidebar.metric("Anomaly Threshold", f"{threshold:.6f}")

# 4. File Uploader Logic
uploaded_file = st.file_uploader("Upload Network Traffic Logs (CSV)", type=["csv"])

if uploaded_file:
    # Read a sample to keep it fast
    df = pd.read_csv(uploaded_file).head(1000)
    
    with st.spinner('Analyzing traffic patterns...'):
        # Preprocess using the saved RobustScaler
        X_scaled = preprocess_dataset(df, is_training=False)
        X_tensor = torch.FloatTensor(X_scaled.values)
        
        with torch.no_grad():
            recons = model(X_tensor)
            mse = torch.mean((recons - X_tensor)**2, dim=1).numpy()
        
        df['Anomaly_Score'] = mse
        df['Prediction'] = ["🚨 ATTACK" if e > threshold else "✅ Normal" for e in mse]
    
    # Dashboard Visuals
    c1, c2 = st.columns([2, 1])
    with c1:
        st.subheader("Live Anomaly Analysis")
        st.line_chart(df['Anomaly_Score'])
    with c2:
        attacks = (df['Prediction'] == "🚨 ATTACK").sum()
        st.metric("Attacks Detected", attacks, delta=f"{attacks} incidents", delta_color="inverse")

    st.subheader("Detailed Traffic Inspection")
    # Apply styling to the prediction column
    st.dataframe(df.style.applymap(
        lambda x: 'background-color: #700000; color: white;' if x == "🚨 ATTACK" else '', 
        subset=['Prediction']
    ))