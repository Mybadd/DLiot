import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib
import config

def train_anomaly_detector():

    print(f"[*] Loading clean data from: {config.CLEAN_DATA_PATH}")

    try:
        df = pd.read_csv(config.CLEAN_DATA_PATH)

        if config.LABEL_COLUMN in df.columns:

            print("[*] Filtering dataset to train ONLY on normal traffic...")

            normal_data = df[df[config.LABEL_COLUMN] == config.NORMAL_LABEL]

            if len(normal_data) == 0:
                print("[!] Error: No 'Normal' traffic found.")
                return

            X_train = normal_data.drop(columns=[config.LABEL_COLUMN])

        else:
            print("[!] Warning: Label column not found. Training on all data.")
            X_train = df

        print(f"[*] Training Isolation Forest on {len(X_train)} samples...")

        model = IsolationForest(
            n_estimators=200,
            contamination=0.2,
            random_state=42,
            n_jobs=-1
        )

        model.fit(X_train)

        # Save trained model
        joblib.dump(model, config.MODEL_SAVE_PATH)

        # Save training feature list (important for unseen datasets)
        joblib.dump(X_train.columns.tolist(), "features.pkl")

        print(f"[+] Model successfully trained and saved to: {config.MODEL_SAVE_PATH}")
        print("[+] Feature list saved to: features.pkl")

    except FileNotFoundError:
        print("[!] Error: Clean data file not found. Run 1_prepare_data.py first.")

    except Exception as e:
        print(f"[!] Error during training: {e}")

if __name__ == "__main__":
    train_anomaly_detector()