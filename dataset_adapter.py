import pandas as pd
import joblib
import config

def preprocess_dataset(df):
    try:
        expected_features = joblib.load("features.pkl")
    except:
        expected_features = config.SELECTED_FEATURES

    # No complex mapping needed if config.py matches the CSV exactly
    # Just ensure we handle duplicates and types
    df = df.loc[:, ~df.columns.duplicated()].copy()
    
    df_final = pd.DataFrame(index=df.index)
    for f in expected_features:
        if f in df.columns:
            df_final[f] = df[f].astype('float32')
        else:
            df_final[f] = 0.0 # This should be rare now!

    return df_final[expected_features]