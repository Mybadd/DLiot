import pandas as pd
import joblib

def preprocess_dataset(df):

    # Load training features
    features = joblib.load("features.pkl")

    # Normalize column names
    df.columns = df.columns.str.lower()

    # Example mapping (optional)
    column_mapping = {
        "duration": "flow_duration",
        "avg": "fwd_pkt_len_mean",
        "max": "fwd_pkt_len_max",
        "min": "fwd_pkt_len_min",
        "header_length": "totlen_fwd_pkts"
    }

    df = df.rename(columns=column_mapping)

    # Create missing columns
    for f in features:
        if f not in df.columns:
            df[f] = 0

    # Keep only model features and enforce correct order
    df = df[features]

    return df