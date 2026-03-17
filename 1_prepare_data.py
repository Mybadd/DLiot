import pandas as pd
import config
import os

def prepare_data():
    print("[*] Cleaning Large Dataset...")
    # Load only 500,000 rows to keep it fast but "Smart"
    # This is 6,000% more data than your previous 80 rows!
    df_chunk = pd.read_csv(config.RAW_DATA_PATH, nrows=500000) 
    
    # Identify the label column automatically (Label or label)
    label_col = next((c for c in df_chunk.columns if 'label' in c.lower()), None)
    
    # Standardize and Clean
    df_chunk = df_chunk.rename(columns={label_col: config.LABEL_COLUMN}).dropna()
    
    # Save the new, larger training set
    df_chunk.to_csv(config.CLEAN_DATA_PATH, index=False)
    print(f"[*] SUCCESS: New training set saved with {len(df_chunk)} rows.")

if __name__ == "__main__":
    prepare_data()