import pandas as pd
import joblib
import config
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score
from dataset_adapter import preprocess_dataset

def evaluate_model():
    print(f"[*] Loading model and preparing for chunked evaluation...")
    try:
        model = joblib.load(config.MODEL_SAVE_PATH)
    except:
        print("[!] Model not found.")
        return

    all_preds = []
    all_true = []
    chunk_size = 100000 

    # Process dataset in small chunks to prevent MemoryError
    for chunk in pd.read_csv(config.TEST_DATA_PATH, chunksize=chunk_size):
        X = preprocess_dataset(chunk)
        raw_preds = model.predict(X)
        
        all_preds.extend([1 if p == -1 else 0 for p in raw_preds])
        all_true.extend([1 if label != config.NORMAL_LABEL else 0 for label in chunk[config.LABEL_COLUMN]])
        print(f"[*] Processed {len(all_preds)} rows...")

    print("\n===== Final Evaluation Results =====")
    print(f"Accuracy: {accuracy_score(all_true, all_preds):.4f}")
    print("\nConfusion Matrix:")
    print(confusion_matrix(all_true, all_preds))
    print("\nClassification Report:")
    print(classification_report(all_true, all_preds, target_names=["Normal", "Attack"]))

if __name__ == "__main__":
    evaluate_model()    