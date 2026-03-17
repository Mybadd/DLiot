import os

# 1. Feature Selection (ALIGNED with your actual test.csv columns)
SELECTED_FEATURES = [
    "flow_duration", "Header_Length", "Rate", "Srate", "Drate", 
    "IAT", "Protocol Type", "fin_flag_number", "syn_flag_number"
]
# 2. Paths (Relative paths are more reliable)
RAW_DATA_PATH = "CICIOT23/train/train.csv" # Update to your actual train filename
TEST_DATA_PATH = "CICIOT23/test/test.csv"
CLEAN_DATA_PATH = "data/clean_data.csv"

MODEL_SAVE_PATH = "models/autoencoder_model.pth"
THRESHOLD_PATH = "models/reconstruction_threshold.pkl"

# 3. Dataset Labels
# In config.py:
RAW_DATA_PATH = "CICIOT23/train/train.csv" 
LABEL_COLUMN = "label" 
NORMAL_LABEL = "BenignTraffic"

# 4. Deep Learning Hyperparameters
INPUT_DIM = len(SELECTED_FEATURES)
LATENT_DIM = 4      
LEARNING_RATE = 0.001
EPOCHS = 15
BATCH_SIZE = 64
THRESHOLD_PERCENTILE = 80
