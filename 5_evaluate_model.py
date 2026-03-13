import pandas as pd
import joblib
import config
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score

def evaluate_model():

    print("[*] Loading dataset for evaluation...")

    df = pd.read_csv(config.CLEAN_DATA_PATH)

    if config.LABEL_COLUMN not in df.columns:
        print("[!] Label column not found in dataset.")
        return

    X = df.drop(columns=[config.LABEL_COLUMN])
    y_true = df[config.LABEL_COLUMN]

    print("[*] Loading trained model...")
    model = joblib.load(config.MODEL_SAVE_PATH)

    print("[*] Running predictions...")

    preds = model.predict(X)

    # Convert Isolation Forest output
    preds = [1 if p == -1 else 0 for p in preds]

    # Convert labels
    y_true = [1 if label != config.NORMAL_LABEL else 0 for label in y_true]

    print("\n===== Evaluation Results =====")

    acc = accuracy_score(y_true, preds)
    print(f"Accuracy: {acc:.4f}")

    cm = confusion_matrix(y_true, preds)
    print("\nConfusion Matrix:")
    print(cm)

    print("\nClassification Report:")
    print(classification_report(y_true, preds))

    # False Positive Rate
    tn, fp, fn, tp = cm.ravel()
    fpr = fp / (fp + tn)

    print(f"\nFalse Positive Rate: {fpr:.4f}")

if __name__ == "__main__":
    evaluate_model()