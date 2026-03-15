import pandas as pd
import time
import config

# Note: Python import parser doesn't like files starting with numbers. 
# We'll use importlib to safely import it.
import importlib.util
import sys

# Safe import for files starting with a number
spec = importlib.util.spec_from_file_location("live_detector", "3_run_live_detector.py")
live_detector = importlib.util.module_from_spec(spec)
sys.modules["live_detector"] = live_detector
spec.loader.exec_module(live_detector)


def run_replay(speed=1.0):
    print("[*] Starting Dataset Replay Simulator...")
    
    detector = live_detector.EdgeDetector()
    if detector.model is None:
        return

    try:
        # For the replay, we'll read the raw dataset so we can see the "true" label
        # and check if our AI guesses correctly.
        df = pd.read_csv(config.RAW_DATA_PATH)
        
        print(f"[*] Replaying {len(df)} network flows...")
        print("-" * 50)
        
        correct_flags = 0
        missed_attacks = 0
        false_alarms = 0
        
        for index, row in df.iterrows():
            # Get the true label
            true_label = row.get(config.LABEL_COLUMN, "Unknown")
            is_true_attack = (true_label != config.NORMAL_LABEL)
            
            # Extract just the features for the detector
            flow_features = {feature: row[feature] for feature in config.SELECTED_FEATURES if feature in row}
            
            # Ask the AI
            result = detector.inspect_flow(flow_features)
            
            if not result:
                continue
                
            # Formatting the output like a real IDS log
            status_symbol = "[ALERT!]" if result["is_anomalous"] else "[ OK ]"
            
            # Print the log (simulating real time)
            print(f"{status_symbol} Score: {result['score']:.4f} | True Label: {true_label}")
            
            # Track metrics
            if result["is_anomalous"] and is_true_attack:
                correct_flags += 1
            elif not result["is_anomalous"] and is_true_attack:
                missed_attacks += 1
            elif result["is_anomalous"] and not is_true_attack:
                false_alarms += 1

            # Sleep to simulate network delay
            time.sleep(0.1 / speed)
            
        print("-" * 50)
        print("[*] Replay Complete. Simulation Results:")
        print(f"    Correctly Blocked Attacks: {correct_flags}")
        print(f"    Missed Attacks (False Negatives): {missed_attacks}")
        print(f"    False Alarms (False Positives): {false_alarms}")

    except FileNotFoundError:
         print(f"[!] Target dataset {config.RAW_DATA_PATH} not found. Generate dummy data with 1_prepare_data.py first.")

if __name__ == "__main__":
    # Run the replay at 5x speed
    run_replay(speed=5.0)
