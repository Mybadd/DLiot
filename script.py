import pandas as pd
import config

# Load a small sample
df = pd.read_csv(config.TEST_DATA_PATH, nrows=5)

print("--- DATASET VERIFICATION ---")
print(f"Total Columns found: {len(df.columns)}")
print("\nActual Column Names (First 10):")
print(df.columns.tolist()[:10])

print("\n--- LABEL VERIFICATION ---")
# Check if the label column exists
if config.LABEL_COLUMN in df.columns:
    # Load more rows just to find unique labels
    df_labels = pd.read_csv(config.TEST_DATA_PATH, usecols=[config.LABEL_COLUMN])
    print("Unique labels found in dataset:")
    print(df_labels[config.LABEL_COLUMN].unique())
    print(f"\nYour config.py expects: '{config.NORMAL_LABEL}'")
else:
    print(f"[!] ERROR: Column '{config.LABEL_COLUMN}' not found!")