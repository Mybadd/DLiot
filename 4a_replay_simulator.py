import pandas as pd
import time
import os
import config

def start_simulation(speed=1.0):
    print("="*50)
    print("🚀  NETWORK TRAFFIC SIMULATOR (CICIOT23 REPLAY)")
    print("="*50)
    
    if not os.path.exists(config.TEST_DATA_PATH):
        print(f"[!] ERROR: Test file not found at {config.TEST_DATA_PATH}")
        return

    # Load 500 rows from the test set for the demo
    print(f"[*] Loading data from: {config.TEST_DATA_PATH}")
    df = pd.read_csv(config.TEST_DATA_PATH, nrows=500)
    
    # Identify label column for the simulator's console output
    label_col = next((c for c in df.columns if 'label' in c.lower()), None)

    print(f"[*] Replaying {len(df)} packets...")
    print(f"[*] Speed: {speed} seconds per packet.")
    print("[*] Press Ctrl+C to stop simulation.")
    print("-" * 50)

    try:
        for i in range(len(df)):
            # 1. Grab one row (one "packet")
            packet = df.iloc[[i]]
            
            # 2. Write it to the shared 'live_stream.csv' file
            # The detector (3_run_live_detector.py) is watching for this file!
            packet.to_csv("live_stream.csv", index=False)
            
            # 3. Print what we sent
            true_label = packet[label_col].values[0] if label_col else "Unknown"
            print(f"[{i+1}/500] 📡 Sent Packet | Original Label: {true_label}")
            
            # 4. Wait based on speed
            time.sleep(speed)
            
    except KeyboardInterrupt:
        print("\n[!] Simulation stopped by user.")
    
    # Clean up the stream file on exit
    if os.path.exists("live_stream.csv"):
        os.remove("live_stream.csv")

if __name__ == "__main__":
    # Change speed here (e.g., 0.5 for faster, 2.0 for slower)
    start_simulation(speed=1.0)