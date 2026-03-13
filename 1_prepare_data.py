import pandas as pd
import numpy as np
import config
import os

def load_and_clean_data(file_path):
    print(f"[*] Loading raw dataset from: {file_path}")
    try:
        # Load data (assuming CSV for now, we'll update if using a different format)
        df = pd.read_csv(file_path)
        
        # Keep only the features we need for the Edge model + the label
        columns_to_keep = config.SELECTED_FEATURES + [config.LABEL_COLUMN]
        
        # Check if requested columns exist
        missing_cols = [col for col in columns_to_keep if col not in df.columns]
        if missing_cols:
            print(f"[!] Warning: Data is missing requested columns: {missing_cols}")
            # Filter columns to only those that exist
            columns_to_keep = [c for c in columns_to_keep if c in df.columns]

        df_filtered = df[columns_to_keep]

        # Handle missing values (simple drop for now)
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
    # Create dummy raw data for testing if it doesn't exist
    os.makedirs(os.path.dirname(config.RAW_DATA_PATH), exist_ok=True)
    if not os.path.exists(config.RAW_DATA_PATH):
        print("[!] Raw dataset not found. Creating a dummy file for testing purposes...")
        # create a dummy dataset with the required columns
        dummy_data = {col: np.random.rand(100) for col in config.SELECTED_FEATURES}
        dummy_data[config.LABEL_COLUMN] = ["Normal"] * 80 + ["Attack"] * 20
        pd.DataFrame(dummy_data).to_csv(config.RAW_DATA_PATH, index=False)
        print(f"[*] Created standard test data at {config.RAW_DATA_PATH}")

    load_and_clean_data(config.RAW_DATA_PATH)
