import pandas as pd
import config
# Load just the header of the test file
df = pd.read_csv(config.TEST_DATA_PATH, nrows=1)
print("--- TEST FILE COLUMNS ---")
print(df.columns.tolist())