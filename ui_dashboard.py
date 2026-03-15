import streamlit as st
import pandas as pd
import joblib
import config
from dataset_adapter import preprocess_dataset

st.title("IoT Edge Intrusion Detection System")

# Load trained model
model = joblib.load(config.MODEL_SAVE_PATH)

st.write("Upload a dataset to detect anomalies")

uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file is not None:

    # Read dataset
    df = pd.read_csv(uploaded_file)

    st.subheader("Dataset Preview")
    st.dataframe(df.head())

    # Convert dataset to training feature format
    X = preprocess_dataset(df)

    # Run prediction
    preds = model.predict(X)

    preds = ["Attack" if p == -1 else "Normal" for p in preds]

    df["Prediction"] = preds

    st.subheader("Detection Results")
    st.dataframe(df)

    # Count detected attacks
    attack_count = preds.count("Attack")

    st.metric("Detected Attacks", attack_count)