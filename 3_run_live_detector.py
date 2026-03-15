import joblib
import pandas as pd
import numpy as np
import config
import os
import datetime

class EdgeDetector:
    def __init__(self):
        print(f"[*] Initializing Edge IDS Detector...")
        self.model = None
        self.load_model()

    def load_model(self):
        try:
            if not os.path.exists(config.MODEL_SAVE_PATH):
                print(f"[!] Error: Model file not found at {config.MODEL_SAVE_PATH}.")
                print("[!] Please run 2_train_model.py first.")
                return False
                
            self.model = joblib.load(config.MODEL_SAVE_PATH)
            print("[+] AI Model loaded successfully. Ready for inference.")
            return True
        except Exception as e:
            print(f"[!] Error loading model: {e}")
            return False

    def inspect_flow(self, flow_data_dict):
        """
        Takes a single dictionary representing a network flow and returns an anomaly check.
        """
        if self.model is None:
            return None

        try:
            # Convert the incoming dictionary into a format the AI understands (a single-row Pandas DataFrame)
            # Ensure the order of features perfectly matches what was trained
            df_flow = pd.DataFrame([flow_data_dict])
            
            # Predict
            # .predict() returns 1 for normal, -1 for anomaly
            # .decision_function() returns the actual anomaly score (lower negative is more anomalous)
            prediction = self.model.predict(df_flow)[0]
            score = self.model.decision_function(df_flow)[0]
            
            is_anomaly = True if prediction == -1 else False
            
            return {
                "is_anomalous": is_anomaly,
                "score": score
            }

        except Exception as e:
            print(f"[!] Error inspecting flow: {e}")
            return None
        return {
    "time": datetime.datetime.now(),
    "is_anomalous": is_anomaly,
    "score": score
        }

if __name__ == "__main__":
    print("[*] 3_run_live_detector.py is a module. Please use 4a_replay_simulator.py or 4b_active_simulator.py to test it.")
    
    # Quick sanity check
    detector = EdgeDetector()
    if detector.model:
        # Create a perfectly normal looking fake packet
        fake_flow = {col: 0.5 for col in config.SELECTED_FEATURES}
        result = detector.inspect_flow(fake_flow)
        print(f"[*] Sanity Check Result: {result}")
    
