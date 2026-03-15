import pandas as pd
import numpy as np
import config
import os

def load_and_clean_data(file_path):
    print(f"[*] Loading raw dataset from: {file_path}")
    try:
        # Load data
        df = pd.read_csv(file_path)
        
        # --- FIX: Standardize column names to match config.py ---
        # This handles the case sensitivity (e.g., 'Flow_Duration' vs 'flow_duration')
        df.columns = df.columns.str.strip() # Remove hidden spaces
        
        # Keep only the features we need for the Edge model + the label
        columns_to_keep = config.SELECTED_FEATURES + [config.LABEL_COLUMN]
        
        # Check if requested columns exist
        missing_cols = [col for col in columns_to_keep if col not in df.columns]
        if missing_cols:
            print(f"[!] Warning: Data is missing requested columns: {missing_cols}")
            # Filter columns to only those that exist
            columns_to_keep = [c for c in columns_to_keep if c in df.columns]

        df_filtered = df[columns_to_keep].copy()

        # Handle missing values
        initial_len = len(df_filtered)
        df_cleaned = df_filtered.dropna()
        print(f"[*] Dropped {initial_len - len(df_cleaned)} rows with NaN values.")

        # Save the clean dataset
        os.makedirs(os.path.dirname(config.CLEAN_DATA_PATH), exist_ok=True)
        df_cleaned.to_csv(config.CLEAN_DATA_PATH, index=False)
        print(f"[*] Clean data saved to: {config.CLEAN_DATA_PATH}")
        print(f"[*] Final dataset size: {df_cleaned.shape}")
        
    except Exception as e:
        print(f"[!] Error processing data: {e}")

if __name__ == "__main__":
    # Ensure the directory exists
    os.makedirs(os.path.dirname(config.RAW_DATA_PATH), exist_ok=True)
    
    # --- IMPORTANT: Change this logic to use your REAL data ---
    if not os.path.exists(config.RAW_DATA_PATH):
        print(f"[!] {config.RAW_DATA_PATH} not found. Creating dummy data...")
        # Only creates dummy data if your real file is missing
        dummy_data = {col: np.random.rand(100) for col in config.SELECTED_FEATURES}
        dummy_data[config.LABEL_COLUMN] = [config.NORMAL_LABEL] * 80 + ["Attack"] * 20
        pd.DataFrame(dummy_data).to_csv(config.RAW_DATA_PATH, index=False)
        print(f"[*] Created dummy test data at {config.RAW_DATA_PATH}")
    else:
        print(f"[*] Found existing dataset at {config.RAW_DATA_PATH}. Processing now...")

    load_and_clean_data(config.RAW_DATA_PATH)