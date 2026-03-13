# Configuration settings for the IoT Edge IDS

# Dataset paths
RAW_DATA_PATH = "data/raw_dataset.csv"
CLEAN_DATA_PATH = "data/clean_data.csv"
MODEL_SAVE_PATH = "saved_ai_model.pkl"

# Features extracted directly from the true CICIoT2023 dataset header
SELECTED_FEATURES = [
    'flow_duration', 
    'Header_Length', 
    'Protocol Type',
    'Duration',
    'Rate',
    'Srate',
    'Drate',
    'Tot sum',
    'Min',
    'Max',
    'AVG',
    'Std',
    'Tot size',
    'Number'
]

# The column name that tells us if it's an attack or normal traffic 
LABEL_COLUMN = "Label" 
NORMAL_LABEL = "Normal" # For CICIoT2023, normal traffic is sometimes 'BenignTraffic' or 'DDoS-ICMP_Flood' etc. for attacks class


# Anomaly threshold
# The Isolation Forest will give a score. Lower negative numbers are more anomalous.
ANOMALY_THRESHOLD = -0.5 
